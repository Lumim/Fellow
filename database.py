from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL Database URL format: mysql+pymysql://<username>:<password>@<host>/<dbname>

#DATABASE_URL = "mysql+pymysql://root:@localhost:3306/fellow_1"
DATABASE_URL = "mysql+pymysql://u767919379_rootxtech:Fello2024x@195.35.59.19:3306/u767919379_xtech"



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
