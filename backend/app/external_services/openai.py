import openai
from openai import OpenAI
from openai import APIError, RateLimitError, APIConnectionError
from fastapi import HTTPException, status
import os
from app.utils.logger import log_info, log_error

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")  # Default to local reverse proxy

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key. Set the OPENAI_API_KEY environment variable.")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

def get_openai_answer(question: str) -> str:
    try:
        log_info("Fetching answer from OpenAI", {"question": question})

        response = client.chat.completions.create(
            model="cosmosrp-pro",
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": question}],
            max_tokens=300
        )
      
        answer = response.choices[0].message.content.strip()
        log_info("Received response from OpenAI", {"answer": answer})
        return answer

    except APIError as e:
        log_error("OpenAI API returned an API error", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenAI API error occurred."
        )
    except RateLimitError as e:
        log_error("OpenAI API rate limit exceeded", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    except APIConnectionError as e:
        log_error("Failed to connect to OpenAI API", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable. Please try again later."
        )
    except Exception as e:
        log_error("An unexpected error occurred while calling OpenAI API", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Sorry, I couldn't generate an answer at the moment."
        )
