from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import get_db
import schemas
from utils import verify_teacher

# Define the router for pupil-related endpoints
router = APIRouter(prefix="/pupils", tags=["Pupils"])

# POST endpoint to create a new pupil
@router.post("/")
def create_pupil(pupil: schemas.PupilCreate, db=Depends(get_db)):
    query = text("""
        INSERT INTO PUPIL (PupilID, PupilFullName, PupilClass)
        VALUES (:id, :name, :p_class)
    """)
    try:
        # Execute the SQL query with the provided data
        db.execute(query, {
            "id": pupil.PupilID, 
            "name": pupil.PupilFullName, 
            "p_class": pupil.PupilClass
        })
        db.commit() # Save changes to the database
        return {"message": "Pupil added successfully!"}
    
    except IntegrityError:
        # Catch duplicate IDs specifically
        db.rollback()
        error_msg = f"The ID {pupil.PupilID} already exists in the system, we are waiting for you on the tiyoul!"
        raise HTTPException(status_code=400, detail=error_msg)
        
    except Exception:
        # Catch any other unexpected database error
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected database error occurred.")

# GET endpoint to retrieve a specific pupil by ID
@router.get("/{pupil_id}")
def get_pupil(pupil_id: str, requester_tz: str, db=Depends(get_db)):
    verify_teacher(requester_tz, db)
    
    query = text("SELECT * FROM PUPIL WHERE PupilID = :id")
    result = db.execute(query, {"id": pupil_id}).mappings().first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Pupil not found.")
    return result

# GET endpoint to retrieve all pupils
@router.get("/")
def get_all_pupils(requester_tz: str, db=Depends(get_db)):
    # Security check: verify if the requester is a valid teacher
    verify_teacher(requester_tz, db)
    
    # Fetch all pupils from the database
    query = text("SELECT * FROM PUPIL")
    return db.execute(query).mappings().all()