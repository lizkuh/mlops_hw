"""
Need for effective session creation
Based on this 
https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
meta = MetaData()

# ToDo: delete variant without get env
postgress_host = os.environ.get("postgress_host", "0.0.0.0")
postgress_password = os.environ.get("postgress_password", "password")
postgress_user = os.environ.get("postgress_user", "postgres")
postgress_db = os.environ.get("postgress_db", "test")
database_uri = f'postgresql+psycopg2://{postgress_user}:'+\
                f'{postgress_password}@{postgress_host}/'+ \
                f'{postgress_db}'
                   
engine = create_engine(
    database_uri,
    # required for sqlite
    # connect_args={"check_same_thread": False},
)

from models import ModelInstance, ModelSignature
meta.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
ModelInstance, ModelSignature

def get_db() -> Generator:
    db = SessionLocal()  # 2
    try:
        yield db  # 3
    finally:
        db.close()  # 4