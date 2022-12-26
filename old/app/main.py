from fastapi import FastAPI, Request
from fastapi import Form, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

import pandas as pd
import pickle
import os
# import sklearn

from create_datasets import create_train_datasets
from utils import str_to_base64, base64_to_str
from utils import get_list_of_datasets, get_list_of_models

from constant import folder_dataset, folder_model
import aiofiles
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    datasets = get_list_of_datasets(folder_dataset)
    models = get_list_of_models(folder_model)
    model_list = list(json.load(open("models_configs.json", 'r')).keys())
    context = {
        "datasets": datasets,
        "models": models,
        "model_list": model_list,
        "request": request
    }
    return templates.TemplateResponse("index.html",
                                      context
                                      )


@app.get("/dataset/", response_class=HTMLResponse)
async def view_datasets(request: Request, file_id: str):
    fn = base64_to_str(file_id)
    data = pd.read_csv(fn)
    html = str(data.to_html(classes=["table-bordered", "table-striped", "table-hover"]))
    context = {"html":  html,
               "request": request
               }
    
    return templates.TemplateResponse("dataset_table.html",
                                      context)


def import_sklearn_model_class(model_type):
    """
        Интроспекция для загрузки модуля sklearn
    """
    from_str = '.'.join(model_type.split('.')[:2])
    res = __import__(from_str)
    res = getattr(res, model_type.split('.')[1])
    res = getattr(res, model_type.split('.')[2])
    return res


def load_dataset(fn):
    data = pd.read_csv(fn)
    return data 


def get_model_fn(model_name):
    """
        Получить путь к модели
    """
    return os.path.join(folder_model, model_name) + '.pickle'


def get_config_fn(model_name):
    """
        Получить путь к конфигу
    """
    return os.path.join(folder_model, model_name) + '.json'


@app.post("/fit")
async def create_model(request: Request,
                       fn_train=Form(),
                       model_type=Form(),
                       column_target=Form(),
                       model_name=Form(),
                       init_fit_intercept=Form(None),
                       init_normalize=Form(None),
                       init_copy_X=Form(None),
                       init_n_jobs=Form(None),
                       init_positive=Form(None),
                       init_dual=Form(None),
                       init_tol=Form(None),
                       init_C=Form(None),
                       init_intercept_scaling=Form(None),
                       init_class_weight=Form(None),
                       init_random_state=Form(None),
                       init_solver=Form(None),
                       init_max_iter=Form(None),
                       init_multi_class=Form(None),
                       init_verbose=Form(None),
                       init_warm_start=Form(None),
                       init_l1_ratio=Form(None),
                       init_criterion=Form(None),
                       init_max_depth=Form(None),
                       init_min_samples_split=Form(None),
                       init_min_samples_leaf=Form(None),
                       init_min_weight_fraction_leaf=Form(None),
                       init_max_features=Form(None),
                       init_max_leaf_nodes=Form(None),
                       init_min_impurity_decrease=Form(None),
                       init_bootstrap=Form(None),
                       init_oob_score=Form(None),
                       init_ccp_alpha=Form(None),
                       init_max_samples=Form(None),
                       init_loss=Form(None),
                       init_learning_rate=Form(None),
                       init_n_estimators=Form(None),
                       init_subsample=Form(None),
                       init_init=Form(None),
                       init_validation_fraction=Form(None),
                       init_n_iter_no_change=Form(None),
                       init_alpha=Form(None)
    ):
    """
        Обучение модели
        Единственный способ передать параметры без Ajax, это так
        Я не знала когда начинала, 
        потом было поздно останавливаться :(
        https://stackoverflow.com/questions/22195065/how-to-send-a-json-object-using-html-form-data
    """
    list_of_possible_parametres = [("fit_intercept", init_fit_intercept),
                                   ("normalize", init_normalize),
                                   ("copy_X", init_copy_X),
                                   ("n_jobs", init_n_jobs),
                                   ("positive", init_positive),
                                   ("dual", init_dual),
                                   ("tol", init_tol),
                                   ("C", init_C),
                                   ("intercept_scaling", init_intercept_scaling),
                                   ("class_weight", init_class_weight),
                                   ("random_state", init_random_state),
                                   ("solver", init_solver),
                                   ("max_iter", init_max_iter),
                                   ("multi_class", init_multi_class),
                                   ("verbose", init_verbose),
                                   ("warm_start", init_warm_start),
                                   ("l1_ratio", init_l1_ratio),
                                   ("criterion", init_criterion),
                                   ("max_depth", init_max_depth),
                                   ("min_samples_split", init_min_samples_split),
                                   ("min_samples_leaf", init_min_samples_leaf),
                                   ("min_weight_fraction_leaf", init_min_weight_fraction_leaf),
                                   ("max_features", init_max_features),
                                   ("max_leaf_nodes", init_max_leaf_nodes),
                                   ("min_impurity_decrease", init_min_impurity_decrease),
                                   ("bootstrap", init_bootstrap),
                                   ("oob_score", init_oob_score),
                                   ("ccp_alpha", init_ccp_alpha),
                                   ("max_samples", init_max_samples),
                                   ("loss", init_loss),
                                   ("learning_rate", init_learning_rate),
                                   ("n_estimators", init_n_estimators),
                                   ("subsample", init_subsample),
                                   ("init", init_init),
                                   ("validation_fraction", init_validation_fraction),
                                   ("n_iter_no_change", init_n_iter_no_change),
                                   ("alpha", init_alpha)
                                   ]

    # Загружаю dataset
    data = load_dataset(fn_train)
    
    # Загружаю класс модели
    model_class = import_sklearn_model_class(model_type)

    # Создаю колонку с признаками
    columns_features = list(data.keys())
    columns_features.remove(column_target)

    # Обучаю модель
    init_parametres = json.load(open("models_configs.json", 'r'))
    init_parametres = init_parametres[model_type.split('.')[-1]]["init"]
    for k, v in list_of_possible_parametres:
        if v is not None and k in init_parametres:
            init_parametres[k] = v

    model = model_class(**init_parametres)
    model.fit(X=data[columns_features],
              y=data[column_target]
              )

    # Сохраняю модель и гиперпараметры
    fn_model = get_model_fn(model_name)
    pickle.dump(model, open(fn_model, 'wb'))

    fn_config = get_config_fn(model_name)
    model_config = init_parametres
    model_config["fn_train"] = fn_train,
    model_config["model_type"] = model_type,
    model_config["column_target"] = column_target

    model_config['columns_features'] = columns_features
    json.dump(model_config, open(fn_config, 'w'))
    return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)


@app.get("/update_datasets", 
         response_class=RedirectResponse
         )
async def update_datasets(request: Request):
    create_train_datasets()
    return "/"


@app.get("/delete_dataset", 
         response_class=RedirectResponse
         )
async def delete_dataset(request: Request, file_id: str):
    fn = base64_to_str(file_id)
    os.remove(fn)
    return "/"


@app.get("/delete_model", 
         response_class=RedirectResponse
         )
async def delete_model(request: Request, model_name: str):
    filename = base64_to_str(model_name)
    os.remove(os.path.join(folder_model, filename + '.json'))
    os.remove(os.path.join(folder_model, filename + '.pickle'))
    return "/"


@app.get("/models", 
         response_class=RedirectResponse
         )
async def view_datasets(request: Request, model_id: str):
    filename = base64_to_str(model_id)
    fn = os.path.join(folder_model, filename + '.json')
    dct = json.load(open(fn, 'r'))
    data = pd.Series({k: str(v) for k, v in dct.items()}).to_frame('value')
    data.index.name = 'name'
    data = data.reset_index()

    html = str(data.to_html(classes=["table-bordered", "table-striped", "table-hover"]))
    context = {"html":  html,
               "request": request
               }

    return templates.TemplateResponse("dataset_table.html",
                                      context
                                      )


@app.get("/add_model", 
         response_class=RedirectResponse
         )
async def add_model(request: Request,
                    model_name: str
                    ):
    
    model_config = json.load(open("models_configs.json", 'r'))
    model_config = model_config[model_name]
    datasets = get_list_of_datasets(folder_dataset)

    context = {"model_name": model_name,
               "model_config":  model_config,
               "request": request,
               "datasets": datasets
               }

    return templates.TemplateResponse("add_model.html",
                                      context)


@app.post("/add_dataset")
async def add_dataset(request: Request,
                      fn=Form(),
                      data: UploadFile = File()
                      ):
    if not fn.endswith(".csv"):
        return {"result": "fail"}
    fn = os.path.join(folder_dataset, "user", fn)
    async with aiofiles.open(fn, 'wb') as out_file:
        content = await data.read()  # async read
        await out_file.write(content)  # async write

    return {"result": "OK"}


@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request,
                  model_name=Form(),
                  fn_input=Form(),
                  fn_output=Form(),
                  ):
    """
        Инференс модели
    """

    # Загружаю dataset
    data = load_dataset(fn_input)
    
    # Загружаем модель
    fn_model = get_model_fn(model_name)
    model = pickle.load(open(fn_model, 'rb'))

    # Загружаем конфиг
    fn_config = get_config_fn(model_name)
    config = json.load(open(fn_config, 'r'))
    columns_features = config['columns_features']

    # Делаем предсказание
    data['predict'] = model.predict(data[columns_features])

    # Сохраняем результаты
    data.to_csv(fn_output)

    html = str(data.to_html(classes=["table-bordered", "table-striped", "table-hover"]))
    context = {"html":  html,
               "request": request
               }

    return templates.TemplateResponse("dataset_table.html",
                                      context)
