import sqlite3

DATABASE = 'tickets.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    # Tabella utenti
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    ''')

    # Tabella ticket
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            department TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL,
            attachment TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')

    # Tabella storico modifiche
    conn.execute('''
        CREATE TABLE IF NOT EXISTS ticket_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            title TEXT,
            description TEXT,
            department TEXT,
            status TEXT,
            modified_at TEXT NOT NULL,
            modified_by INTEGER NOT NULL,
            FOREIGN KEY(ticket_id) REFERENCES tickets(id),
            FOREIGN KEY(modified_by) REFERENCES users(id)
        );
    ''')

    conn.commit()
    conn.close()
