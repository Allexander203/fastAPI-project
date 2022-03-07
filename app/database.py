#import here or adbove for connecting to database manually.
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    #connecting to database
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastAPI', 
#         user='postgres', password='123456789', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("db connection was successfull")
#         break
#     except Exception as error:
#         print("connecting to db failed")
#         print("Error:",error)
#         TIMESTAMP.sleep(2)



