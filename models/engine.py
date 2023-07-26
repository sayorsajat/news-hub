import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.news_model import NewsTable, Base

load_dotenv()

# PostgreSQL connection details
postgres_host = os.getenv("postgres_host")
postgres_port = os.getenv("postgres_port")
dbname = os.getenv("dbname")
user_name = os.getenv("user_name")
user_pass = os.getenv("user_pass")

# Create the SQLAlchemy engine and session
engine = create_engine(f'postgresql://{user_name}:{user_pass}@{postgres_host}:{postgres_port}/{dbname}')
Session = sessionmaker(bind=engine)

# Create the table if it doesn't already exist
Base.metadata.create_all(engine)