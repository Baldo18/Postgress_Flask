from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import os

db_url = os.environ.get('SQLALCHEMY_DATABASE_URI')
# Database connection and session setup
engine = create_engine(db_url)
db_session = scoped_session(sessionmaker(bind=engine))

# Declarative base
Database = declarative_base()

# Table creation function
def init_db():
    Database.metadata.create_all(bind=engine)
