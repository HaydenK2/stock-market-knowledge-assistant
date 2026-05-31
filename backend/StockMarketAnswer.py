from pydantic import BaseModel, Field
from bydantic import ObjectId  # for _id handling
from typing import Optional

class StockMarketQuestion(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    question: str
    answer: str
