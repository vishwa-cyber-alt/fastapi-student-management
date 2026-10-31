from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Schema for creating a student
class StudentCreate(BaseModel):

    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(gt=0, le=120)


# Schema for returning a student
class StudentResponse(BaseModel):

    id: int
    name: str
    email: EmailStr
    age: int

    model_config = ConfigDict(from_attributes=True)