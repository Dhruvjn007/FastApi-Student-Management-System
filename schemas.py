from pydantic import BaseModel, AnyUrl, Field, field_validator, computed_field
from typing import Literal, Annotated, Optional

class StudentCreate(BaseModel):
    roll_num: Annotated[str, Field(..., description="roll number of the student")]
    name: Annotated[str, Field(..., description="name of the student")]
    age: Annotated[int, Field(..., gt=15, lt=28)]
    cgpa: Annotated[float, Field(..., gt=0, lt=10)]
    semester: Annotated[int, Field(..., gt=0, lt=10)]
    married: Annotated[bool, Field(...)]
    gender: Annotated[Literal["male", "female", "others"], Field(...)]
    linkedin: Annotated[AnyUrl, Field(...)]

    @field_validator("roll_num")
    @classmethod
    def validate_roll_num(cls, value):
        valid_branches = ["UEC","UME","UCS","DEC","DCS","UCC","PEC","PCS"]
        if len(value) != 8 or not value[:2].isdigit() or value[2:5] not in valid_branches or not value[5:8].isdigit():
            raise ValueError("Invalid roll number")
        return value
    
class StudentUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=15, lt=28)]
    cgpa: Annotated[Optional[float], Field(default=None, gt=0, lt=10)]
    semester: Annotated[Optional[int], Field(default=None, gt=0, lt=10)]
    married: Annotated[Optional[bool], Field(default=None)]
    gender: Annotated[Optional[Literal["male","female","others"]], Field(default=None)]
    linkedin: Annotated[Optional[AnyUrl], Field(default=None)]

class StudentOut(BaseModel):
    id: int
    roll_num: str
    name: str
    age: int
    cgpa: float
    semester: int
    married: bool
    gender: str
    linkedin: str

    @computed_field
    @property
    def year(self) -> int:
        return int(self.roll_num[:2])
    
    @computed_field
    @property
    def branch(self) -> str:
        programs = {
            "UEC":"Bachelors of Electronics and Communication Engineering",
            "UME":"Bachelors of Mechanical Engineering",
            "UCS":"Bachelors of Computer Science Engineering",
            "DEC":"Bachelors and Masters of Electronics and Communication",
            "DCS":"Bachelors and Masters of Computer Science Engineering",
            "UCC":"Bachelors of Computer and Communication Engineering",
            "PEC":"Doctorate of Electronics and Communication",
            "PCS":"Doctorate of Computer Science Engineering",
        }

        return programs[self.roll_num[2:5]]
    
    @computed_field
    @property
    def email(self) -> str:
        return f"{self.roll_num}@lnmiit.ac.in"
       
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: Annotated[str,Field(...,description = "username of the user",min_length = 3)]
    password: Annotated[str,Field(...,description = "password of the user",min_length = 6)]

class MarksCreate(BaseModel):
    subject: Annotated[str, Field(...)]
    marks_obtained: Annotated[int, Field(..., ge = 0)]
    maximum_marks: Annotated[int,Field(...,gt = 0)]

class MarksOut(BaseModel):
    id: int
    subject: str
    marks_obtained: int
    maximum_marks: int

    class Config:
        from_attributes = True