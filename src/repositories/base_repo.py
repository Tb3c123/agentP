"""
agentP - Base Repository
Pattern: Repository Pattern (Data Access Decoupling)
Author: Maya (Architect) & Carlos (Backend Dev)
"""

import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DB_PATH = os.path.join(BASE_DIR, '.agents', 'db.sqlite')

class BaseRepository:
    """Manages SQLite WAL database connections with foreign key enforcement."""

    @staticmethod
    def get_connection():
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        return conn
