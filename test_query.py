from database import SessionLocal,Session
from models import Student

db = SessionLocal()

student = db.query(Student).get(1)
if student:
    student.name = 'mohit kumar'
    student.age = 15
    db.commit()
    print("successfully updated")
else:
    print("no such student found")

db.close()