import sqlite3
from datetime import datetime

# Function to add a new task
def add_task(name, project, deadline, priority, category, user_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Insert a new task into the tasks table
    cursor.execute('''
        INSERT INTO tasks (name, project, deadline, priority, category, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, project, deadline, priority, category, user_id))

    conn.commit()
    conn.close()
    print("Task added successfully!")
    print(f"Adding task for user_id: {user_id}")


# Function to view all tasks for a user
def view_tasks(user_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Retrieve all tasks for the given user
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()

    conn.close()
    
    # If no tasks found
    if len(tasks) == 0:
        print("No tasks found.")
        return
    
    print("Tasks:")
    for task in tasks:
        print(f"ID: {task[0]}, Name: {task[1]}, Project: {task[2]}, Deadline: {task[3]}, Priority: {task[4]}, Category: {task[5]}")

# Function to update a task by task_id
def update_task(task_id, name=None, project=None, deadline=None, priority=None, category=None):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Fetch the current task details
    cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
    task = cursor.fetchone()

    if not task:
        print(f"Task with ID {task_id} not found.")
        return

    # Update the task details only if a new value is provided
    new_name = name if name else task[1]
    new_project = project if project else task[2]
    new_deadline = deadline if deadline else task[3]
    new_priority = priority if priority else task[4]
    new_category = category if category else task[5]

    # Update the task in the database
    cursor.execute('''
        UPDATE tasks
        SET name = ?, project = ?, deadline = ?, priority = ?, category = ?
        WHERE id = ?
    ''', (new_name, new_project, new_deadline, new_priority, new_category, task_id))

    conn.commit()
    conn.close()
    print(f"Task {task_id} updated successfully!")

# Function to delete a task by task_id
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Delete the task
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    
    if cursor.rowcount == 0:
        print(f"Task with ID {task_id} not found.")
    else:
        print(f"Task {task_id} deleted successfully!")

    conn.commit()
    conn.close()

# Example usage of task management functions
if __name__ == "__main__":
    # Add a task
    add_task("Finish Project", "Work", "2024-10-30", 1, "High", user_id=1)

    # View tasks for user with user_id = 1
    view_tasks(user_id= 1)

    # Update a task with task_id = 1
    update_task(task_id= 1, name="Finish Python Project", deadline="2024-11-01")

    # Delete a task with task_id = 1
    delete_task(task_id= 1)
