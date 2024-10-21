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
    profile_img: Optional[bytes] = None  # If needed, consider how to handle image uploads

# New Pydantic model for availing an offer
class AvailOfferRequest(BaseModel):
    mobile_number: str
    offer_id: int
    restaurant_id: int


# New Pydantic model for availing an offer
class AvailOfferRequest(BaseModel):
    mobile_number: str
    offer_id: int
    restaurant_id: int


# Endpoint to create a new restaurant
@app.post("/restaurants/", response_model=RestaurantCreate)
def create_restaurant(restaurant: RestaurantCreate, db: Session = Depends(database.get_db)):
    # Check for existing restaurant by name or mobile number, if needed
    new_restaurant = models.Restaurant(
        rest_name=restaurant.rest_name,
        rest_mobile_number=restaurant.rest_mobile_number,
        type=restaurant.type,
        cvr=restaurant.cvr,
        profile_img=restaurant.profile_img,
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant

# Endpoint to create an offer
@app.post("/offers/", response_model=OfferCreate)
def create_offer(offer: OfferCreate, db: Session = Depends(database.get_db)):
    # Verify if the restaurant exists
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
    return new_offer

# Other existing endpoints...

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
    return db_user

# Endpoint to check if a user exists
@app.get("/users/check/{mobile_number}", response_model=UserCreate)
def read_user(mobile_number: str, db: Session = Depends(database.get_db)):
    user = db.query(models.Customers).filter(models.Customers.mobile_number == mobile_number).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user:
        return user
    else:
        return {"message": "failes"}
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
        models.Points.rest_name == user_point_add.restaurant_name,
    ).first()
    
    if existing_points is None:
        # No existing points, create a new entry
        new_points = models.Points(
            customer_id=user.id,
            mobile_number=user_point_add.mobile_number,
            available_points=user_point_add.points,
            used_points=0,
        )
        db.add(new_points)
    else:
        # Update the existing points
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
        models.Points.rest_name == restaurant_name,
    ).scalar()

    if total_points is None:
        total_points = 0  # In case there are no points records, return 0

    return OfferResponse(mobile_number=mobile_number, restaurant_name=restaurant_name, total_points=total_points)
# New endpoint to avail an offer
@app.post("/offers/avail/")
def avail_offer(avail_request: AvailOfferRequest, db: Session = Depends(database.get_db)):
    # Check if user exists
    user = db.query(models.Customers).filter(models.Customers.mobile_number == avail_request.mobile_number).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the offer exists
    offer = db.query(models.OfferTable).filter(models.OfferTable.id == avail_request.offer_id).first()
    if offer is None:
        raise HTTPException(status_code=404, detail="Offer not found")

    # Check if the user has enough points to avail the offer
    total_points = db.query(func.sum(models.Points.available_points)).filter(
        models.Points.customer_id == user.id
    ).scalar()
    
    if total_points is None or total_points < offer.condition_value:
        raise HTTPException(status_code=400, detail="Not enough points to avail this offer")

    # Deduct the points from the user's account (this may depend on your business logic)
    new_points_balance = total_points - offer.condition_value
    user_points_record = db.query(models.Points).filter(models.Points.customer_id == user.id).first()
    user_points_record.available_points = new_points_balance

    # Optionally, you may want to log this action
    # For example, create a new entry in a 'used_offers' table (not shown here)

    db.commit()
    
    return {"message": "Offer availed successfully", "remaining_points": new_points_balance}
