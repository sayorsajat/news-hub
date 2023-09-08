from lib.constants import table_name
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

# Define a SQLAlchemy model
Base = declarative_base()


# Define a SQLAlchemy table
class NewsTable(Base):
    __tablename__ = table_name

    id = Column(Integer, primary_key=True)
    type = Column(String)
    title = Column(String)
    descriptionUrl = Column(String, unique=True)
    content = Column(String)
    language = Column(String)
    source = Column(String)
    created_at = Column(DateTime, default=func.now())
