import json

def test_create_item(client):
    data={
        "username": "testuser1@test.com",
        "password": "testuser1"
    }
    response = client.post("/login/token", data=data)
    access_token=response.json()["access_token"]
    token_header={"Authorization":f"Bearer {access_token}"}

    data = {"title": "Gaming Laptop", "description": "HP Pavillion Gaming Laptop"}
    response = client.post("/items", json.dumps(data),headers=token_header)
    
    assert response.status_code == 200
    assert response.json()["title"] == "Gaming Laptop"
    assert response.json()["description"] == "HP Pavillion Gaming Laptop"


def test_retrieve_item_by_id(client):
    db_items = client.get("/items")
    response=client.get(f"/items/{db_items.json()[0]['id']}")
    assert response.status_code==200
    assert response.json()["title"] == "Gaming Laptop"
    assert response.json()["description"] == "HP Pavillion Gaming Laptop"


def test_update_item_by_id(client):
    data = {
        "username": "testuser1@test.com",
        "password": "testuser1"
    }
    response = client.post("/login/token", data=data)
    access_token=response.json()["access_token"]
    token_header={"Authorization":f"Bearer {access_token}"}

    db_items = client.get("/items")
    data = {"title": "Laptop", "description": "HP Pavillion Gaming Laptop"}
    id = db_items.json()[0]['id']
    response = client.put(f"/items/update/{id}", json.dumps(data), headers=token_header)
    assert response.status_code == 200
    assert response.json()["Message"] == f"Details Of {id} Successfully Updated"

   
def test_delete_item_by_id(client):
    data = {
        "username": "testuser1@test.com",
        "password": "testuser1"
    }
    response = client.post("/login/token", data=data)
    access_token=response.json()["access_token"]
    token_header={"Authorization":f"Bearer {access_token}"}
    
    db_items = client.get("/items")
    id = db_items.json()[0]['id']
    response = client.delete(f"/items/delete/{id}", headers=token_header)
    assert response.status_code == 200
    assert response.json()["Message"] == f"Item {id} Deleted Successfully"


