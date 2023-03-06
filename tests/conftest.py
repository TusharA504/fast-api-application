from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest

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

