import re

def normalize_question(question: str) -> str:
   
    question = re.sub(r'\s+', ' ', question.strip()).lower()
    question = re.sub(r'[?.]+$', '', question)

    return question
