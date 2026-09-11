import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app.database import Base
from app.models import categoria, movimentacao, produto
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

load_dotenv()

conexao_db_test = os.getenv("TEST_DATABASE_URL")

engine_teste = create_engine(conexao_db_test)
SessionTeste = sessionmaker(bind=engine_teste)

def get_db_test():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine_teste)
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_teste)

@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = get_db_test
    test_client = TestClient(app)

    test_client.post("/usuarios/", json={
        "nome": "Usuario Teste",
        "email": "teste@teste.com",
        "senha": "senha123"
    })

    response_login = test_client.post("/usuarios/login", json={
        "email": "teste@teste.com",
        "senha": "senha123"
    })

    token = response_login.json()["access_token"]
    test_client.headers.update({"Authorization": f"Bearer {token}"})

    yield test_client

    app.dependency_overrides.clear()



