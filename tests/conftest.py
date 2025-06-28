import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app import create_app, get_session
from config.settings import Settings


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app = create_app()
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_settings(monkeypatch):
    """Mock settings for testing"""
    test_settings = Settings(
        database_url="sqlite:///:memory:",
        s3_bucket="test-bucket",
        broker_url="redis://localhost:6379/0",
        aws_access_key_id="test-key",
        aws_secret_access_key="test-secret",
        aws_region="us-east-1"
    )
    monkeypatch.setattr("config.settings.settings", test_settings)
    return test_settings