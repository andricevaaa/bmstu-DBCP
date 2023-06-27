import tkinter as tk
from tkinter import messagebox
from previousorders import *

def prof(connection, current_user):
    def home():
        window.destroy()
        from homepage import first_hp
        first_hp(connection, current_user)

    def show_profile():
        # Retrieve the user's information from the database
        cursor = connection.cursor()
        query = "SELECT username, pwd, firstname, lastname, phone, mail, address, city, country FROM users WHERE username = %s"
        cursor.execute(query, (current_user,))
        user_data = cursor.fetchone()
        cursor.close()

        # Display the user's information
        label_username.config(text=f"Username: {user_data[0]}")
        label_password.config(text=f"Password: {'*' * len(user_data[1])}")
        label_first_name.config(text=f"First Name: {user_data[2]}")
        label_last_name.config(text=f"Last Name: {user_data[3]}")
        label_phone_number.config(text=f"Phone Number: {user_data[4]}")
        label_email.config(text=f"Email: {user_data[5]}")
        label_address.config(text=f"Address: {user_data[6]}")
        label_city.config(text=f"City: {user_data[7]}")
        label_country.config(text=f"Country: {user_data[8]}")

    def update_profile_window():
        # Create a new window for updating the profile
        update_window = tk.Toplevel(window)
        update_window.title("Update Profile")
        update_window.configure(bg="white")

        # Calculate the center position of the screen
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        window_width = 300
        window_height = 200
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window size and position
        update_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Create and place the input field for updating the profile
        entry_update = tk.Entry(update_window)
        entry_update.pack(pady=10)
        options = ["Username", "Password", "First Name", "Last Name", "Phone Number", "Email", "Address", "City", "Country"]
        var = tk.StringVar()
        var.set(options[0])
        dropdown_menu = tk.OptionMenu(update_window, var, *options)
        dropdown_menu.pack(pady=20)

        def update_profile():
            new_value = entry_update.get()
            # Determine the selected option and update the corresponding field in the database
            if var.get() == options[0]:
                cursor = connection.cursor()
                query = "UPDATE users SET username = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_username.config(text=f"Username: {new_value}")

            elif var.get() == options[1]:
                cursor = connection.cursor()
                query = "UPDATE users SET pwd = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_password.config(text=f"Password: {'*' * len(new_value)}")

            elif var.get() == options[2]:
                cursor = connection.cursor()
                query = "UPDATE users SET firstname = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_first_name.config(text=f"First Name: {new_value}")

            elif var.get() == options[3]:
                cursor = connection.cursor()
                query = "UPDATE users SET lastname = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_last_name.config(text=f"Last Name: {new_value}")

            elif var.get() == options[4]:
                cursor = connection.cursor()
                query = "UPDATE users SET phone = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_phone_number.config(text=f"Phone Number: {new_value}")

            elif var.get() == options[5]:
                cursor = connection.cursor()
                query = "UPDATE users SET mail = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_email.config(text=f"Email: {new_value}")

            elif var.get() == options[6]:
                cursor = connection.cursor()
                query = "UPDATE users SET address = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_address.config(text=f"Address: {new_value}")
            
            elif var.get() == options[7]:
                cursor = connection.cursor()
                query = "UPDATE users SET city = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_city.config(text=f"City: {new_value}")
            
            elif var.get() == options[8]:
                cursor = connection.cursor()
                query = "UPDATE users SET country = %s WHERE username = %s"
                cursor.execute(query, (new_value, current_user))
                connection.commit()
                cursor.close()
                label_country.config(text=f"Country: {new_value}")

            # Close the update window
            update_window.destroy()

        # Create and place the update button
        btn_update = tk.Button(update_window, text="Update", command=update_profile)
        btn_update.pack()

    def delete_account():
        # Confirm account deletion with a message box
        confirm = messagebox.askyesno("Confirm Account Deletion", "Are you sure you want to delete your account?")

        if confirm:
            # Delete the user's account from the database
            cursor = connection.cursor()
            query = "DELETE FROM users WHERE username = %s"
            cursor.execute(query, (current_user,))
            connection.commit()
            cursor.close()

            # Show a message box confirming account deletion
            messagebox.showinfo("Account Deleted", "Your account has been successfully deleted.")

            # Close the application
            window.destroy()
            from homepage import first_hp
            first_hp(connection, "")

    def logout():
        # Close the application
        window.destroy()
        from homepage import first_hp
        first_hp(connection, "")

    def prevo():
        prev_ord(connection, current_user)

    # Create the main window
    window = tk.Tk()
    window.title("Profile")
    window.configure(bg="#ffffff")
    window.state('normal')
    window.attributes('-zoomed', True)

    # Calculate the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()


    # Create and place the logo
    logo_img = tk.PhotoImage(file="img/logo.png", master=window)
    label_logo = tk.Label(window, image=logo_img, bg="white")
    label_logo.pack(pady=40)


    btn_orders = tk.Button(window, text="Orders", command=prevo, bg="#ff80ab")
    btn_orders.place(x=screen_width-100, y=20)

    btn_shop = tk.Button(window, text="Shop", command=home, bg="#ff80ab")
    btn_shop.place(x=20, y=20)

    # Create and place the labels to display user information
    label_username = tk.Label(window, text="Username: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_username.pack(pady=(10, 5))

    label_password = tk.Label(window, text="Password: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_password.pack(pady=(0, 5))

    label_first_name = tk.Label(window, text="First Name: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_first_name.pack(pady=(0, 5))

    label_last_name = tk.Label(window, text="Last Name: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_last_name.pack(pady=(0, 5))

    label_phone_number = tk.Label(window, text="Phone Number: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_username.pack(pady=(0, 5))

    label_email = tk.Label(window, text="Email: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_email.pack(pady=(0, 5))

    label_address = tk.Label(window, text="Address: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_address.pack(pady=(0, 5))

    label_city = tk.Label(window, text="City: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_city.pack(pady=(0, 5))

    label_country = tk.Label(window, text="Country: ", font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
    label_country.pack(pady=(0, 5))


    # Set the column and row weights to make the label centered
    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1, minsize=100)
    window.grid_rowconfigure(2, weight=1)
    # Display the user's profile information
    show_profile()

    # Create and place the buttons for updating, logging out, and deleting the profile
    btn_update = tk.Button(window, text="Update", command=update_profile_window, bg="#ff80ab")
    btn_update.place(x=screen_width//2 - 110, y=screen_height- 200)

    btn_logout = tk.Button(window, text="Logout", command=logout, bg="#ff80ab")
    btn_logout.place(x=screen_width//2 - 20, y=screen_height-200)

    btn_delete = tk.Button(window, text="Delete", command=delete_account, bg="#ff80ab")
    btn_delete.place(x=screen_width//2 + 70, y=screen_height-200)

    # Run the main window loop
    window.mainloop()



