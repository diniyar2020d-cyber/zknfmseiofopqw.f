import sqlite3
from datetime import datetime, timedelta
from typing import List, Tuple, Optional

DB_NAME = "bot_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    # Пользователи
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            tag TEXT UNIQUE,
            description TEXT,
            balance INTEGER DEFAULT 0,
            total_profits_sum INTEGER DEFAULT 0,
            total_profits_count INTEGER DEFAULT 0,
            rank TEXT DEFAULT 'LOW',
            join_date TEXT,
            is_banned INTEGER DEFAULT 0,
            is_approved INTEGER DEFAULT 0,
            is_anonymous INTEGER DEFAULT 0,
            mirror_token TEXT
        )
    """)
    
    # Профиты (история)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS profits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            commission INTEGER,
            net INTEGER,
            timestamp TEXT,
            country TEXT,
            streak INTEGER
        )
    """)
    
    # Заявки на вывод
    cur.execute("""
        CREATE TABLE IF NOT EXISTS withdraw_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            method TEXT,
            address TEXT,
            status TEXT DEFAULT 'pending'
        )
    """)
    
    # Реквизиты по странам
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requisites (
            country TEXT PRIMARY KEY,
            bank TEXT,
            holder TEXT,
            number TEXT,
            limits TEXT
        )
    """)
    
    # Анкеты (временные)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            user_id INTEGER PRIMARY KEY,
            answers TEXT,
            timestamp TEXT
        )
    """)
    
    conn.commit()
    conn.close()

# --- Users CRUD ---
def add_user(user_id: int, username: str, tag: str = None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if not tag:
        tag = f"user_{user_id}"
    cur.execute("""
        INSERT OR IGNORE INTO users (user_id, username, tag, join_date, is_approved)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, tag, datetime.now().isoformat(), 0))
    conn.commit()
    conn.close()

def get_user(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def update_user_field(user_id: int, field: str, value):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET {field} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def is_tag_free(tag: str, exclude_user_id: int = None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    if exclude_user_id:
        cur.execute("SELECT user_id FROM users WHERE tag = ? AND user_id != ?", (tag, exclude_user_id))
    else:
        cur.execute("SELECT user_id FROM users WHERE tag = ?", (tag,))
    result = cur.fetchone()
    conn.close()
    return result is None

# --- Profits ---
def add_profit(user_id: int, amount: int, country: str, streak: int = 1):
    commission = int(amount * 0.2)
    net = amount - commission
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # Обновляем баланс и статистику
    cur.execute("UPDATE users SET balance = balance + ?, total_profits_sum = total_profits_sum + ?, total_profits_count = total_profits_count + 1 WHERE user_id = ?",
                (net, amount, user_id))
    # Обновляем ранг
    cur.execute("SELECT total_profits_sum FROM users WHERE user_id = ?", (user_id,))
    total = cur.fetchone()[0]
    if total < 50000:
        rank = "LOW"
    elif total < 250000:
        rank = "MEDIA"
    elif total < 500000:
        rank = "HIGHT"
    else:
        rank = "GOD"
    cur.execute("UPDATE users SET rank = ? WHERE user_id = ?", (rank, user_id))
    # Записываем профит
    cur.execute("""
        INSERT INTO profits (user_id, amount, commission, net, timestamp, country, streak)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, amount, commission, net, datetime.now().isoformat(), country, streak))
    conn.commit()
    conn.close()
    return net

def get_user_stats(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT total_profits_count, total_profits_sum, balance FROM users WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row or (0, 0, 0)

def get_top_users(period: str = "all_time", limit: int = 10) -> List[Tuple]:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    now = datetime.now()
    if period == "day":
        start = datetime(now.year, now.month, now.day)
    elif period == "week":
        start = now - timedelta(days=7)
    elif period == "month":
        start = now - timedelta(days=30)
    else:
        start = datetime(1970, 1, 1)
    
    query = """
        SELECT u.tag, COUNT(p.id), SUM(p.amount)
        FROM profits p
        JOIN users u ON u.user_id = p.user_id
        WHERE p.timestamp >= ?
        GROUP BY p.user_id
        ORDER BY SUM(p.amount) DESC
        LIMIT ?
    """
    cur.execute(query, (start.isoformat(), limit))
    result = cur.fetchall()
    conn.close()
    return result

def get_total_cash(period: str = "all_time") -> int:
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    now = datetime.now()
    if period == "day":
        start = datetime(now.year, now.month, now.day)
    elif period == "week":
        start = now - timedelta(days=7)
    elif period == "month":
        start = now - timedelta(days=30)
    else:
        start = datetime(1970, 1, 1)
    cur.execute("SELECT SUM(amount) FROM profits WHERE timestamp >= ?", (start.isoformat(),))
    total = cur.fetchone()[0] or 0
    conn.close()
    return total

# --- Withdraw ---
def create_withdraw_request(user_id: int, amount: int, method: str, address: str = None):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO withdraw_requests (user_id, amount, method, address, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (user_id, amount, method, address))
    conn.commit()
    conn.close()

def get_pending_withdraws():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM withdraw_requests WHERE status = 'pending'")
    result = cur.fetchall()
    conn.close()
    return result

def update_withdraw_status(req_id: int, status: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE withdraw_requests SET status = ? WHERE id = ?", (status, req_id))
    conn.commit()
    conn.close()

# --- Requisites ---
def set_requisites(country: str, bank: str, holder: str, number: str, limits: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO requisites (country, bank, holder, number, limits)
        VALUES (?, ?, ?, ?, ?)
    """, (country, bank, holder, number, limits))
    conn.commit()
    conn.close()

def get_requisites(country: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT bank, holder, number, limits FROM requisites WHERE country = ?", (country,))
    row = cur.fetchone()
    conn.close()
    return row

def delete_requisites(country: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM requisites WHERE country = ?", (country,))
    conn.commit()
    conn.close()

def get_all_users_count():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users WHERE is_approved = 1")
    count = cur.fetchone()[0]
    conn.close()
    return count

def get_all_users_ids():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users WHERE is_approved = 1")
    users = [row[0] for row in cur.fetchall()]
    conn.close()
    return users

# --- Applications ---
def save_application(user_id: int, answers: str):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO applications (user_id, answers, timestamp) VALUES (?, ?, ?)",
                (user_id, answers, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_application(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT answers FROM applications WHERE user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def delete_application(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM applications WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

init_db()