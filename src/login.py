import tkinter as tk
from tkinter import messagebox
from signup import *
from prof import *
from manager import *
from admin import *
import psycopg2

def login(connection):
    """def get_conn(username):
        if username == 'manager':
            connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="manager",
                password="manager"
            )
        elif username == 'admin':
            connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="admin",
                password="admin"
            )
        else:
            connection = psycopg2.connect(
                host="localhost",
                database="postgres",
                user="user",
                password="user"
            )
        return connection"""
    def validate_login():
        username = entry_username.get()
        password = entry_password.get()

        # Verify the login credentials using the PostgreSQL database
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = %s AND pwd = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            #messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            #connection = get_conn(username)
            if username == 'manager':
                window.destroy()
                manager(connection)
            elif username == 'admin':
                window.destroy()
                admin(connection)
            else:
                window.destroy()
                prof(connection, username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def toSignup():
        window.destroy()
        signup(connection)

    # Create the main window
    window = tk.Tk()
    window.title("Login Screen")
    window.configure(bg="#ffffff")
    window.state('normal')
    window.attributes('-zoomed', True)

    # Create and place the logo
    logo = tk.PhotoImage(file="img/logo.png")
    label_logo = tk.Label(window, image=logo, bg="#ffffff")
    label_logo.pack(pady=40)

    # Create and place the username label and entry
    label_username = tk.Label(window, text="USERNAME", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_username.pack(pady=(20, 5))
    entry_username = tk.Entry(window, font=("Arial", 12), bg="#ffffff", fg="#333333", relief="flat")
    entry_username.pack(pady=(0, 20), ipady=5)

    # Create and place the password label and entry
    label_password = tk.Label(window, text="PASSWORD", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_password.pack(pady=(0, 5))
    entry_password = tk.Entry(window, show="*", font=("Arial", 12), bg="#ffffff", fg="#333333", relief="flat")
    entry_password.pack(pady=(0, 20), ipady=5)

    # Create and place the login button
    btn_login = tk.Button(window, text="Login", command=validate_login, font=("Arial", 12), bg="#ff80ab", fg="#ffffff", relief="flat")
    btn_login.pack(pady=(0, 20), ipadx=30, ipady=5)

    # Create and place the divider line
    line_divider = tk.Frame(window, width=200, height=1, bg="#ff80ab")
    line_divider.pack(pady=(20, 5))

    # Create and place the signup label
    label_signup = tk.Label(window, text="Don't have an account?", font=("Arial", 10), bg="#ffffff", fg="#808080")
    label_signup.pack()

    # Create and place the signup button
    btn_signup = tk.Button(window, text="Sign Up for Free", command=toSignup, font=("Arial", 10, "bold"), bg="#ffffff", fg="#ff80ab", relief="flat")
    btn_signup.pack(pady=(0, 40), ipadx=30, ipady=5)

    # Run the main event loop
    window.mainloop()

