from database import SessionLocal
from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import Student, Users, Marks
from typing import List
from schemas import StudentOut,StudentCreate,StudentUpdate, UserCreate, MarksCreate, MarksOut
from sqlalchemy import asc, desc, func, Integer
from auth_utils import verify_password, hash_password, create_access_token, get_current_user
import os
import shutil
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

load_dotenv(dotenv_path="config.env")

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.mount("/uploads",StaticFiles(directory = "uploads"),name = "uploads")

@app.get("/students",response_model=List[StudentOut])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return students

@app.post("/add")
def add_student(new_student: StudentCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    student_obj = Student(**new_student.model_dump(mode = "json"))
    db.add(student_obj)
    db.commit()
    return {"message":f"student with roll number {student_obj.roll_num} is inserted in the table"}

@app.put("/update/{roll_num}")
def update_student(roll_num:str,updated_student: StudentUpdate, db:Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_num == roll_num).first()

    if not student:
        return HTTPException(status_code = 404, detail = "Student not found")
    
    update_data = updated_student.model_dump(exclude_unset = True,mode="json")

    for key,value in update_data.items():
        setattr(student,key,value)

    db.commit()
    return {"message":f"student data updated for roll number {roll_num}"}

@app.delete("/delete/{roll_num}")
def delete_student(roll_num:str,db:Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_num == roll_num).first()

    if not student:
        raise HTTPException(status_code = 404,detail = "Student not found")
    
    db.delete(student)
    db.commit()
    return {"message":f"Student with roll number {roll_num} deleted successfully"}

@app.get("/sort",response_model = List[StudentOut])
def sort_students(sort_by:str = Query(...,description = "parameter on the basis of which students need to be sorted"),
                  order: str = Query("asc",description = "order in which we students need to be sorted asc or desc"),
                  db: Session = Depends(get_db)):
    
    valid_fields = ["age","roll_num","name","semester","year","cgpa","id"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400,detail = f"Invalid field choose from {valid_fields}")
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail = "select order from asc or desc")
    
    column = getattr(Student,sort_by)

    if order == "desc":
        column = column.desc()

    students = db.query(Student).order_by(column).all()

    return students

@app.get("/filter",response_model = List[StudentOut])
def filter_students(filter_by:str = Query(None,description="paramter on which students need to be filtered"),
                    min:float = Query(None,description = "minimum value of the parameter"),
                    max:float = Query(None,description = "minimum value of the parameter"),
                    value:str = Query(None,description="value of the parameter"),db:Session = Depends(get_db)):
    
    valid_fields = ["married","cgpa","name","age","semester","id","year","branch","gender"]

    if filter_by not in valid_fields:
        raise HTTPException(status_code = 400,detail = f"Invalid field choose from {valid_fields}")
    
    elif filter_by == "cgpa" or filter_by == "semester" or filter_by == "age" or filter_by == "id":
        if min is None or max is None:
            raise HTTPException(status_code=400,description = "min and max are required")
        column = getattr(Student,filter_by)
        query = db.query(Student).filter(column>=min, column<=max)

    elif filter_by == "married":
        if value not in ["true","false"]:
            raise HTTPException(status_code=400,description = "select value from true or false")
        
        bool_value = value.lower() == "true"
        column = getattr(Student,filter_by)
        query = db.query(Student).filter(column == bool_value)

    elif filter_by == "name":
        if value is None:
            raise HTTPException(status_code=400,description = "value field is required")
        
        column = getattr(Student,filter_by)
        query = db.query(Student).filter(column == value)

    elif filter_by == "gender":
        if value not in ["male","female","others"]:
            raise HTTPException(status_code=400,description = "choose value from male female or others")
        
        column = getattr(Student,filter_by)
        query = db.query(Student).filter(column == value)

    elif filter_by == "branch":

        valid_fields = ["UEC","UCC","UCS","UME","DCS","DEC","PCS","PEC"]

        if value not in valid_fields:
            raise HTTPException(status_code=400,description = f"choose value from {valid_fields}")
        
        column = func.substr(Student.roll_num,3,3)
        query = db.query(Student).filter(column == value)


    elif filter_by == "year":
        if min is None or max is None:
            raise HTTPException(status_code=400,description = "min and max are required")

        column = func.substr(Student.roll_num,1,2).cast(Integer)

        query = db.query(Student).filter(column>=int(min), column<=int(max))

    students = query.all()

    return students

@app.post("/signup")
def signup(user: UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(Users.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code = 400,detail = "username already taken")
    
    new_user = Users(
        username = user.username,
        hashed_password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message":f"user with username {user.username} added to the database"}

@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    
    existing_user = db.query(Users).filter(Users.username == form_data.username).first()

    if not existing_user:
        raise HTTPException(status_code=401,detail = "invalid username or password")
    
    if not verify_password(form_data.password,existing_user.hashed_password):
        raise HTTPException(status_code = 401, detail = "invalid username or password")
    
    access_token = create_access_token(data = {"sub":form_data.username})

    return {"access_token": access_token, "token_type": "bearer"}

UPLOAD_DIR = "uploads/profile_pics"
ALLOWED_TYPES = ["image/jpeg","image/png"]
MAX_FILE_SIZE = 2*1024*1024

os.makedirs(UPLOAD_DIR,exist_ok = True)


@app.post("/upload-profile-pic/{roll_num}")
async def upload_profile_pic(roll_num:str,file:UploadFile = File(...,description="uplaoded image of the student profile"),db:Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_num == roll_num).first()

    if not student:
        raise HTTPException(status_code=400,detail = "student not found")
    
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400,detail = "Invalid file type upload file of jpeg or jpg type")
    
    contents = await file.read()

    if len(contents)>MAX_FILE_SIZE:
        raise HTTPException(status_code=400,detail = "File size should be less than 2MB")
    
    file_extension = file.filename.split(".")[-1]
    file_path = f"{UPLOAD_DIR}/{roll_num}.{file_extension}"

    with open(file_path,"wb") as f:
        f.write(contents)

    student.profile_pic_path = file_path
    db.commit()

    return {"message":f"profile picture of {roll_num} uploaded", "path":file_path}

@app.get("/students/{roll_num}/profile-pic")
def get_profile_pic(roll_num:str, db:Session=Depends(get_db)):
    student = db.query(Student).filter(Student.roll_num == roll_num).first()

    if not student or not student.profile_pic_path:
        raise HTTPException(status_code = 404, detail = f"Profile picture not found for {roll_num}")
    
    return FileResponse(student.profile_pic_path)

@app.post("/students/{roll_num}/marks")
def add_marks(roll_num: str, marks_data: MarksCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_num == roll_num).first()

    if not student:
        raise HTTPException(status_code=404, detail = f"student with {roll_num} not found")
    
    new_marks = Marks(student_id = student.id, **marks_data.model_dump())
    db.add(new_marks)
    db.commit()

    return {"message": "marks added for {roll_num}"}

@app.get("/students/{roll_num}/retrieve_marks",response_model=List[MarksOut])
def get_marks(roll_num: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_num == roll_num).first()

    if not student:
        raise HTTPException(status_code=404, detail = f"student with {roll_num} not found")
    
    return student.marks





    













    


    



    

