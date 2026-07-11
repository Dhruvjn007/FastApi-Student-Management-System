from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, autoincrement=True, primary_key=True)
    roll_num = Column(String,unique = True, nullable=False)
    age = Column(Integer, nullable=False)
    name = Column(String,nullable = False)
    cgpa = Column(Float, nullable = False)
    semester = Column(Integer, nullable = False)
    married = Column(Boolean,nullable = False)
    gender = Column(String, nullable = False)
    linkedin = Column(String, nullable = False)
    profile_pic_path = Column(String, nullable=True)

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String,unique = True,nullable = False)
    hashed_password = Column(String,nullable = False)

