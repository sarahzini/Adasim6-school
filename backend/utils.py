from fastapi import HTTPException
from sqlalchemy import text

#to check that this is a teacher before giving access to certain routes (ex: get all pupils)
def verify_teacher(tz: str, db):
    query = text("SELECT TeacherID FROM TEACHER WHERE TeacherID = :tz")
    if not db.execute(query, {"tz": tz}).first():
        raise HTTPException(status_code=403, detail="Access denied: Teacher not found.")