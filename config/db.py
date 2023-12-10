from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from config.const_db import URL_DB

engine = create_engine(URL_DB)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()