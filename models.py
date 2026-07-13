from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
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

    marks = relationship("Marks", back_populates = "student")
    semesters = relationship("Studentsemester",back_populates="student")

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String,unique = True,nullable = False)
    hashed_password = Column(String,nullable = False)

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer,ForeignKey("students.id"), nullable = False)
    subject = Column(String,nullable = False)
    marks_obtained = Column(Integer,nullable = False)
    maximum_marks = Column(Integer,nullable = False)

    student = relationship("Student", back_populates = "marks")

class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_code = Column(String, nullable=False, unique=True)
    subject_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)

    subject_marks = relationship("SubjectMarks", back_populates="subject")


class Studentsemester(Base):
    __tablename__ = "student_semester"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    semester_number = Column(Integer, nullable=False)
    sgpa = Column(Float, nullable=True)

    student = relationship("Student", back_populates="semesters")
    subject_marks = relationship("SubjectMarks", back_populates="student_semester")


class SubjectMarks(Base):
    __tablename__ = "subject_marks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_semester_id = Column(Integer, ForeignKey("student_semester.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    total_marks = Column(Float, nullable=True)
    grade_point = Column(Float, nullable=True)

    student_semester = relationship("Studentsemester", back_populates="subject_marks")
    subject = relationship("Subject", back_populates="subject_marks")
    components = relationship("MarksComponents", back_populates="subject_marks")


class MarksComponents(Base):
    __tablename__ = "markscomponents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_marks_id = Column(Integer, ForeignKey("subject_marks.id"), nullable=False)
    name = Column(String, nullable=False)
    marks_obtained = Column(Float, nullable=False)
    maximum_marks = Column(Float, nullable=False)

    subject_marks = relationship("SubjectMarks", back_populates="components")







