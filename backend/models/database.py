import sqlite3

DATABASE = 'users.db'

# Function to get a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to add a new user to the database
def add_user(name, image_path, account_number, balance):
    try:
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO users (name, image_path, account_number, balance) 
                VALUES (?, ?, ?, ?)
            ''', (name, image_path, account_number, balance))
            conn.commit()
    except Exception as e:
        raise Exception(f"Error adding user: {e}")

# Function to get all users from the database
def get_all_users():
    try:
        with get_db_connection() as conn:
            cursor = conn.execute('SELECT name, image_path FROM users')
            users = cursor.fetchall()
        return users
    except Exception as e:
        raise Exception(f"Error fetching users: {e}")

# Function to get a user by name from the database
def get_user_by_name(name):
    try:
        with get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM users WHERE name = ?', (name,))
            user = cursor.fetchone()
        return user
    except Exception as e:
        raise Exception(f"Error fetching user: {e}")
