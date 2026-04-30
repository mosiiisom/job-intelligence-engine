
# ==================== Database Tests ====================
def test_init_db_creates_jobs_table(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='jobs';
    """)

    table = cursor.fetchone()

    assert table is not None