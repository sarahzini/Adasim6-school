from pydantic import BaseModel, Field

# TODO - Catch exceptions for invalid input and return appropriate error messages

class PupilCreate(BaseModel):
    PupilID: str = Field(..., pattern=r"^[0-9]{8,10}$")
    PupilFullName: str = Field(..., pattern=r"^[a-zA-Z\s]+$")
    PupilClass: int

class TeacherCreate(BaseModel):
    TeacherID: str = Field(..., pattern=r"^[0-9]{8,10}$")
    TeacherFullName: str = Field(..., pattern=r"^[a-zA-Z\s]+$")
    TeacherClass: int