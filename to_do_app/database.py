import sqlite3

def initialize_db():
    try:
        # Connect to the SQLite database (or create it if it doesn't exist)
        conn = sqlite3.connect('tasks.db')
        cursor = conn.cursor()

        # Modify the 'users' table to include email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                email TEXT NOT NULL  -- New email field
            )
        ''')

        # Create the 'tasks' table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                project TEXT,
                deadline TEXT,
                priority INTEGER,
                category TEXT,
                user_id INTEGER,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        conn.commit()
        print("Database initialized successfully.")

    except sqlite3.Error as e:
        print(f"SQLite error occurred: {e}")
    
    finally:
        if conn:
            conn.close()

# Run database initialization
if __name__ == "__main__":
    initialize_db()
