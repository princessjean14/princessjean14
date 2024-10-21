import sqlite3
import bcrypt
from tasks import add_task, view_tasks, update_task, delete_task
from notification import check_and_notify_upcoming_tasks


# Function to register a new user
def register_user(username, password, email):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone() is not None:
        print("Username already exists!")
        return False

    # Hash the password using bcrypt
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # Insert the new user into the database, including email
    cursor.execute('INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)', (username, password_hash, email))
    conn.commit()
    conn.close()
    print("User registered successfully!")
    return True

# Function to log in a user and retrieve their email
def login_user(username, password):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Fetch the user's id, hashed password, and email from the database
    cursor.execute('SELECT id, password_hash, email FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user is None:
        print("User not found!")
        return False, None, None

    # Verify the password
    if bcrypt.checkpw(password.encode(), user[1]):
        print("Login successful!")
        return True, user[0], user[2]  # Return the user's id and email
    else:
        print("Invalid password!")
        return False, None, None


# Main function to drive the application
def main():
    print("Welcome to the To-Do List Application!")
    choice = input("Do you have an account? (yes/no): ").strip().lower()

    if choice == "no":
        username = input("Enter a new username: ")
        password = input("Enter a new password: ")
        email = input("Enter your email: ")
        register_user(username, password, email)


    # Initialize the variables for login state
    logged_in = False
    user_id = None

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Try to log in the user
    logged_in, user_id, recipient_email = login_user(username, password)

    if logged_in:
        print("Checking for upcoming tasks...")
        check_and_notify_upcoming_tasks(user_id, recipient_email)


        while True:
            print("\nMenu:")
            print("1. Add a new task")
            print("2. View all tasks")
            print("3. Update a task")
            print("4. Delete a task")
            print("5. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                # Add a new task
                name = input("Task Name: ")
                project = input("Project Name: ")
                deadline = input("Deadline (YYYY-MM-DD): ")
                priority = int(input("Priority (1=High, 2=Medium, 3=Low): "))
                category = input("Category: ")
                add_task(name, project, deadline, priority, category, user_id)

            elif choice == "2":
                # View all tasks
                view_tasks(user_id)

            elif choice == "3":
                # Update a task
                task_id = int(input("Enter the task ID to update: "))
                name = input("New Task Name (leave empty to keep current): ")
                project = input("New Project Name (leave empty to keep current): ")
                deadline = input("New Deadline (leave empty to keep current): ")
                priority = input("New Priority (1=High, 2=Medium, 3=Low, leave empty to keep current): ")
                category = input("New Category (leave empty to keep current): ")
                update_task(task_id, name, project, deadline, int(priority) if priority else None, category)

            elif choice == "4":
                # Delete a task
                task_id = int(input("Enter the task ID to delete: "))
                delete_task(task_id)

            elif choice == "5":
                print("Goodbye!")
                break

            else:
                print("Invalid choice! Please try again.")
    else:
        print("Login failed!")

if __name__ == "__main__":
    main()