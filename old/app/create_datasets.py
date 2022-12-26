import os
import pandas as pd
from sklearn.datasets import load_digits, load_iris, load_boston,\
                             load_breast_cancer, load_diabetes, load_wine
from sklearn.model_selection import train_test_split
from constant import folder_dataset


def create_train_datasets():
    """
        Созраняет обучающие выборки в папку
    """
    print("create_train_datasets")
    os.makedirs(folder_dataset, exist_ok=True)

    datasets = [(load_digits, "digits"),
                (load_iris, "iris"),
                (load_boston, "boston"),
                (load_breast_cancer, "breast_cancer"),
                (load_diabetes, "diabetes"),
                (load_wine, "wine")
                ]

    for loader, name in datasets:
        print(name)
        folder = os.path.join(folder_dataset, name)
        os.makedirs(folder, exist_ok=True)

        X, y = loader(return_X_y=True)

        data = pd.DataFrame(X)
        data['y'] = y
        df_train, df_test, _, _ = train_test_split(data, data, test_size=0.3)

        data.to_csv(os.path.join(folder, 'data.csv'), 
                    index=False)
        df_train.to_csv(os.path.join(folder, 'data_train.csv'), 
                        index=False)
        df_test.to_csv(os.path.join(folder, 'data_test.csv'), 
                       index=False)
