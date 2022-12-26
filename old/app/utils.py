import base64
import os
import json


def str_to_base64(s: str) -> str:
    message_bytes = s.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_bytes = base64_bytes.decode('UTF-8')
    return base64_bytes


def base64_to_str(s: str) -> str:
    base64_bytes = s.encode("ascii")

    base64_bytes = base64.b64decode(base64_bytes)
    res = base64_bytes.decode("ascii")
    return res


def get_list_of_datasets(folder_dataset):
    res = []
    for name in os.listdir(folder_dataset):
        path = os.path.join(folder_dataset, name)
        if os.path.isdir(path):
            for _fn in os.listdir(path):
                fn = os.path.join(path, _fn)
                res.append({"name": name,
                            "folder": path,
                            "fn": fn,
                            "score": 1,
                            "file_id": str_to_base64(fn)
                            }
                           )
    return res


def get_list_of_models(folder_model):
    res = {}
    for name in os.listdir(folder_model):
        fn = os.path.join(folder_model, name)
        print(fn)
        model_name = name.split('.')[0]
        if model_name not in res:
            res[model_name] = {"model_name": model_name}
            res[model_name]['model_id'] = str_to_base64(model_name)
        if fn.endswith('.pickle'):
            res[model_name]['fn_model'] = os.path.join(folder_model, fn)
        else:
            res[model_name]['fn_config'] = os.path.join(folder_model, fn)
            print(fn)
            res[model_name]['config'] = str(json.load(open(fn, 'r')))
                
    return list(res.values())
