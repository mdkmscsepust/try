from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from sqlalchemy import create_engine

import database

DATABASE_URL = "postgresql+psycopg2://postgres:12345678@db.zeoubsuvplwxzkmoergu.supabase.co:5432/postgres"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute("SELECT version()")
        print("✅ Connected to:", result.fetchone())
except Exception as e:
    print("❌ Connection failed:", e)

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI with SQLAlchemy ORM!"}
