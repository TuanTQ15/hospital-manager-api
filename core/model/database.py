from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DATABASE_URL = os.environ["uri_db"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_engine():
    return engine

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
