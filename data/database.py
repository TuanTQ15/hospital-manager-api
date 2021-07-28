from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

user = 'yobbtyvsphftgn'
password = "d5611dbc897053e01868bd1d379e3aa55093bfb1d831d2dfd6092d1fdcd3f914"
host = 'ec2-44-194-225-27.compute-1.amazonaws.com'
port = '5432'
dbName = 'dbvb9pgec703ho'
driverName = 'postgresql://'
DATABASE_URL = driverName + user + ':' + password + "@" + host + ':' + port + '/' + dbName
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
