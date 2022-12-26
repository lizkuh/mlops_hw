import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import Depends

from typing import Union, List, Dict, Any
import os

from database.models import ModelInstance, ModelSignature
from database.session import get_db
from sqlalchemy.orm import Session
from utils import __json_to_dataframe
from utils import WrongInputData, WrongFitParams, WrongModelType, WrongModelName

app = FastAPI()

## See al errors at the output
@app.exception_handler(Exception)
async def validation_exception_handler(request, err):
    return JSONResponse(status_code = getattr(err, "status_code", 400),
                        content={"error": str(err),
                                 "type": str(type(err)) 
                                }
                       )


@app.post("/fit_model")
def fit_model(model_type: str,
              model_name: str,
              input_data_json: str,
              fit_params_json: Union[str, None],
              target_column: str = 'y',
              session: Session = Depends(get_db)
             ) -> None:
    """
    Fit model_type on input_data_json with fit_params_json hyperparametres
    and save fitted model at models.models_instances


    Parameters
    ----------
    model_type : str 
        model type (list of possible model types are in models.models_signature)
    model_name : str
        unique model name 
        If model already exists, there would be an errror (try /refit_model or /delete, /fit).

    input_data_json : str
        train dataset in json format

    fit_params_json : str
        model hyperparametres (changeble only parametres from models.models_signature)


    Return
    --------
        status of operation
    """
    if session.query(ModelInstance).get(model_name) is not None:
        raise WrongModelName(f"model_name={model_name} already exist")
       
    if session.query(ModelSignature).get(model_type) is None:
        raise WrongModelName(f"model_type={model_type} is not exist")
    
    data  = __json_to_dataframe(input_data_json)
    if not target_column in data:
        raise WrongInputData(f'There are no "{target_column}" at input_data_json')
    
    model_signature = session.query(ModelSignature).get(model_type)
    python_library_path   = model_signature.python_library_path

    model_instance = ModelInstance(model_name  = model_name,
                                model_type  = model_type,
                                fit_params_json = fit_params_json,
                                python_library_path = python_library_path,
                                )

    model_instance.fit(data = data, target_column = "y")
    session.add(model_instance)
    session.commit()

    return


@app.post("/refit_model")
def refit_model(model_name: str,
                input_data_json: str,
                session: Session = Depends(get_db)
               ) -> None:
    """
    Fefit model_name on input_data_json

    Parameters
    ----------
    model_name : str
        model name, that should be already added into database
        
    input_data_json : str
        train dataset in json format

    Return
    --------
        status of operation
    """
    data  = __json_to_dataframe(input_data_json)
    model_instance = session.query(ModelInstance).get(model_name)
    if model_instance is None:
        raise WrongModelName(f"model_name={model_name} is not exist")
    
    model_instance.fit(data = data, target_column = "y")
    session.add(model_instance)
    session.commit()
    return


@app.post("/predict_model")
def predict_model(model_name: str, 
                  input_data_json: str,
                  session: Session = Depends(get_db)
                ) -> List[int]:
    """
    Delete model_name

    Parameters
    ----------
    model_name : str
        model name, that should be already added into database

    input_data_json : str
        test dataset in json format

    Return
    --------
        List of predicted classes
    """
    model_instance = session.query(ModelInstance).get(model_name)
    if model_instance is None:
        raise WrongModelName(f"model_name={model_name} is not exist")
        
    data  = __json_to_dataframe(input_data_json)
    pred_list = model_instance.predict(data)
    return pred_list


@app.post("/delete_model")
def delete_model(model_name: str, session: Session = Depends(get_db)) -> None:
    """
    Delete model_name

    Parameters
    ----------
    model_name : str
        model name, that should be already added into database

    Return
    --------
        status of operation
    """
    if not session.query(ModelInstance).get(model_name):
        raise WrongModelName(f"model_name={model_name} is not exist")
    else:
        session.query(ModelInstance).filter_by(model_name = model_name).delete()
        session.commit() 


@app.get("/get_model_types")
def get_model_types(session: Session = Depends(get_db)) -> List[Dict[Any, Any]]:
    """
    Get all possible model types

    Return
    --------
        List of possible model types with all possible hyperparametres
    """
    res = [line._to_json() for line in session.query(ModelSignature).all()]

    return res


@app.get("/get_model_instances")
def get_model_instances(session: Session = Depends(get_db)) -> List[Dict[Any, Any]]:
    """
    Get all model instances

    Return
    --------
        List of model instances with all of their hyperparametres
    """
    res = [line._to_json() for line in session.query(ModelInstance).all()]

    return res


if __name__ == "__main__":
    # ToDo: delete 
    fastapi_host = os.environ.get("fastapi_host")
    fastapi_port = os.environ.get("fastapi_port")


    uvicorn.run(app, host = fastapi_host, port = fastapi_port)

