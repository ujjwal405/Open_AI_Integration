from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.external_services.openai import get_openai_answer
from app.crud.faq import get_faq_answer, create_faq
from app.schemas.faq import FAQResponse, FAQRequest
from app.utils.utils import normalize_question
from app.utils.logger import log_error


router = APIRouter()



@router.get("/faq", response_model=FAQResponse)
def fetch_faq(question: str, db: Session = Depends(get_db)):
    normalized_question = normalize_question(question)
    faq = get_faq_answer(db, normalized_question)
    
    if faq is None:
        try:
            generated_answer = get_openai_answer(normalized_question)
            faq_data = FAQRequest(question=normalized_question, answer=generated_answer)
            new_faq = create_faq(db, faq_data)
            return new_faq
        except Exception as e:
            log_error("Failed to fetch or create FAQ", {"error": str(e)})
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while generating the answer."
            )
    return faq