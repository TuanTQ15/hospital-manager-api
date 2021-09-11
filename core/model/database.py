from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

userRemote = 'yobbtyvsphftgn'
passwordRemote = "d5611dbc897053e01868bd1d379e3aa55093bfb1d831d2dfd6092d1fdcd3f914"
hostRemote = 'ec2-44-194-225-27.compute-1.amazonaws.com'
port = '5432'
dbNameRemote = 'dbvb9pgec703ho'
driverName = 'postgresql://'
DATABASE_URL = driverName + userRemote + ':' + passwordRemote + "@" + hostRemote + ':' + port + '/' + dbNameRemote

userLocal = 'postgres'
passwordLocal = "postgres"
hostLocal = '6.tcp.ngrok.io'
port = '14185'
dbNameLocal = 'benhvien'
driverName = 'postgresql://'
DATABASE_URL_LOCAL = driverName + userLocal + ':' + passwordLocal + "@" + hostLocal + ':' + port + '/' + dbNameLocal


engine = create_engine(DATABASE_URL_LOCAL)
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