import sqlite3
import bcrypt

# Function to register a new user
def register_user(username, password):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is not None:
        print("Username already exists!")
        return False

    # Hash the password using bcrypt
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert the new user into the database
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()
    print("User registered successfully!")
    return True

# Function to log in a user
def login_user(username, password):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Fetch the user's hashed password from the database
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user is None:
        print("User not found!")
        return False

    # Verify the password
    if bcrypt.checkpw(password.encode(), user[0]):
        print("Login successful!")
        return True
    else:
        print("Invalid password!")
        return False

# Example usage:
if __name__ == "__main__":
    # Register a new user
    register_user("testuser", "testpassword")

    # Log in with the same user
    login_user("testuser", "testpassword")
