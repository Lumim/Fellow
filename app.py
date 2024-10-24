from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
import models, database

app = FastAPI()

# CORS configuration
origins = [
    "https://your-frontend.netlify.app",
    "http://localhost:8000",  # Ensure localhost is included
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

# Pydantic models for request validation
class UserCreate(BaseModel):
    user_name: str
    mobile_number: str

class UserPointAdd(BaseModel):
    user_name: str
    mobile_number: str
    restaurant_name: str
    points: int

class OfferResponse(BaseModel):
    mobile_number: str
    restaurant_name: str
    total_points: int

class OfferCreate(BaseModel):
    restaurant_id: int
    offer_name: str
    details: str
    condition_type: str
    condition_value: int
    type: Optional[str] = None  # Optional field

class RestaurantCreate(BaseModel):
    rest_name: str
    rest_mobile_number: Optional[str] = None
    type: Optional[str] = None
    cvr: Optional[str] = None
    logo_img: Optional[bytes] = None  # If needed, consider how to handle image uploads

class AvailOfferRequest(BaseModel):
    mobile_number: str
    offer_id: int
    restaurant_id: int


# Endpoint to create a new restaurant
class RestaurantResponse(BaseModel):
    restaurant_name: str
    rest_mobile_number: str
    type: str
    cvr: str
    
    class Config:
        orm_mode = True

@app.post("/restaurants/")
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(database.get_db)):
    rest = db.query(models.Restaurant).filter(models.Restaurant.rest_name == restaurant.rest_name).first()
    if rest is None:
        new_restaurant = models.Restaurant(
            rest_name=restaurant.rest_name,
            rest_mobile_number=restaurant.rest_mobile_number,
            type=restaurant.type,
            cvr=restaurant.cvr,
            logo_img=restaurant.logo_img,
        )
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)
        return {
            "restaurant_name": new_restaurant.rest_name,
            "rest_mobile_number": new_restaurant.rest_mobile_number,
            "type": new_restaurant.type,
            "cvr": new_restaurant.cvr
        } 
        #return {"Added successfully"}
    message="restaurant already exist."
    return message
# Endpoint to create an offer
@app.post("/offers/", response_model=OfferCreate)
def create_offer(offer: OfferCreate, db: Session = Depends(database.get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == offer.restaurant_id).first()
    if restaurant is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    new_offer = models.OfferTable(
        restaurant_id=offer.restaurant_id,
        offer_name=offer.offer_name,
        details=offer.details,
        condition_type=offer.condition_type,
        condition_value=offer.condition_value,
        type=offer.type,
    )
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return {
        "restaurant_id": new_offer.restaurant_id,
        "offer_name": new_offer.offer_name,
        "details": new_offer.details,
        "condition_type": new_offer.condition_type,
        "condition_value": new_offer.condition_value,
        "type": new_offer.type
    }
# Endpoint to create a customer
@app.post("/customers/", response_model=UserCreate)
def create_customer(user: UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.Customers).filter(models.Customers.mobile_number == user.mobile_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Mobile number already registered")
    
    db_user = models.Customers(user_name=user.user_name, mobile_number=user.mobile_number)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user  # Directly return the SQLAlchemy model, FastAPI will handle the Pydantic conversion

# Endpoint to check if a user exists
@app.get("/users/check/{mobile_number}")
def read_user(mobile_number: str, db: Session = Depends(database.get_db)):
    user = db.query(models.Customers).filter(models.Customers.mobile_number == mobile_number).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User exists"}
#--------------
# Endpoint to check if a retaurant exists
@app.get("/restaurant/check/{rest_name}")
def read_res(rest_name: str, db: Session = Depends(database.get_db)):
    rest = db.query(models.Restaurant).filter(models.Restaurant.rest_name == rest_name).first()
    if rest is None:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    message="Restaurant name is ",rest.rest_name,"id is ",rest.id
    return message

#root information
@app.get("/")
async def read_root():
    return {"message": "Welcome to Fellow! Use the endpoints to manage customers and offers."}

# Endpoint to add points for a customer at a restaurant
@app.post('/users/restaurant/addpoint')
def add_restaurant_point(user_point_add: UserPointAdd, db: Session = Depends(database.get_db)):
    user = db.query(models.Customers).filter(models.Customers.mobile_number == user_point_add.mobile_number).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the user already has points for the given restaurant
    existing_points = db.query(models.Points).filter(
        models.Points.mobile_number == user_point_add.mobile_number,
        models.Points.restaurant_name == user_point_add.restaurant_name,
    ).first()
    
    if existing_points is None:
        new_points = models.Points(
            customer_id=user.id,
            mobile_number=user_point_add.mobile_number,
            restaurant_name=user_point_add.restaurant_name,
            available_points=user_point_add.points,
            used_points=0,
        )
        db.add(new_points)
    else:
        existing_points.available_points += user_point_add.points

    db.commit()
    return {"message": "Points added successfully"}

# Endpoint to get total points against a restaurant
@app.get('/users/get/offer/{mobile_number}/{restaurant_name}', response_model=OfferResponse)
def get_offer_against_restaurant(mobile_number: str, restaurant_name: str, db: Session = Depends(database.get_db)):
    user = db.query(models.Customers).filter(models.Customers.mobile_number == mobile_number).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    total_points = db.query(func.sum(models.Points.available_points)).filter(
        models.Points.mobile_number == mobile_number,
        models.Points.restaurant_name == restaurant_name,
    ).scalar()

    if total_points is None:
        total_points = 0  # If no points exist, return 0

    return OfferResponse(mobile_number=mobile_number, restaurant_name=restaurant_name, total_points=total_points)

# Endpoint to avail an offer
@app.post("/offers/avail/")
def avail_offer(avail_request: AvailOfferRequest, db: Session = Depends(database.get_db)):
    # Check if the user exists
    user = db.query(models.Customers).filter(models.Customers.mobile_number == avail_request.mobile_number).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the offer exists
    offer = db.query(models.OfferTable).filter(models.OfferTable.id == avail_request.offer_id).first()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")

    # Calculate total available points for the user
    total_points = db.query(func.sum(models.Points.available_points)).filter(
        models.Points.customer_id == user.id
    ).scalar()

    # If the user has insufficient points, raise an error
    if total_points is None or total_points < offer.condition_value:
        raise HTTPException(status_code=400, detail="Not enough points to avail this offer")

    # Calculate the new points balance after availing the offer
    new_points_balance = total_points - offer.condition_value
    
    # Fetch the user's points record
    user_points_record = db.query(models.Points).filter(models.Points.customer_id == user.id).first()
    
    # Update available points
    user_points_record.available_points = new_points_balance
    
    # Update used points: Add the condition_value (availed points) to the existing used points
    if user_points_record.used_points is None:
        user_points_record.used_points = 0  # Initialize if used_points is null
    user_points_record.used_points += offer.condition_value

    # Commit the changes to the database
    db.commit()
    
    return {"message": "Offer availed successfully", "remaining_points": new_points_balance, "total_used_points": user_points_record.used_points}
