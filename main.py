from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
from models import Student
from schemas import StudentCreate, StudentResponse


# Create database table
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI()


# Database connection
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================
# 1. GET - Get all students
# =====================================

@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):

    students = db.query(Student).all()

    return students


# =====================================
# 2. GET - Get student by ID
# =====================================

@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# =====================================
# 3. POST - Create new student
# =====================================

@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):

    # Check whether email already exists
    existing_student = db.query(Student).filter(
        Student.email == student.email
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # Convert Pydantic data into SQLAlchemy object
    new_student = Student(
        name=student.name,
        email=student.email,
        age=student.age
    )

    # Save student in database
    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    return new_student


# =====================================
# 4. PUT - Update student
# =====================================

@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):

    # Find student
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Check if another student uses this email
    existing_student = db.query(Student).filter(
        Student.email == student_data.email,
        Student.id != student_id
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    # Update student details
    student.name = student_data.name
    student.email = student_data.email
    student.age = student_data.age

    db.commit()

    db.refresh(student)

    return student


# =====================================
# 5. DELETE - Delete student
# =====================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):

    # Find student
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # Delete student
    db.delete(student)

    db.commit()

    return {
        "message": "Student deleted successfully"
    }

# =====================================
# 6. GET - Count adult students
# =====================================

@app.get("/students/count/adults")
def count_adult_students(db: Session = Depends(get_db)):

    student_count = db.query(Student).filter(
        Student.age > 18
    ).count()

    return {
        "total_adult_students": student_count
    }

# =====================================
# 7. GET - Search student by name
# =====================================

@app.get("/students/name/{student_name}", response_model=StudentResponse)
def search_studentname(student_name: str, db: Session = Depends(get_db)):

    student = db.query(Student).filter(
        Student.name == student_name
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student
