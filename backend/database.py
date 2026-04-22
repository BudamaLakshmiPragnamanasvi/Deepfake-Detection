import os
import sqlite3
import aiosqlite
from datetime import datetime

DATABASE_URL = "predictions.db"

async def init_db():
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                label TEXT NOT NULL,
                confidence REAL NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                grad_cam_path TEXT
            )
        ''')
        await db.commit()

async def save_prediction(filename: str, label: str, confidence: float, grad_cam_path: str = None):
    async with aiosqlite.connect(DATABASE_URL) as db:
        await db.execute('''
            INSERT INTO predictions (filename, label, confidence, timestamp, grad_cam_path)
            VALUES (?, ?, ?, ?, ?)
        ''', (filename, label, confidence, datetime.now(), grad_cam_path))
        await db.commit()

async def get_all_predictions():
    async with aiosqlite.connect(DATABASE_URL) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM predictions ORDER BY timestamp DESC') as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
