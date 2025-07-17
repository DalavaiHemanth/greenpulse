import sqlite3

# Connect to the SQLite database (or create it)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Drop existing users table
cursor.execute('DROP TABLE IF EXISTS users')

# Create a fresh users table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("✅ users.db initialized.")
