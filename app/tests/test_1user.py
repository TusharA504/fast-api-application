
import json


def test_create_user(client):
    data={"email":"testuser2@test.com","password":"testuser2"}
    response=client.post("/user",json.dumps(data))
    assert response.status_code==200
    assert response.json()["email"] == "testuser2@test.com"
    assert response.json()["is_active"]==True
    

def test_duplicate_user(client):
    data = {"email": "testuser2@test.com", "password": "testuser2"}
    response=client.post("/user",json.dumps(data))
    assert response.status_code==400
    assert response.json()["detail"] == "Email already registered"

