
import sqlite3

DB_NAME = "database.db"


def get_db():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    users = [
        ("admin", "admin123"),
        ("user", "user123")
    ]

    for username, password in users:
        db.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

    db.commit()
    db.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
