import pytest
from unittest.mock import patch

from storage.database import get_connection, init_db


@pytest.fixture
def test_db_path(tmp_path):
    return tmp_path / "test_job.db"


@pytest.fixture
def db_connection(test_db_path):
    with patch('storage.database.DB_PATH', str(test_db_path)):
        conn = get_connection()
        init_db()
        yield conn
        conn.close()