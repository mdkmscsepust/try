import datetime
import secrets
from fastapi import FastAPI, Depends, HTTPException,status
import jwt
from sqlalchemy.orm import Session
import models, database
from models import User
from passlib.context import CryptContext

from UserIn import UserIn

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

secret_key = secrets.token_hex(32)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
def password_generate(password:str):
    return pwd_context.hash(password)

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

@app.post("/users/register", status_code=status.HTTP_201_CREATED)
def add(userin: UserIn, db: Session = Depends(get_db)):
    try:
        user = User(name=userin.name, username=userin.username, password=password_generate(userin.password), email=userin.email, contact=userin.contact)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as ex:
        raise HTTPException(ex.message)
        

@app.get("/token")
def get_token():
    return create_jwt_token({"username":"masum"}, 15)