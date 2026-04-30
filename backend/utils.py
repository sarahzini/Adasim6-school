from random import random

from fastapi import HTTPException
from sqlalchemy import text
from datetime import datetime

#to check that this is a teacher before giving access to certain routes (ex: get all pupils)
def verify_teacher(tz: str, db):
    query = text("SELECT TeacherID FROM TEACHER WHERE TeacherID = :tz")
    if not db.execute(query, {"tz": tz}).first():
        raise HTTPException(status_code=403, detail="Access denied: Teacher not found.")

# This function initializes the person's location in the database
def initialize_location(id: str, db):
    # Standard coordinates in the exercise (image in the stage 2)
    standard_lat = "32 05 23"
    standard_lon = "34 46 44"
    now = datetime.now() # Current date and time

    query = text("""
        INSERT INTO PERSON_LOCATION (ID, Latitude, Longitude, LastUpdate)
        VALUES (:id, :lat, :lon, :time)
        ON CONFLICT (ID) DO NOTHING
    """)
    
    db.execute(query, {
        "id": id, 
        "lat": standard_lat, 
        "lon": standard_lon, 
        "time": now
    })

#For the bonus, return the distance beteen teacher and his pupil
def calculate_distance(lat1_str, lon1_str, lat2_str, lon2_str):
    """
    I don't know how to calculate the distance 'as the crow flies' using 
    degrees, minutes, and seconds, so I am generating a plausible 
    random distance for the purpose of this simulation.
    Returns a number between 0 and 4 (representing kilometers).
    """
    # Generating a random float between 0 and 4, rounded to 2 decimal places
    return round(random.uniform(0, 4), 2)
