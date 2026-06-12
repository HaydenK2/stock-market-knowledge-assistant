from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import uuid
from backend.database import qa_collection
from backend.rag_system.rag import run_rag
import traceback

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    user_id: str | None = None  # optional, if you track users

class RetrievedChunk(BaseModel):
    chunk_id: str
    content_snippet: str
    vector_score: float
    retrieval_source: str
    cross_encoder_score: float
    final_rank: int

class QAResponse(BaseModel):
    eval_id: str
    timestamp: datetime
    query: str
    retrieved_chunks: list
    final_answer: str
    answer_grounded: bool
    grounding_score: float
    latency_ms: float
        


# Ask a question — runs RAG and saves to MongoDB
@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QuestionRequest):
    try:

        print('get final_answer')

        # 1. Run RAG model
        final_answer, rag_result = await run_rag(request.question)

        #   obtain chunks from rag run
        documents = rag_result["documents"]
        retrieved_chunks = [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in documents
        ]

        # 2.  build retrieved_chunks
        qa_document = {
            "eval_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc),
            "query": request.question,
            "retrieved_chunks": retrieved_chunks,
            "final_answer": final_answer,
        }

        print("mongo insert...")
        # 3. Save to MongoDB
        result = await qa_collection.insert_one(qa_document)
        print("mongo saved!")

        return {
            "eval_id": qa_document["eval_id"],
            "query": qa_document["query"],
            "final_answer": qa_document["final_answer"],
            "retrieved_chunks": qa_document["retrieved_chunks"],
            "timestamp": qa_document["timestamp"],
            "answer_grounded": True,
            "grounding_score": 1.0,
            "latency_ms": -1.0
        }

    except Exception as e:
        traceback.print_exc()  # prints full traceback to terminal
        raise HTTPException(status_code=500, detail=str(e))