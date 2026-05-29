import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from rag_system.app import run_rag
from core.config import settings


app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

class Items(BaseModel):
    items: List[Item]


origins = [
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_db = {"items": []}

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items", response_model=Items)
def get_items():
    return Items(items=memory_db["items"])

@app.post("/items", response_model=Item)
def add_item(item: Item):
    memory_db["items"].append(item)
    return item

@app.post('/create')
def generate_answer(question):
    answer = run_rag(question)

    return answer

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)