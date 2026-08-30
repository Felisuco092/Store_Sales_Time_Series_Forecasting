import os
from contextlib import asynccontextmanager

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Request

from .schemas import Prediction


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load the model on startup and release it on shutdown.

    Parameters
    ----------
    app : FastAPI
        The FastAPI application instance.

    Yields
    ------
    None
    """
    model_path = os.getenv("MODEL_PATH", "./models/model.joblib")
    app.state.model = joblib.load(model_path)
    yield
    app.state.model = None


app = FastAPI(lifespan=lifespan)


@app.post("/predict")
async def predict_sale(prediction: Prediction, request: Request):
    """
    Predict the sales for a single prediction request.

    Parameters
    ----------
    prediction : Prediction
        The input payload with the store and product data.
    request : Request
        The request object, used to access the loaded model.

    Returns
    -------
    dict
        A dictionary with the predicted sales value.
    """
    model = request.app.state.model

    prediction_dict = prediction.model_dump()
    index = [prediction.id] if prediction.id is not None else [0]

    df = pd.DataFrame(prediction_dict, index=index)
    df["date"] = pd.to_datetime(df["date"])

    y_pred = model.predict(df)
    return {"sales": y_pred[0]}


@app.post("/predicts")
async def predict_sales(predictions: list[Prediction], request: Request):
    """
    Predict the sales for a batch of prediction requests.

    Parameters
    ----------
    predictions : list of Prediction
        The list of input payloads with the store and product data.
    request : Request
        The request object, used to access the loaded model.

    Returns
    -------
    list
        A list with the predicted sales, either keyed by id when ids are
        provided or as a plain list of values otherwise.
    """
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