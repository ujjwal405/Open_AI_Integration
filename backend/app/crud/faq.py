from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.faq import FAQ
from app.schemas.faq import FAQRequest, FAQResponse
from app.utils.logger import log_info, log_error

def create_faq(db: Session, faq_data: FAQRequest)-> FAQResponse:
   
    try:
        new_faq = FAQ(question=faq_data.question, answer=faq_data.answer)
        db.add(new_faq)
        db.commit()
        db.refresh(new_faq)

        
        log_info("FAQ created successfully", {"question": faq_data.question})
        return FAQResponse(  answer=new_faq.answer)
        
    except IntegrityError:
        db.rollback()
        log_error("FAQ already exists: Duplicate question", {"question": faq_data.question})
       
    except Exception as e:
        db.rollback()
        log_error("An error occurred while creating the FAQ", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the FAQ."
        )
    
def get_faq_answer(db: Session, question: str) -> Optional[FAQResponse]:
    """
    Fetches an FAQ answer based on the question.
    Raises an error if the question is not found.
    """
    faq =  db.query(FAQ).filter(FAQ.question.ilike(question)).first()


    if faq is None:
        log_error("FAQ not found", {"question": question})
        return None
      

    log_info("FAQ retrieved successfully", {"question": question})
    return FAQResponse( answer=faq.answer)
