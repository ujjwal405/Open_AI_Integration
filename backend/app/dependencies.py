from app.database.config import SessionLocal

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the database session to the route
    finally:
        db.close()  # Ensure the session is closed after the request
