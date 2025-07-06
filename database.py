import sqlite3
import os

DB_PATH = "data/users.db"

def init_db():
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        cmnd TEXT,
        diachi TEXT,
        baohiem TEXT,
        stk TEXT,
        username TEXT UNIQUE,
        password TEXT
    )
    ''')
    conn.commit()
    conn.close()


def add_user(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (name, cmnd, diachi, baohiem, stk, username, password)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user


def update_user_by_username(username, updated_data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE users
        SET name = ?, cmnd = ?, diachi = ?, baohiem = ?, stk = ?
        WHERE username = ?
    ''', (
        updated_data['name'],
        updated_data['cmnd'],
        updated_data['diachi'],
        updated_data['baohiem'],
        updated_data['stk'],
        username
    ))
    conn.commit()
    conn.close()


def delete_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user
