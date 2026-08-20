from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_log_error
from features import get_full_preprocessing
from train import HybridModel
from data import load_data
from config import TRAIN_CSV_PATH, TEST_CSV_PATH
import numpy as np
import pandas as pd

import joblib
import os

#Si el modelo ya existe lo cargamos
if os.path.exists("./data/processed/LinearandXGBoost/model.joblib"):
    pipeline = joblib.load("./data/processed/LinearandXGBoost/model.joblib")
    print("Modelo cargado")
else:
    print("Modelo no encontrado")

    ct = get_full_preprocessing()
    ct.set_output(transform='pandas')

    pipeline = Pipeline([
        ("preprocessing", ct),
        ("model", HybridModel(random_state=42))
    ])

    df = load_data(TRAIN_CSV_PATH)
    X = df.drop("sales", axis=1)
    y = df["sales"]
    # Los partimos en train y test
    X_train, X_test, y_train, y_test = X[:-90], X[-90:], y[:-90], y[-90:]
    
    # Lo siguiente es para subir al kaggle habiendo entrenado el modelo con todos los datos
    #X_train, X_test, y_train, y_test = X, X, y, y
    #No hay diferencia en los resultados

    pipeline.fit(X_train, y_train)

    print("MSLE on test set:")
    print(np.sqrt(mean_squared_log_error(y_test, pipeline.predict(X_test))))

    joblib.dump(pipeline, "./data/processed/LinearandXGBoost/model.joblib")

test_df = load_data(TEST_CSV_PATH)


predictions = pd.DataFrame(pipeline.predict(test_df), columns=["sales"], index=test_df["id"])
predictions.index.name = "id"
print(predictions.head())
predictions.to_csv("./data/processed/LinearandXGBoost/predictions.csv")