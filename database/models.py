from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy_utils import database_exists, create_database

from sqlalchemy.orm import declarative_base, Session, sessionmaker
from sqlalchemy import Column, Integer, String, TypeDecorator
import pandas as pd

class HexByteString(TypeDecorator):
    """  
        Class to store model weights in postgress
    """

    impl = String

    def process_bind_param(self, value, dialect):
        if not isinstance(value, bytes):
            raise TypeError("HexByteString columns support only bytes values.")
        return value.hex()

    def process_result_value(self, value, dialect):
        return bytes.fromhex(value) if value else None

import json
from typing import Dict, Any, List
# from functools import lru_cache
import pickle
from io import BytesIO


Base = declarative_base()
class ModelSignature(Base):
    """
        ORM for model's signatures
    """
    __tablename__ = "model_signature"

    model_type = Column(String, primary_key=True)
    fit_params_json = Column(String)
    python_library_path = Column(String)
    
    def __repr__(self):
        return "{model_type=%s, fit_params_json=%s, python_library_path=%s}"%(self.model_type, 
                                                      self.fit_params_json, self.python_library_path
                                                     )
    
    def _to_json(self):
        return {"model_type": self.model_type,
                "fit_params_json": json.loads(self.fit_params_json),
                "python_library_path": self.python_library_path
               }

class ModelInstance(Base):
    """
        ORM for model's instances
    """
    __tablename__ = "model_instance"

    model_name = Column(String, primary_key=True)
    model_type = Column(String)
    fit_params_json = Column(String)
    python_library_path = Column(String)
    model_bin = Column(HexByteString)
    features  = Column(String)
    target_column = Column(String)
    
    def __repr__(self):
        return f"model_name={self.model_name}\n" + \
               f"model_type={self.model_type}" + \
               f"fit_params_json={self.fit_params_json}" + \
               f"python_library_path={self.python_library_path}"
    
    def _to_json(self):
        return {"model_name": self.model_name,
                "model_type": self.model_type,
                "fit_params_json": json.loads(self.fit_params_json),
                "python_library_path": self.python_library_path,
                "features": json.loads(self.features),
                "target_column": self.target_column
               }
    
    def _get_features(self):
        open("xyu.txt", 'w+').write(self.features)
        return json.loads(self.features)
    
    def fit(self, 
            data: pd.DataFrame, 
            target_column: str = 'y'
           ) -> None:
        model_class = self._import_sklearn_model_class()
        fit_params = json.loads(self.fit_params_json)
        model = model_class(**fit_params)
        
        self.target_column = target_column

        features = list(data.keys())
        features.remove(target_column)
        self.features = json.dumps(features)
        
        model.fit(X = data[self._get_features()], 
                  y = data[self.target_column]
                 )
        
        self.model_bin = ModelInstance._model_to_buff(model)
        
    def predict(self, data: pd.DataFrame) -> Dict[Any, Any]:
        model = self._get_model()
        data['predict'] = model.predict(X = data[self._get_features()])
        return data['predict'].to_list()
    
    def _import_sklearn_model_class(self):
        """
            Интроспекция для загрузки модуля sklearn
        """
        from_str = '.'.join(self.python_library_path.split('.')[:2])
        res = __import__(from_str)
        res = getattr(res, self.python_library_path.split('.')[1])
        res = getattr(res, self.python_library_path.split('.')[2])
        return res
    
    @classmethod
    def _model_to_buff(cls, model_python) -> bytes:
        buffer = BytesIO()
        pickle.dump(model_python, buffer)
        buffer.seek(0)
        return buffer.read()
    
    @classmethod
    def _buff_to_model(csl, model_bin) -> Any:
        model_python = pickle.loads(model_bin)
        return model_python

    def _get_model(self) -> Any:
        return ModelInstance._buff_to_model(self.model_bin)
    

    if __name__ == "__main__":
        pass
        #ToDo: create database if those code run at first time