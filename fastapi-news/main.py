
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from sqlalchemy.sql import text
from app.dependencies import get_db 
from app.routers import news, summary

app = FastAPI(
    title="AI-based News Summary API",
    version="0.2",
    description=("This is the API documentation for News Summary generating by AI.  \n\n"
                 "***Developer Information***  \n\n"
                 "---> Developer 01 : Mohammad Kamrul Hasan (C193072)  \n"
                 "---> Developer 02 : Miraj Uddin Chowdhury (C201074) "),
    contact={
        "email": "kamrul@gmail.com",
    },
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Replace "*" with specific domains if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include your routers
app.include_router(news.router)
app.include_router(summary.router)


@app.on_event("startup")
def test_db_connection():
    try:
        # Get a session from the dependency
        db: Session = next(get_db())
        # Use `text` to test the connection
        db.execute(text("SELECT 1"))
        print("Database connection is successful.")
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        raise RuntimeError("Failed to connect to the database.")

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Summary API"}

#Uncomment this block if running as a standalone application
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8011, reload=True)
