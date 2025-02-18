from app.models.faq import FAQ
from .config import  engine, SessionLocal
from sqlalchemy.orm import Session


def init_data(db: Session):
    # Check if FAQs already exist to avoid duplicates
    if db.query(FAQ).first() is None:
        faqs = [
    FAQ(question="what is FastAPI", answer="FastAPI is a modern web framework for building APIs with Python."),
    FAQ(question="how do I install FastAPI", answer="You can install it using `pip install fastapi` and `pip install uvicorn` for the ASGI server."),
    FAQ(question="what is uvicorn", answer="Uvicorn is an ASGI server for running FastAPI applications."),
    FAQ(question="how to run FastAPI", answer="Use `uvicorn your_module:app --reload` to run FastAPI."),
    FAQ(question="what is pydantic", answer="Pydantic is used for data validation in FastAPI."),
    FAQ(question="does FastAPI support async", answer="Yes, FastAPI is designed for asynchronous request handling."),
    FAQ(question="how to add middleware", answer="Use `@app.middleware('http')` to define middleware."),
    FAQ(question="how to use dependencies", answer="Use `Depends` from `fastapi` to inject dependencies."),
    FAQ(question="is FastAPI better than Flask", answer="FastAPI is faster and supports async, but Flask is more mature."),
    FAQ(question="how to handle errors in FastAPI", answer="Use `@app.exception_handler(Exception)` to handle errors."),
]


        db.add_all(faqs)
        db.commit()

def initialize_database():
    db = SessionLocal()
    try:
        init_data(db)
    finally:
        db.close()
