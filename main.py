# app/main.py
import datetime
import secrets
from fastapi import FastAPI, Depends
import jwt
from sqlalchemy.orm import Session
import models, database
from models import User

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

secret_key = secrets.token_hex(32)

algorithm = "HS256"
def create_jwt_token(data: dict, expires_delta: int=3600):
    payload = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_delta)
    payload.update({"exp":expire})
    token = jwt.encode(payload,secret_key,algorithm)
    return token

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/getbyid/{id}")
def getbyid(id: int, db: Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        return "user not found"
    return user

@app.post("/")
def add(db: Session = Depends(get_db)):
    user = User(name="Masum", email="masumcsepust@gmail.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/token")
def get_token():
    return create_jwt_token({"username":"masum"}, 15)