"""
Need for effective session creation
Based on this 
https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
import json
from pathlib import Path

def get_engine():
    postgress_host = os.environ.get("postgress_host")
    postgress_password = os.environ.get("postgress_password")
    postgress_user = os.environ.get("postgress_user")
    postgress_db = os.environ.get("postgress_db")
    database_uri = f'postgresql+psycopg2://{postgress_user}:'+\
                    f'{postgress_password}@{postgress_host}/'+ \
                    f'{postgress_db}'


    engine = create_engine(database_uri)
    return engine

def get_session_local():
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

SessionLocal = get_session_local()

def init_db(engine, fn_json = ".model_signature.json"):
    """
        First inisialization of database at first run
    """
    fn_json =  Path(__file__).parent / "model_signature.json"
        
    # This is not cool, but it is more optimal to place here
    import models
    from models import ModelSignature
    
    models.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    model_signatures_json = json.load(open(fn_json, 'r'))
    for dct in model_signatures_json:
        model_type = dct['model_type']
        fit_params_json = json.dumps(dct['fit_params_json'])
        python_library_path = dct['python_library_path']
        model_signature = ModelSignature(model_type = model_type, 
                                         fit_params_json = fit_params_json,
                                         python_library_path = python_library_path
                                        )
        session.add(model_signature)
    
    session.commit()
    return

def get_db() -> Generator:
    """
        Get session for fast api
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

if __name__ == "__main__":
    engine = get_engine()
    init_db(engine)


