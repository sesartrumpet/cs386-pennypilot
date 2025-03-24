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
