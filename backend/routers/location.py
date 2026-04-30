import random
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from database import get_db
from schemas import LocationUpdate 

router = APIRouter(prefix="/location", tags=["Location"])

# OFFICIAL ROUTE: Used by GPS devices to send data 
@router.post("/update")
def update_location(data: LocationUpdate, db=Depends(get_db)):
    try:
        # Format the data from the Pydantic schema (I respect in schema.py the json format)
        person_id = str(data.ID)
        lat = f"{data.Coordinates.Latitude.Degrees} {data.Coordinates.Latitude.Minutes} {data.Coordinates.Latitude.Seconds}"
        lon = f"{data.Coordinates.Longitude.Degrees} {data.Coordinates.Longitude.Minutes} {data.Coordinates.Longitude.Seconds}"
        timestamp = data.Time.replace('T', ' ').replace('Z', '') # Clean for SQL

        # Then update the specific person's location
        query = text("""
            UPDATE PERSON_LOCATION 
            SET Latitude = :lat, 
                Longitude = :lon, 
                LastUpdate = :time
            WHERE ID = :id
        """)
        
        result = db.execute(query, {"id": person_id, "lat": lat, "lon": lon, "time": timestamp})
        db.commit()
        
        return {"message": "Location updated successfully"}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

#Used for test but that need to come from the GPS device 
@router.get("/run-simulation")
def run_simulation(db=Depends(get_db)):
    # Get everyone 
    query = text("SELECT id, latitude, longitude FROM person_location")
    people = db.execute(query).mappings().all()
    
    for person in people:

        # Extract values using LOWERCASE keys (PostgreSQL default) because we had a pbm with this in a previous run
        # Use .get() to avoid the NoSuchColumnError
        lat_str = person.get("latitude") or person.get("Latitude")
        lon_str = person.get("longitude") or person.get("Longitude")
        person_id = person.get("id") or person.get("ID")

        if not lat_str or not lon_str:
            continue

        lat_parts = lat_str.split()
        lon_parts = lon_str.split()
        
        #  Add +1 or +2 seconds randomly
        new_lat_sec = (int(lat_parts[2]) + random.randint(1, 2)) % 60
        new_lon_sec = (int(lon_parts[2]) + random.randint(1, 2)) % 60
        
        # Reconstruct the new coordinates (because that is not a sting)
        new_lat = f"{lat_parts[0]} {lat_parts[1]} {new_lat_sec:02d}"
        new_lon = f"{lon_parts[0]} {lon_parts[1]} {new_lon_sec:02d}"
        
        # Save to DB
        update_query = text("""
            UPDATE person_location 
            SET latitude = :lat, longitude = :lon, lastupdate = :time 
            WHERE id = :id
        """)
        db.execute(update_query, {
            "lat": new_lat, 
            "lon": new_lon, 
            "time": datetime.now(), 
            "id": person_id
        })
    
    db.commit() 
    return {"message": "Everyone moved!"}

# To display in the front
@router.get("/")
def get_all_locations(db=Depends(get_db)):
    query = text("SELECT ID, Latitude, Longitude FROM PERSON_LOCATION")
    return db.execute(query).mappings().all()