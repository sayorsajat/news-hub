import csv
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from lib.constants import table_name, delay_of_fetching_titles, delay_of_fetching_content_between_same_source
from lib.collect_titles import collect_titles_dynamic
from lib.collect_description import collect_description_dynamic
from time import sleep

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
session = Session()

# Define a SQLAlchemy model
Base = declarative_base()

# Define a SQLAlchemy table
class NewsTable(Base):
    __tablename__ =  table_name

    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    descriptionUrl = Column(String, unique=True)
    content = Column(String)
    language = Column(String)
    source = Column(String)

# Create the table if it doesn't already exist
Base.metadata.create_all(engine)

while True:
    with open("./lib/news_sources.csv", 'r') as file:
        csv_file = csv.DictReader(file, delimiter=';')
        websites_list = []
        for row in csv_file:
            if row["is_description_availaible"] == "yes":
                websites_list.append(row["website"])
            collect_titles_dynamic(session, NewsTable, row["website"])
            sleep(delay_of_fetching_titles)
        

        # Basically, while there are news without content value
        while session.query(NewsTable).filter(NewsTable.content.is_(None), NewsTable.source.in_(websites_list)).all():
            for website in websites_list:
                row = session.query(NewsTable).filter(NewsTable.content.is_(None), NewsTable.source.is_(website)).first()
                if row:
                    collect_description_dynamic(session, NewsTable, row.descriptionUrl, row.id)
                    sleep(delay_of_fetching_content_between_same_source/len(websites_list))

        file.close()
        

    session.close()