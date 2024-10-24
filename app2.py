from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
import models, database

app = FastAPI()

origins = [
    "https://your-frontend.netlify.app", "localhost"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the tables in the database
models.Base.metadata.create_all(bind=database.engine)

# Pydantic model for user creation
class UserCreate(BaseModel):
    name: str
    mobile: str

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(models.User.mobile_number == user.mobile).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Mobile number/user already registered")
    
    db_user = models.User(user_name=user.name, mobile_number=user.mobile)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    message="user registered!"
    return db_user,message

@app.get("/users/check/{mobile_number}")
def read_user(mobile_number: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.mobile_number == mobile_number).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    message="user already exist"
    status_code=200,
    return user,message,status_code

@app.get("/")
async def read_root():
    return {"message": "Welcome to Fellow! Use the endpoints to manage users and other services."}
