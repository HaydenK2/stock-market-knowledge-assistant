import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List
from core.config import settings
from rag_system.rag import run_rag
from database import qa_collection
from routes.rag_routes import router as rag_router

MONGO_URL = settings.DATABASE_URL

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    app.mongodb_client = AsyncIOMotorClient(MONGO_URL)
    app.db = app.mongodb_client["stock_market_qa_database"]
    print("Connected to MongoDB")
    yield
    # --- SHUTDOWN ---
    app.mongodb_client.close()
    print("Disconnected from MongoDB")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rag_router, prefix="/api/rag", tags=["RAG"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

    