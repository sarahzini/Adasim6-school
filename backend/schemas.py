from pydantic import BaseModel, Field

class PersonBase(BaseModel):
    ID: str = Field(..., pattern=r"^[0-9]{8,10}$")
    FullName: str = Field(..., pattern=r"^[a-zA-Z\s]+$")

# The PupilCreate and TeacherCreate models inherit from PersonBase and add their specific fields

class PupilCreate(PersonBase):
    PupilClass: int

class TeacherCreate(PersonBase):
    TeacherClass: int

class CoordDetail(BaseModel):
    Degrees: str
    Minutes: str
    Seconds: str

class Coordinates(BaseModel):
    Longitude: CoordDetail
    Latitude: CoordDetail

class LocationUpdate(BaseModel):
    ID: int
    Coordinates: Coordinates
    Time: str # Format: YYYY-MM-DDTHH:MM:SSZ
