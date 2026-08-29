# Store_Sales_Time_Series_Forecasting
Competición hecha por Félix Jiménez Almanza
A kaggle competition for practice of the end-to-end projects


Estructura del proyecto inicial:

```
time_series_kaggle/
├── .gitignore
├── README.md
├── pyproject.toml  
├── uv.lock
├── .dockerignore
├── Dockerfile                  # Contenerización de la app de inferencia
│
├── data/                       # IGNORADO EN .GITIGNORE (excepto sample)
│   ├── raw/                    # Datos originales de Kaggle
│   ├── processed/              # Datos limpios y procesados
│   └── sample/                 # Pequeña muestra (5-10 filas) para tests y API
│
├── notebooks/                  # Exploración e investigación
│   ├── 01_eda.ipynb            # Análisis exploratorio visual y limpio
│   ├── 02_feature_engineering.ipynb
│   └── 03_model_experiments.ipynb
│
├── src/                        # Código modular de Python
│   ├── __init__.py
│   ├── config.py               # Rutas, hiperparámetros y constantes
│   ├── data.py                 # Carga, limpieza y particionado
│   ├── features.py             # Feature engineering reutilizable
│   ├── train.py                # Script de entrenamiento e hiperparámetros
│   └── pipeline.py             # Programa principal que prueba todo con un pipeline
│
└──  api/                        # Capa de Backend (Servicio web)
    ├── __init__.py
    ├── main.py                 # FastAPI / Flask endpoint
    └── schemas.py              # Validación de entradas/salidas (Pydantic)
    └── test_api.py             # Tests para main.py (Pytest)


```

## Modelo Entrenado

El modelo entrenado y su control de versiones se encuentran en:
🔗 [Hugging Face Model Registry](https://huggingface.co/Felisuco092/timeSeriesSalesKaggle/tree/main)

### ⚠️ Importante para usar el modelo con joblib

Para que el modelo entrenado funcione correctamente al cargarlo con `joblib`, es **necesario** que el módulo `src` esté disponible como paquete Python. Asegúrate de:

1. Que el directorio `src/` tenga un archivo `__init__.py` (ya incluido en la estructura)
2. Que `src/` esté en el `PYTHONPATH` o que instales el proyecto como paquete:
   ```bash
   pip install -e .
   ```
3. Que las importaciones en el modelo coincidan con la estructura de `src/` (ej: `from src.features import ...`)

Sin esto, joblib no podrá desserializar correctamente el modelo y sus dependencias.
