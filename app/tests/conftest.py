from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest
import json

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import setting
from services import get_db
from database import Base
from main import app

SQLALCHEMY_DATABASE_URL = setting.SQLITE_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()


    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    yield client 


@pytest.fixture
def login(client):
    client=client

    # creates user
    data = {"email": "testuser1@test.com", "password": "testuser1"}
    response = client.post("/user", json.dumps(data))

    # login
    data = {
        "username": "testuser1@test.com",
        "password": "testuser1"
    }
    
    response = client.post("/login/token", data=data)
    access_token = response.json()["access_token"]
    return access_token





    
