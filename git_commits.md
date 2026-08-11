| Tipo de Commit | ¿Cuándo usarlo? | Ejemplo concreto |
| :--- | :--- | :--- |
| `feat` | Nueva funcionalidad en código Python o API. | `feat(features): add scaling and encoding pipelines` |
| `model` | Cambios o experimentos directos en el modelo. | `model(xgb): train baseline xgboost model with 0.82 auc` |
| `refactor` | Pasar código de notebooks a `src/` sin cambiar su comportamiento. | `refactor(data): move data loading functions to src/data.py` |
| `api` | Cambios en la capa de backend / endpoints. | `api(fastapi): implement /predict endpoint with pydantic validation` |
| `docker` | Archivos de contenerización o despliegue. | `docker: create dockerfile for api deployment` |
| `docs` | Cambios en la documentación o `README.md`. | `docs: update install instructions and add architecture diagram` |
| `chore` | Tareas secundarias (crear `.gitignore`, actualizar `requirements.txt`). | `chore: add models directory to gitignore` |
| `fix` | Corregir un error de código o fallo en el entrenamiento. | `fix(predict): handle missing keys in incoming json payload` |
| `test` | Añadir o modificar pruebas unitarias. | `test(api): add unit test for status 200 on /predict` |
