import sqlite3
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEST_DB_NAME = "test_ims.db"
TEST_DB_PATH = Path(BASE_DIR) / TEST_DB_NAME


@pytest.fixture(autouse=True)
def use_test_db(monkeypatch):
    """
    Change the database path to the testing database.
    """

    import database

    Path.unlink(TEST_DB_PATH, missing_ok=True)

    monkeypatch.setattr(database, "DB_PATH", TEST_DB_PATH)

    database.initialize_db(TEST_DB_PATH)
