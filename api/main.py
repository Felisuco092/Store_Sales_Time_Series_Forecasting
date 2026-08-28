import os
from contextlib import asynccontextmanager

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request

from .schemas import Prediction


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Lógica de carga del modelo al iniciar la app
    env = os.getenv("ENVIRONMENT", "dev")

    if env == "docker":
        local_file = "./models/model.joblib"
        if not os.path.exists(local_file):
            from huggingface_hub import hf_hub_download

            print("Cargando modelo...")
            os.makedirs("./models", exist_ok=True)
            hf_hub_download(
                repo_id="Felisuco092/timeSeriesSalesKaggle",
                repo_type="model",
                filename="model.joblib",
                local_dir="./models",
            )
        model_file = local_file
    else:
        from src.config import MODEL_PATH

        model_file = os.path.join(MODEL_PATH, "model.joblib")

    # Guardamos el modelo en el estado global de la aplicación
    app.state.model = joblib.load(model_file)
    
    yield
    
    app.state.model = None


app = FastAPI(lifespan=lifespan)


@app.post("/predict")
async def predict_sale(prediction: Prediction, request: Request):
    model = request.app.state.model

    prediction_dict = prediction.model_dump()
    index = [prediction.id] if prediction.id is not None else [0]

    df = pd.DataFrame(prediction_dict, index=index)
    df["date"] = pd.to_datetime(df["date"])

    y_pred = model.predict(df)
    return {"sales": y_pred[0]}


@app.post("/predicts")
async def predict_sales(predictions: list[Prediction], request: Request):
    model = request.app.state.model

    prediction_dict = [p.model_dump() for p in predictions]
    df = pd.DataFrame(prediction_dict)

    has_ids = df["id"].notnull().all()
    if has_ids:
        df = df.set_index("id")
    df["date"] = pd.to_datetime(df["date"])

    y_pred = model.predict(df)

    if has_ids:
        response = [
            {"id": pred.id, "sales": y_pred[i]}
            for i, pred in enumerate(predictions)
        ]
    else:
        response = y_pred.ravel().tolist()

    return response