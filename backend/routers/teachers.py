from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from database import get_db
import schemas
from utils import initialize_location, verify_teacher

# Define the router for teacher-related endpoints
router = APIRouter(prefix="/teachers", tags=["Teachers"])

# POST endpoint to create a new teacher
@router.post("/")
def create_teacher(teacher: schemas.TeacherCreate, db=Depends(get_db)):
  
    query_person = text("""
        INSERT INTO PERSON (ID, FullName, UserType)
        VALUES (:id, :name, 'teacher')
    """)
    query_teacher = text("""
        INSERT INTO TEACHER (TeacherID, TeacherClass)
        VALUES (:id, :t_class)
    """)

    try:
        # First Try to insert into PERSON
        try:
            db.execute(query_person, {
                "id": teacher.ID, 
                "name": teacher.FullName
            })
        except IntegrityError:
            db.rollback()
            # If it fails here, it's because the ID already exists
            raise HTTPException(
                status_code=400, 
                detail=f"The ID {teacher.ID} already exists in the system."
            )

        # Second we try to insert into TEACHER
        try:
            db.execute(query_teacher, {
                "id": teacher.ID, 
                "t_class": teacher.TeacherClass
            })
        except IntegrityError:
            db.rollback()
            # If it fails here, it's because the Class is already assigned (UNIQUE)
            raise HTTPException(
                status_code=400, 
                detail=f"The class {teacher.TeacherClass} is already assigned to another teacher!"
            )

        # Initialize the teacher's location in the database (for the bonus)
        initialize_location(teacher.ID, db)

        db.commit() # Save everything if both steps passed
        return {"message": "Teacher added successfully!"}
    
    except HTTPException as he:
        # Re-raise the specific HTTP exceptions we just created
        raise he
    except Exception:
        db.rollback()
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
    
    query = text("""
        SELECT t.TeacherID, pe.FullName AS TeacherFullName, t.TeacherClass
        FROM TEACHER t
        JOIN PERSON pe ON t.TeacherID = pe.ID
        WHERE t.TeacherID = :id
    """)
    result = db.execute(query, {"id": teacher_id}).mappings().first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Teacher not found.")
    return result

# GET endpoint to display all pupils assigned to a specific teacher
@router.get("/{teacher_id}/pupils")
def get_pupils_for_teacher(teacher_id: str, requester_tz: str, db=Depends(get_db)):
    verify_teacher(requester_tz, db)
    
    query = text("""
        SELECT p.PupilID, pe.FullName AS PupilFullName, p.PupilClass
        FROM PUPIL p
        JOIN TEACHER t ON p.PupilClass = t.TeacherClass
        JOIN PERSON pe ON p.PupilID = pe.ID
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
    
    query = text("""
        SELECT t.TeacherID, pe.FullName AS TeacherFullName, t.TeacherClass
        FROM TEACHER t
        JOIN PERSON pe ON t.TeacherID = pe.ID
    """)
    result = db.execute(query).mappings().all()
    if not result:
        raise HTTPException(status_code=404, detail="No teachers found.")
    return result   