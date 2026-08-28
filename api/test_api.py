from api.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import numpy as np
import pytest



#Hacemos una fixture para preparar el mock de joblib y ejecutar el lifespan
@pytest.fixture
def client_and_mock():
    with patch("api.main.joblib.load") as mock_joblib_load:
        mock_modelo = MagicMock()
        mock_joblib_load.return_value = mock_modelo
        with TestClient(app) as client:
            yield client, mock_modelo

#############
# TESTS
#############

def test_predict_sale(client_and_mock):
    client, mock_modelo = client_and_mock
    mock_modelo.predict.return_value = [5]

    message = {
        "date": "2017-08-16",
        "store_nbr": 1,
        "family": "AUTOMOTIVE",
        "onpromotion": 0
    }
    response = client.post("/predict", json=message)
    assert response.status_code == 200
    assert response.json() == {"sales": 5}

def test_predicts_sales_with_ids(client_and_mock):
    client, mock_modelo = client_and_mock
    mock_modelo.predict.return_value = [5,7]

    message = [
        {
            "id": 3000888,
            "date": "2017-08-16",
            "store_nbr": 1,
            "family": "AUTOMOTIVE",
            "onpromotion": 0
        },
        {
            "id": 3000889,
            "date": "2017-08-16",
            "store_nbr": 1,
            "family": "BABY CARE",
            "onpromotion": 0
        }
    ]
    response = client.post("/predicts", json=message)
    assert response.status_code == 200
    assert response.json() == [{"id": 3000888, "sales": 5}, {"id": 3000889, "sales": 7}]

def test_predicts_sales_without_ids(client_and_mock):
    client, mock_modelo = client_and_mock
    mock_modelo.predict.return_value = np.array([5,7])

    message = [
        {
            "date": "2017-08-16",
            "store_nbr": 1,
            "family": "AUTOMOTIVE",
            "onpromotion": 0
        },
        {
            "date": "2017-08-16",
            "store_nbr": 1,
            "family": "BABY CARE",
            "onpromotion": 0
        }
    ]
    response = client.post("/predicts", json=message)
    assert response.status_code == 200
    assert response.json() == [5,7]