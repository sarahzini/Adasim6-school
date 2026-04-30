from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import get_db
import schemas
from utils import verify_teacher
from utils import initialize_location

# Define the router for pupil-related endpoints
router = APIRouter(prefix="/pupils", tags=["Pupils"])

# POST endpoint to create a new pupil
@router.post("/")
def create_pupil(pupil: schemas.PupilCreate, db=Depends(get_db)):
    query_person = text("""
        INSERT INTO PERSON (ID, FullName, UserType)
        VALUES (:id, :name, 'pupil')
    """)
    query_pupil = text("""
        INSERT INTO PUPIL (PupilID, PupilClass)
        VALUES (:id, :p_class)
    """)

    try:
        # Insert into the parent table
        db.execute(query_person, {
            "id": pupil.ID, 
            "name": pupil.FullName
        })
        
        # Insert into the child table 
        db.execute(query_pupil, {
            "id": pupil.ID, 
            "p_class": pupil.PupilClass
        })

        # Initialize the pupil's location in the database
        initialize_location(pupil.ID, db)

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
    
    query = text("""SELECT p.PupilID, pe.FullName AS PupilFullName, p.PupilClass
        FROM PUPIL p
        JOIN PERSON pe ON p.PupilID = pe.ID
        WHERE p.PupilID = :id""")
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
    query = text("""SELECT p.PupilID, pe.FullName AS PupilFullName, p.PupilClass
        FROM PUPIL p
        JOIN PERSON pe ON p.PupilID = pe.ID""")
    return db.execute(query).mappings().all()