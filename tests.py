import pandas as pd 
import requests
import json
import pytest
import os

fastapi_host = os.environ.get("fastapi_host", "0.0.0.0")
fastapi_port = os.environ.get("fastapi_port", "8000")
dataset_test = os.environ.get("dataset_test", "database/data.csv")
input_data = pd.read_csv(dataset_test).to_json()
host =  f"http://{fastapi_host}:{fastapi_port}}"

def test_get_model_types():
    """
        Test get_model_types
    """
    url = f"{host}/get_model_types"

    json_etalon = json.load(open("database/model_signature.json", 'r'))
    json_host = requests.get(url).json()
    assert json_etalon == json_host
    

def test_get_model_instances():
    url = f"{host}/get_model_instances"
    list_of_models = requests.get(url).json()
    
    etalon_list_model = [{'model_name': 'test_real90',
                          'model_type': 'RandomForestClassifier',
                          'fit_params_json': {},
                          'python_library_path': 'sklearn.ensemble.RandomForestClassifier',
                          'features': ['0', '1', '2', '3'],
                          'target_column': 'y'
                         },
                         {'model_name': 'test_real',
                          'model_type': 'RandomForestClassifier',
                          'fit_params_json': {},
                          'python_library_path': 'sklearn.ensemble.RandomForestClassifier',
                          'features': ['0', '1', '2', '3'],
                          'target_column': 'y'
                         }
                        ]
    assert etalon_list_model == list_of_models

@pytest.mark.parametrize("status_code", [200, 409])
def test_fit_model(status_code):
    url = f"{host}/fit_model"
    data = {"model_type": "RandomForestClassifier",
            "model_name": "test_RF0",
            "input_data_json": input_data,
            "fit_params_json": "{}",
            "target_column": "y"
           }

    resp = requests.post(url, params = data)
    assert resp.status_code == status_code

def test_refit_model():
    url = f"{host}/refit_model"
    data = {"model_name": "test_RF0",
            "input_data_json": input_data,
           }

    resp = requests.post(url, params = data)
    assert resp.status_code == 200

def test_predict_model():
    url = f"{host}/predict_model"
    data = {"model_name": "test_RF0",
            "input_data_json": input_data,
           }

    resp = requests.post(url, params = data)
    return resp == ([0] * 50) + ( [1] * 50 ) + ( [2] * 50 )

def test_delete_model():
    url = f"{host}/delete_model"
    data = {"model_name": "test_RF0",
           }

    resp = requests.post(url, params = data)
    assert resp.status_code == 200

