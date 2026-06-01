from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid
from database import qa_collection
from rag_system.rag import run_rag

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
    retrieved_chunks: list[RetrievedChunk]
    final_answer: str
    answer_grounded: bool
    grounding_score: float
    latency_ms: float
        


# Ask a question — runs RAG and saves to MongoDB
@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QuestionRequest):
    try:
        # 1. Run RAG model
        final_answer, chunk_records = await run_rag(request.question)

        # 2. Build document to store

        #   build retrieved_chunks
        qa_document = {
            "eval_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "query": request.question,
            "retrieved_chunks": chunk_records,
            "final_answer": final_answer,
        }

        # 3. Save to MongoDB
        result = await qa_collection.insert_one(qa_document)
        
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
        raise HTTPException(status_code=500, detail=str(e))

# Get all past Q&A history
@router.get("/history")
async def get_history(user_id: str | None = None):
    query = {"user_id": user_id} if user_id else {}
    history = []
    async for doc in qa_collection.find(query).sort("timestamp", -1):
        doc["_id"] = str(doc["_id"])
        history.append(doc)
    return history

# Get a single past answer by ID
@router.get("/history/{qa_id}")
async def get_qa(qa_id: str):
    from bson import ObjectId
    doc = await qa_collection.find_one({"_id": ObjectId(qa_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    doc["_id"] = str(doc["_id"])
    return doc