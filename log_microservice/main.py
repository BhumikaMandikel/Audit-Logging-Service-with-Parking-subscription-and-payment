from fastapi import FastAPI
from app import models, database, routes
import time

app = FastAPI(title="PES University Log Management Microservice")

# Wait a bit to ensure the database is fully up and migrations can run safely
time.sleep(3)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Log Management Service is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}