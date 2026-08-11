# Store_Sales_Time_Series_Forecasting
Competición hecha por Félix Jiménez Almanza
A kaggle competition for practice of the end-to-end projects


Estructura del proyecto inicial:

```
time_series_kaggle/
├── .gitignore
├── README.md
├── requirements.txt            # o pyproject.toml / environment.yml
├── Dockerfile                  # Contenerización de la app de inferencia
├── docker-compose.yml          # Opcional: si montas backend + base de datos
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
│   └── predict.py              # Lógica de inferencia con el modelo cargado
│
├── api/                        # Capa de Backend (Servicio web)
│   ├── __init__.py
│   ├── main.py                 # FastAPI / Flask endpoint
│   └── schemas.py              # Validación de entradas/salidas (Pydantic)
│
├── models/                     # Artefactos del modelo (.pkl, .onnx, etc.) -> .gitignore
└── tests/                      # Pruebas unitarias
    ├── test_data.py
    └── test_api.py
```
