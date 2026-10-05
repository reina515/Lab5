import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


def connect_to_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_db_table():
    conn = connect_to_db()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')
        conn.commit()
        print("User table ready")
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
        new_id = cur.lastrowid
    except Exception:
        conn.rollback()
        new_id = None
    finally:
        conn.close()

    if new_id is not None:
        inserted_user = get_user_by_id(new_id)
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
        ok = True
    except Exception:
        conn.rollback()
        ok = False
    finally:
        conn.close()

    if ok:
        updated_user = get_user_by_id(user["user_id"])
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



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())


@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))


@app.route('/api/users/add', methods=['POST'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))


@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))


@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))


if __name__ == "__main__":
    create_db_table()
    app.run()