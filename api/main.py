from fastapi import FastAPI
import os
import joblib
from .schemas import Prediction
import pandas as pd
import numpy as np


app = FastAPI()


## Logica de cargar modelo
ENV = os.getenv("ENVIRONMENT", "dev")

# Esto para cargarlo en docker
if ENV == "docker":
    local_file = "./models/model.joblib"
    if not os.path.exists(local_file):
        from huggingface_hub import hf_hub_download
        print("Cargando modelo")
        os.makedirs("./models", exist_ok=True)
        hf_hub_download(
            repo_id="Felisuco092/timeSeriesSalesKaggle",
            repo_type="model",
            filename="model.joblib",
            local_dir="./models"
        )
    model_file = local_file
else: #Y esto para cargarlo en dev
    from src.config import MODEL_PATH
    model_file = os.path.join(MODEL_PATH, "model.joblib")

model = joblib.load(model_file)

@app.post("/predict")
async def predict_sale(prediction: Prediction):
    prediction_dict = prediction.model_dump()
    if prediction.id is not None:
        index = [prediction.id]
    else:
        index = [0]
    
    df = pd.DataFrame(prediction_dict, index=index)
    df["date"] = pd.to_datetime(df["date"])

    y_pred = model.predict(df)
    print(y_pred)
    return {"sales": y_pred[0]}


@app.post("/predicts")
async def predict_sale(predictions: list[Prediction]):
    prediction_dict = [prediction.model_dump() for prediction in predictions]

        
    df = pd.DataFrame(prediction_dict)

    if "id" in df.columns:
        df = df.set_index("id")
    df["date"] = pd.to_datetime(df["date"])

    y_pred = model.predict(df)
    print(y_pred)
    return [{"id": prediction.id, "sales": y_pred[i]} for i, prediction in enumerate(predictions)]