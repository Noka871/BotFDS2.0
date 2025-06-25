import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional


class Database:
    def __init__(self, db_path: str = "dubbing.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        with self.conn:
            self.conn.executescript("""
                                    CREATE TABLE IF NOT EXISTS users
                                    (
                                        id
                                        INTEGER
                                        PRIMARY
                                        KEY,
                                        username
                                        TEXT,
                                        role
                                        TEXT
                                        CHECK (
                                        role
                                        IN
                                    (
                                        'dubber',
                                        'timer',
                                        'admin'
                                    )),
                                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                        );

                                    CREATE TABLE IF NOT EXISTS titles
                                    (
                                        id
                                        INTEGER
                                        PRIMARY
                                        KEY
                                        AUTOINCREMENT,
                                        name
                                        TEXT
                                        NOT
                                        NULL,
                                        total_episodes
                                        INTEGER,
                                        current_episode
                                        INTEGER
                                        DEFAULT
                                        1,
                                        created_at
                                        TIMESTAMP
                                        DEFAULT
                                        CURRENT_TIMESTAMP
                                    );

                                    -- Остальные таблицы по аналогии
                                    """)

    async def get_user_titles(self, user_id: int) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("""
                       SELECT t.id, t.name, t.current_episode
                       FROM titles t
                                JOIN assignments a ON t.id = a.title_id
                       WHERE a.user_id = ?
                       """, (user_id,))
        return [dict(row) for row in cursor.fetchall()]