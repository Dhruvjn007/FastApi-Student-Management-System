from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.orm import declarative_base,sessionmaker,Session
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="config.env")

password = quote_plus(os.getenv("DB_PASSWORD"))

DATABASE_URL = f"postgresql+psycopg2://postgres:{password}@localhost:5432/student_db"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = sessionmaker(bind = engine)

if __name__=="__main__":
    try:
        with engine.connect() as connection:
            print("connection successful")
    except Exception as e:
        print("connection failed",e) 