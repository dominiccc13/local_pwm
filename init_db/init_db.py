import sqlite3

users = []

with open(".\\init_db\\users_table.csv", "r") as f:
    for line in f:
        row = line.split(",")
        row = [row[0], row[1], row[-1]]
        users.append(row)

passwords = []

with open(".\\init_db\\passwords_table.csv", "r") as f:
    for line in f:
        row = line.split(",")
        passwords.append(row)

conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        confirmed INT DEFAULT 1,
        last_confirmed TEXT DEFAULT NULL,
        password_hash TEXT NOT NULL
    )         
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        user_id INTEGER NOT NULL,
        account TEXT NOT NULL UNIQUE,
        username TEXT,
        email TEXT,
        encrypted_password TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )         
''')
for row in users:
    if row == users[0]:
        continue
    cur.execute(f'''
        INSERT INTO users (email, password_hash)
        VALUES (?, ?)      
    ''', (row[1], row[2],))
    conn.commit()

for row in passwords:
    if row == passwords[0]:
        continue
    cur.execute(f'''
        INSERT INTO passwords (user_id, account, username, email, encrypted_password)
        VALUES (?, ?, ?, ?, ?)      
    ''', (row[0], row[1], row[2], row[3], row[4],))
    conn.commit()

conn.close()