from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import get_db
import schemas
from utils import verify_teacher

# Define the router for teacher-related endpoints
router = APIRouter(prefix="/teachers", tags=["Teachers"])

# POST endpoint to create a new teacher
@router.post("/")
def create_teacher(teacher: schemas.TeacherCreate, db=Depends(get_db)):
    query = text("""
        INSERT INTO TEACHER (TeacherID, TeacherFullName, TeacherClass)
        VALUES (:id, :name, :t_class)
    """)
    try:
        # Execute the SQL query with the provided data
        db.execute(query, {
            "id": teacher.TeacherID, 
            "name": teacher.TeacherFullName, 
            "t_class": teacher.TeacherClass
        })
        db.commit() # Save changes to the database
        return {"message": "Teacher added successfully!"}
    
    except IntegrityError:
        # Catch duplicate IDs or duplicate classes
        db.rollback() # Undo the failed transaction
        error_msg = f"The ID {teacher.TeacherID} already exists in the system, or this class is already assigned to another teacher!"
        raise HTTPException(status_code=400, detail=error_msg)
        
    except Exception:
        # Catch any other unexpected database error
        db.rollback() # Undo the failed transaction
        raise HTTPException(status_code=500, detail="An unexpected database error occurred.")

# GET endpoint for teacher login (for simplicity, we just verify the tz and return a success message)
@router.get("/login/{tz}")
def login(tz: str, db=Depends(get_db)):
    verify_teacher(tz, db)
    
    return {"message": "Login successful"}

# GET endpoint to display a specific teacher by ID
@router.get("/{teacher_id}")
def get_teacher(teacher_id: str, requester_tz: str, db=Depends(get_db)):
    verify_teacher(requester_tz, db)
    
    query = text("SELECT * FROM TEACHER WHERE TeacherID = :id")
    result = db.execute(query, {"id": teacher_id}).mappings().first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Teacher not found.")
    return result

# GET endpoint to display all pupils assigned to a specific teacher
@router.get("/{teacher_id}/pupils")
def get_pupils_for_teacher(teacher_id: str, requester_tz: str, db=Depends(get_db)):
    verify_teacher(requester_tz, db)
    
    query = text("""
        SELECT p.* FROM PUPIL p
        JOIN TEACHER t ON p.PupilClass = t.TeacherClass
        WHERE t.TeacherID = :id
    """)
    result = db.execute(query, {"id": teacher_id}).mappings().all()

    if not result:
        raise HTTPException(status_code=404, detail="No pupils found for this teacher.")
    return result

# GET endpoint to display all teachers
@router.get("/")
def get_all_teachers(requester_tz: str, db=Depends(get_db)):
    verify_teacher(requester_tz, db)
    
    query = text("SELECT * FROM TEACHER")
    result = db.execute(query).mappings().all()
    if not result:
        raise HTTPException(status_code=404, detail="No teachers found.")
    return result   