from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
import pymysql
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "ijwtbpoys")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "audit_logs_db")

# First connect to MySQL without specifying a database to ensure the database exists
ROOT_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/"

# Function to wait for database to be ready
def wait_for_db(max_retries=30, retry_interval=2):
    retries = 0
    while retries < max_retries:
        try:
            # Try to connect to MySQL server
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                port=int(DB_PORT)
            )
            conn.close()
            print("Successfully connected to MySQL server")
            return True
        except pymysql.MySQLError as e:
            print(f"MySQL not ready yet: {e}. Retrying in {retry_interval} seconds...")
            retries += 1
            time.sleep(retry_interval)
    
    print("Failed to connect to MySQL after maximum retries")
    return False

# Create the database if it doesn't exist
def ensure_database_exists():
    try:
        # Connect to MySQL server
        engine = create_engine(ROOT_DATABASE_URL)
        with engine.connect() as conn:
            # Create the database if it doesn't exist
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
            print(f"Database {DB_NAME} created or already exists")
    except Exception as e:
        print(f"Error creating database: {e}")
        raise

# Wait for database to be ready
if not wait_for_db():
    raise Exception("Could not connect to MySQL server")

# Ensure our database exists
ensure_database_exists()

# Now connect to the specific database
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()