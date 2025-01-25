from app.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
def get_db():
    print("get_db: Initializing database session")
    db: Session = SessionLocal()
    try:
        print("get_db: Testing DB connection with SELECT 1")
        db.execute(text("SELECT 1"))
        print("Connection hyse?")
        yield db
    except Exception as e:
        print(f"get_db: Failed to connect to the database: {e}")
        raise
    finally:
        print("get_db: Closing database session")
        db.close()
