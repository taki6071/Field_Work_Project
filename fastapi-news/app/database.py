import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
host = os.getenv("HOST")
user = os.getenv("USER")
passwd = os.getenv("PASS")
database = os.getenv("NAME")
port = os.getenv("PORT", "3306")  # Default to 3306 if PORT is not set

# Build the database URL with port
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{database}"

print(f"Connecting to database at host: {host}, port: {port}, user: {user}, database: {database}")

# Create engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test connection
try:
    with engine.connect() as connection:
        print("Database connection is successful.")
except Exception as e:
    print(f"Database connection failed: {e}")
    raise

# Base for ORM models
Base = declarative_base()
