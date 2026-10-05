import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_db_table():
    conn = connect_to_db()
    try:
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("User table created successfully")
    except Exception as e:
        print("User table creation failed:", e)
    finally:
        conn.close()

def insert_user(user):
    inserted_user = {}
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
            (user['name'], user['email'], user['phone'], user['address'], user['country'])
        )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except Exception:
        conn.rollback()
    finally:
        conn.close()
    return inserted_user

def get_users():
    users = []
    conn = connect_to_db()
    try:
        rows = conn.execute("SELECT * FROM users").fetchall()
        users = [dict(row) for row in rows]
    except Exception:
        users = []
    finally:
        conn.close()
    return users

def get_user_by_id(user_id):
    user = {}
    conn = connect_to_db()
    try:
        row = conn.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
        if row:
            user = dict(row)
    except Exception:
        user = {}
    finally:
        conn.close()
    return user

def update_user(user):
    updated_user = {}
    conn = connect_to_db()
    try:
        conn.execute(
            "UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?",
            (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"])
        )
        conn.commit()
        updated_user = get_user_by_id(user["user_id"])
    except Exception:
        conn.rollback()
        updated_user = {}
    finally:
        conn.close()
    return updated_user

def delete_user(user_id):
    message = {}
    conn = connect_to_db()
    try:
        conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception:
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message

if __name__ == "__main__":
    create_db_table()