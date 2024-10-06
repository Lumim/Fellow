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

class UserPointAdd(BaseModel):
    name: str
    mobile: str
    restaurant_name: str  # Fix the typo here
    points: int

@app.post('/users/restaurant/addpoint')
def add_restaurant_point(user_point_add: UserPointAdd, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.mobile_number == user_point_add.mobile).first()  # Adjusted field
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    
    restaurant= db.query(models.UserPoint).filter( models.UserPoint.restaurant_name==user_point_add.restaurant_name).first()
    if restaurant is None:
        db_point_add = models.UserPoint(
        user_name=user_point_add.name,  # Adjusted field
        mobile_number=user_point_add.mobile,  # Adjusted field
        restaurant_name=user_point_add.restaurant_name,
        points=user_point_add.points)
        db.add(db_point_add)
    else:
        total_points = db.query(func.sum(models.UserPoint.points)).filter(
            models.UserPoint.mobile_number == mobile_number,
            models.UserPoint.restaurant_name == restaurant_name,
            models.UserPoint.active == 1,
            ).scalar()
        db_point_add = models.UserPoint(
            user_name=user_point_add.name,  # Adjusted field
            mobile_number=user_point_add.mobile,  # Adjusted field
            restaurant_name=user_point_add.restaurant_name,
            points=user_point_add.points+total_points)
            
        
        db.update(db_point_add)
    db.commit()
    db.refresh(db_point_add)
    
    return {"message": "Point added successfully", "data": db_point_add}

@app.get('/users/get/offer/{mobile_number}/{restaurant_name}')
def get_offer_against_restaurant(mobile_number: str, restaurant_name: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.mobile_number == mobile_number).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
   
    total_points = db.query(func.sum(models.UserPoint.points)).filter(
        models.UserPoint.mobile_number == mobile_number,
        models.UserPoint.restaurant_name == restaurant_name,
        models.UserPoint.active == 1,
        
    ).scalar()

    if total_points is None:
        total_points = 0  # In case there are no points records, return 0

    return {"mobile_number": mobile_number, "restaurant_name": restaurant_name, "total_points": total_points}

