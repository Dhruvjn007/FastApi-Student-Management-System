from database import SessionLocal
from models import Student

db = SessionLocal()

new_student1 = Student( 
    roll_num="23UCS101", 
    name="Test Kumar", 
    age=20, cgpa=8.5, 
    semester=4, 
    married=False, 
    gender="male", 
    linkedin="https://linkedin.com/in/testkumar" 
)

new_student2 = Student(
    roll_num="23UCS102",
    name="Aarav Sharma",
    age=19,
    cgpa=8.1,
    semester=3,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/aaravsharma"
)

new_student3 = Student(
    roll_num="23UCS103",
    name="Priya Verma",
    age=20,
    cgpa=9.2,
    semester=4,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/priyaverma"
)

new_student4 = Student(
    roll_num="23UCS104",
    name="Rohan Gupta",
    age=21,
    cgpa=7.8,
    semester=5,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/rohangupta"
)

new_student5 = Student(
    roll_num="23UCS105",
    name="Sneha Patel",
    age=20,
    cgpa=8.9,
    semester=4,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/snehapatel"
)

new_student6 = Student(
    roll_num="23UCS106",
    name="Aditya Singh",
    age=22,
    cgpa=7.3,
    semester=6,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/adityasingh"
)

new_student7 = Student(
    roll_num="23UCS107",
    name="Neha Joshi",
    age=19,
    cgpa=9.0,
    semester=3,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/nehajoshi"
)

new_student8 = Student(
    roll_num="23UCS108",
    name="Karan Mehta",
    age=21,
    cgpa=8.0,
    semester=5,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/karanmehta"
)

new_student9 = Student(
    roll_num="23UCS109",
    name="Ananya Roy",
    age=20,
    cgpa=9.4,
    semester=4,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/ananyaroy"
)

new_student10 = Student(
    roll_num="23UCS110",
    name="Vikram Nair",
    age=22,
    cgpa=6.9,
    semester=6,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/vikramnair"
)

new_student11 = Student(
    roll_num="23UCS111",
    name="Ishita Kapoor",
    age=20,
    cgpa=8.7,
    semester=4,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/ishitakapoor"
)

new_student12 = Student(
    roll_num="23UCS112",
    name="Rahul Yadav",
    age=21,
    cgpa=7.6,
    semester=5,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/rahulyadav"
)

new_student13 = Student(
    roll_num="23UCS113",
    name="Meera Iyer",
    age=19,
    cgpa=9.6,
    semester=3,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/meeraiyer"
)

new_student14 = Student(
    roll_num="23UCS114",
    name="Arjun Malhotra",
    age=22,
    cgpa=7.4,
    semester=6,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/arjunmalhotra"
)

new_student15 = Student(
    roll_num="23UCS115",
    name="Pooja Chawla",
    age=20,
    cgpa=8.3,
    semester=4,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/poojachawla"
)

new_student16 = Student(
    roll_num="23UCS116",
    name="Siddharth Rao",
    age=21,
    cgpa=8.8,
    semester=5,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/siddharthrao"
)

new_student17 = Student(
    roll_num="23UCS117",
    name="Kavya Menon",
    age=19,
    cgpa=9.1,
    semester=3,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/kavyamenon"
)

new_student18 = Student(
    roll_num="23UCS118",
    name="Harsh Agarwal",
    age=20,
    cgpa=7.9,
    semester=4,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/harshagarwal"
)

new_student19 = Student(
    roll_num="23UCS119",
    name="Diya Khanna",
    age=21,
    cgpa=8.6,
    semester=5,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/diyakhanna"
)

new_student20 = Student(
    roll_num="23UCS120",
    name="Manish Bansal",
    age=22,
    cgpa=7.1,
    semester=6,
    married=False,
    gender="male",
    linkedin="https://linkedin.com/in/manishbansal"
)

new_student21 = Student(
    roll_num="23UCS121",
    name="Riya Sinha",
    age=20,
    cgpa=9.3,
    semester=4,
    married=False,
    gender="female",
    linkedin="https://linkedin.com/in/riyasinha"
)

new_students = [
    new_student2,
    new_student3,
    new_student4,
    new_student5,
    new_student6,
    new_student7,
    new_student8,
    new_student9,
    new_student10,
    new_student11,
    new_student12,
    new_student13,
    new_student14,
    new_student15,
    new_student16,
    new_student17,
    new_student18,
    new_student19,
    new_student20,
    new_student21,
]
for new_student in new_students:
    db.add(new_student)
db.commit()

for new_student in new_students:
    print("student inserted with id",new_student.id)
db.close()
