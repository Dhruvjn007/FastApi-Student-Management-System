from database import SessionLocal
from models import Student

db = SessionLocal()

student = db.query(Student).filter(Student.roll_num == "23UCS102").first()

if student:
    db.delete(student)
    db.commit()
    print("student deleted")
else:
    print("no such student found")

db.close()