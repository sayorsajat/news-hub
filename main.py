import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from lib.constants import table_name, URLs
from lib.collect_titles import collect_titles_dynamic
from time import sleep

load_dotenv()

# Configure the PostgreSQL connection details
postgres_host = os.getenv("postgres_host")
postgres_port = os.getenv("postgres_port")
dbname = os.getenv("dbname")
user_name = os.getenv("user_name")
user_pass = os.getenv("user_pass")

# Create the SQLAlchemy engine and session
engine = create_engine(f'postgresql://{user_name}:{user_pass}@{postgres_host}:{postgres_port}/{dbname}')
Session = sessionmaker(bind=engine)
session = Session()

# Define a SQLAlchemy model
Base = declarative_base()

class NewsTable(Base):
    __tablename__ =  table_name

    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    descriptionUrl = Column(String)
    content = Column(String)
    language = Column(String)
    source = Column(String)

# Create the table if it doesn't already exist
Base.metadata.create_all(engine)

for url in URLs:
    collect_titles_dynamic(session, NewsTable, url)
    sleep(0.5)

session.close()