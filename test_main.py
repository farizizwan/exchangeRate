from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_convert_unathorized():
    response = client.get("/convert")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}

def test_convert_forbidden():
    response = client.get("/convert", headers={"api_key": "myapikey123"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid credential"}

def test_convert_currency_notexists():
    response = client.get("/convert?convertFrom=gbp123&to=myr123&amount=1", headers={"api_key": "myapikey"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Currency not found"}

def test_convert_success():
    response = client.get("/convert?convertFrom=gbp&to=myr&amount=1", headers={"api_key": "myapikey"})
    assert response.status_code == 200
    res = response.json()
    assert res['rates'] != None

def test_history_unathorized():
    response = client.get("/history")
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}

def test_history_forbidden():
    response = client.get("/history", headers={"api_key": "myapikey123"})
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid credential"}

def test_history_success():
    response = client.get("/history?base=gbp&symbol=myr", headers={"api_key": "myapikey"})
    assert response.status_code == 200
    res = response.json()
    assert res['rates'] != None