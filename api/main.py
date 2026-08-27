from fastapi import FastAPI
import os
import joblib


app = FastAPI()


## Logica de cargar modelo
ENV = os.getenv("ENVIRONMENT", "docker")

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

@app.get("/")
async def read_item(item_id):
    return {"item_id": item_id}