import os.path
from unittest.mock import patch, MagicMock

import pytest

from storage.database import get_connection, init_db

# ==================== Fixtures ====================

db_test_path = "./test.db"


@pytest.fixture
def connection():
    with patch('storage.database.DB_PATH', db_test_path):
        conn = get_connection()
        yield conn

    conn.close()
    if os.path.exists(db_test_path):
        os.remove(db_test_path)


# ==================== Database Tests ====================
def test_init_db_creates_jobs_table(connection):
    init_db()

    cursor = connection.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='jobs';
    """)

    table = cursor.fetchone()

    assert table is not None