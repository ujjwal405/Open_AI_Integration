from pydantic import BaseModel

# Request schema for creating an FAQ
class FAQRequest(BaseModel):
    question: str
    answer: str


class FAQResponse(BaseModel):
    answer: str

    class Config:
        orm_mode = True  # This allows SQLAlchemy models to be converted to Pydantic schemas
