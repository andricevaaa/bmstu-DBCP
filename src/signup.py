import tkinter as tk
from tkinter import messagebox
from prof import *

def signup(connection):
    def validate_signup():
        # Get the values from the input fields
        username = input_fields[0][1].get()
        password = input_fields[1][1].get()
        first_name = input_fields[2][1].get()
        last_name = input_fields[3][1].get()
        phone_number = input_fields[4][1].get()
        email = input_fields[5][1].get()
        address = input_fields[6][1].get()
        city = input_fields[7][1].get()
        country = input_fields[8][1].get()

        # Perform validation
        if not username or not password or not email:
            messagebox.showerror("Error", "Username, password, and email are required.")
        else:
            # Insert the new user data into the database
            try:
                cursor = connection.cursor()
                query = "INSERT INTO users (username, pwd, firstname, lastname, phone, mail, address, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (username, password, first_name, last_name, phone_number, email, address, city, country))
                connection.commit()
                cursor.close()
                window.destroy()
                prof(connection, username)
            except:
                messagebox.showerror("Error", "Incorrect input")


    # Create the main window
    window = tk.Tk()
    window.title("Signup Page")
    window.state('normal')
    window.attributes('-zoomed', True)
    window.configure(bg="white")

    # Calculate the center position of the screen
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = 500
    window_height = 500
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Set the background color
    window.configure(bg="white")

    # Create and place the logo
    logo = tk.PhotoImage(file="img/logo.png")
    label_logo = tk.Label(window, image=logo, bg="white")
    label_logo.pack(pady=20)

    # Create and place the signup title
    label_signup = tk.Label(window, text="Sign up", font=("Arial", 16, "bold"), bg="white")
    label_signup.pack(pady=10)

    # Create a frame to contain the input fields
    frame_inputs = tk.Frame(window, bg="white")
    frame_inputs.pack()

    # Create and place the input fields
    input_fields = [
        ("Username", tk.Entry(frame_inputs, font=("Arial", 12))),
        ("Password", tk.Entry(frame_inputs, show="*", font=("Arial", 12))),
        ("First Name", tk.Entry(frame_inputs, font=("Arial", 12))),
        ("Last Name", tk.Entry(frame_inputs, font=("Arial", 12))),
        ("Phone Number", tk.Entry(frame_inputs, font=("Arial", 12))),
        ("Email", tk.Entry(frame_inputs, font=("Arial", 12))),
        ("Address", tk.Entry(frame_inputs, font=("Arial", 12))),
        ("City", tk.Entry(frame_inputs, font=("Arial", 12))),
        ("Country", tk.Entry(frame_inputs, font=("Arial", 12)))
    ]

    for i, (label_text, entry) in enumerate(input_fields):
        label = tk.Label(frame_inputs, text=label_text, font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
        label.grid(row=i, column=0, padx=10, pady=5)
        entry.grid(row=i, column=1, padx=10, pady=5)
        
    # Create and place the signup button
    btn_signup = tk.Button(window, text="Sign up", command=validate_signup, font=("Arial", 12), bg="#ff80ab", fg="#ffffff", relief="flat")
    btn_signup.pack(pady=20, ipadx=30, ipady=5)

    # Create and place the terms of service label
    label_tos = tk.Label(window, text="By signing up, you agree to Terms of Service and Privacy Policy.", font=("Arial", 10), bg="white")
    label_tos.pack()

    # Run the main event loop
    window.mainloop()

