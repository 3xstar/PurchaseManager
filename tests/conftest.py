import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from modules_project.models.models import Base

TEST_DATABASE_URL = DATABASE_URL.replace("purchase_manager", "purchase_manager_test")

SERVER_URL = DATABASE_URL.rsplit('/', 1)[0] + '/mysql'


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    engine = create_engine(SERVER_URL)
    with engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS purchase_manager_test"))
    engine.dispose()


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(TEST_DATABASE_URL)

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)