import pytest
from app import app as flask_app
from mongoengine import connect, disconnect
import mongomock

@pytest.fixture(scope='session', autouse=True)
def mock_db():
    # Desconectar cualquier conexión real antes de empezar
    disconnect()
    # Conectar usando mongomock
    connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)
    yield
    disconnect()

@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-key-123"
    })
    return flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
