import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import get_connection

def test_get_connection():
    config = {
        'host': 'localhost',
        'database': 'pennypilot_db',
        'user': 'root',
        'password': '123455',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
        'port': 3306
    }
    conn = get_connection(config)

    # Make sure connection is active
    assert conn.is_connected() is True
    conn.close()

def test_create_database_if_not_exists_invalid_config():
    from database import create_database_if_not_exists
    result = create_database_if_not_exists({"host": "invalid", "user": "none", "password": "bad"})
    assert result is False

def test_run_sql_file_missing_file(tmp_path):
    from database import run_sql_file
    fake_file = tmp_path / "fake.sql"
    class DummyCursor:
        def execute(self, sql): pass
    result = run_sql_file(DummyCursor(), str(fake_file))
    assert result is False
