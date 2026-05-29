from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import qa_collection
from rag_system.rag import run_rag

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    user_id: str | None = None  # optional, if you track users

class QAResponse(BaseModel):
    question: str
    answer: str
    timestamp: datetime

# Ask a question — runs RAG and saves to MongoDB
@router.post("/ask", response_model=QAResponse)
async def ask_question(request: QuestionRequest):
    try:
        # 1. Run RAG model
        # answer = await run_rag(request.question)
        answer = "temp"

        # 2. Build document to store
        qa_document = {
            "question": request.question,
            "answer": answer,
            "user_id": request.user_id,
            "timestamp": datetime.utcnow()
        }

        # 3. Save to MongoDB
        result = await qa_collection.insert_one(qa_document)

        return {
            "question": request.question,
            "answer": answer,
            "timestamp": qa_document["timestamp"]
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