import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app, calculate


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- Unit tests for calculate() ---

def test_addition():
    assert calculate(3, "+", 4) == 7


def test_subtraction():
    assert calculate(10, "-", 3) == 7


def test_multiplication():
    assert calculate(6, "*", 7) == 42


def test_division():
    assert calculate(15, "/", 3) == 5


def test_division_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculate(5, "/", 0)


def test_unknown_operator():
    with pytest.raises(ValueError, match="Unknown operator"):
        calculate(5, "^", 2)


def test_negative_numbers():
    assert calculate(-3, "+", -4) == -7


def test_float_result():
    assert calculate(1, "/", 3) == pytest.approx(1 / 3)


def test_square():
    assert calculate(5, "sqr", 0) == 25


# --- Integration tests for Flask routes ---

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Calculator" in response.data


def test_calculate_addition(client):
    response = client.post("/calculate", json={"num1": 5, "operator": "+", "num2": 3})
    assert response.status_code == 200
    assert response.get_json()["result"] == 8


def test_calculate_subtraction(client):
    response = client.post("/calculate", json={"num1": 10, "operator": "-", "num2": 4})
    assert response.status_code == 200
    assert response.get_json()["result"] == 6


def test_calculate_multiplication(client):
    response = client.post("/calculate", json={"num1": 7, "operator": "*", "num2": 6})
    assert response.status_code == 200
    assert response.get_json()["result"] == 42


def test_calculate_division(client):
    response = client.post("/calculate", json={"num1": 20, "operator": "/", "num2": 4})
    assert response.status_code == 200
    assert response.get_json()["result"] == 5


def test_calculate_square(client):
    response = client.post("/calculate", json={"num1": 9, "operator": "sqr"})
    assert response.status_code == 200
    assert response.get_json()["result"] == 81


def test_calculate_division_by_zero(client):
    response = client.post("/calculate", json={"num1": 5, "operator": "/", "num2": 0})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_calculate_invalid_operator(client):
    response = client.post("/calculate", json={"num1": 5, "operator": "^", "num2": 2})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_calculate_missing_fields(client):
    response = client.post("/calculate", json={"num1": 5})
    assert response.status_code == 400
    assert "error" in response.get_json()
