from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.config import init_db  # Creates tables
from app.database import initialize_database  # Seeds initial data
from app.routers.faqs import router as faq_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()  # Ensures tables are created
    initialize_database() 

app.include_router(faq_router, tags=["FAQs"])