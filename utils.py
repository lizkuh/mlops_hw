import pandas as pd
from typing import List, Dict, Any
from pydoc import locate
from database.models import ModelSignature

class WrongFitParams(Exception):
    """
        Model's hyperparametres are wrong
    """
    status_code = 400
    pass


class WrongModelType(Exception):
    """
        Model type unexist
    """
    status_code = 409
    pass

class WrongModelName(Exception):
    """
        These model instance already exist
    """
    status_code = 409
    pass

class WrongInputData(Exception):
    """
        Error at input_data_json
    """
    status_code = 400
    pass

def __json_to_dataframe(json_input: List[Dict[Any, Any]]) -> pd.DataFrame:
    """
        Change input json to pd.DataFrame
    """
    try:
        data = pd.read_json(json_input)
        #ToDo: Check that types are not objects or string
        # These will cause error with hight probability
        return data
    except Exception as e:
        raise WrongInputData(e)

def check_fit_params_json(model_signature: ModelSignature,
                          input_json: Dict[str, Any]) -> None:
    """
        Check that input types are valid
    """
        
    json_shema = model_signature._to_json()['fit_params_json']
    
    for key, value in input_json.items():
        if key not in json_shema:
            raise WrongFitParams(f"Unknown params {key}")

        valid_type = json_shema[key]
        if not isinstance(value, locate(valid_type)):
            raise WrongFitParams(f"{key} = {value} that is not valid type " + \
                                 f"(valid_type is {valid_type}, these type is {str(type(value))}")
    return