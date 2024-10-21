import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import sqlite3

# Function to send an email notification
def send_email_notification(task_name, deadline, recipient_email):
    # Create the email content
    subject = "Task Reminder"
    body = f"Reminder: Task '{task_name}' is due on {deadline}."
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "youremail@gmail.com"  # Replace with your Gmail address
    msg["To"] = recipient_email

    # Send the email via Gmail's SMTP server
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login("youremail@gmail.com", "yourpassword")  # Use your email and password (or App Password)
            server.sendmail("youremail@gmail.com", recipient_email, msg.as_string())
        print(f"Email notification sent to {recipient_email} for task '{task_name}'.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to check for upcoming tasks and send notifications (via email)
def check_and_notify_upcoming_tasks(user_id, recipient_email):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    # Get today's date
    today = datetime.today().date()
    print(f"Today's date: {today}")

    # Fetch tasks with deadlines within the next 3 days for the given user
    cursor.execute('''
        SELECT name, deadline FROM tasks
        WHERE user_id = ? AND DATE(deadline) >= DATE(?) AND DATE(deadline) <= DATE(?, '+3 days')
    ''', (user_id, today, today))

    tasks = cursor.fetchall()
    conn.close()

    # If tasks are found, send an email notification for each
    if len(tasks) > 0:
        for task in tasks:
            task_name, deadline = task
            print(f"Sending email notification for task: '{task_name}' due on {deadline}")
            send_email_notification(task_name, deadline, recipient_email)
    else:
        print("No upcoming tasks within the next 3 days.")
