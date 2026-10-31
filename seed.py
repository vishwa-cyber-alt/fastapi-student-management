from database import SessionLocal
from models import Student

db = SessionLocal()

students = [
    Student(name="Arun", email="arun@gmail.com", age=22),
    Student(name="Kumar", email="kumar@gmail.com", age=24),
    Student(name="Ravi", email="ravi@gmail.com", age=23)
]

db.add_all(students)

db.commit()

db.close()

print("Students added successfully!")