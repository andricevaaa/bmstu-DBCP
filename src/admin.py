import tkinter as tk
from tkinter import ttk, messagebox

def admin(conn):
    cur = conn.cursor()

    def fetch_all_albums(order_by):
        query = """
            SELECT * FROM Album ORDER BY {0};
            """.format(order_by)
        cur.execute(query)
        all_albums = cur.fetchall()
        return all_albums

    def add_album():
        def validate_add():
            # Get the values from the input fields
            albumid = input_fields[0][1].get()
            artistid = input_fields[1][1].get()
            albumname = input_fields[2][1].get()
            albumver = input_fields[3][1].get()
            price = input_fields[4][1].get()
            releasedate = input_fields[5][1].get()
            qbought = input_fields[6][1].get()
            qleft = input_fields[7][1].get()
            company = input_fields[8][1].get()
            country = input_fields[9][1].get()

            # Perform validation
            if not albumid or not artistid or not albumname or not albumver or not price or not releasedate or not qbought or not qleft or not company or not country:
                messagebox.showerror("Error", "All fields are required.")
            else:
                try:
                    # Insert the new user data into the database
                    cursor = conn.cursor()
                    query = "INSERT INTO Album (albumid, artistid, albumname, albumver, price, releasedate, qbought, qleft, company, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(query, (albumid, artistid, albumname, albumver, price, releasedate, qbought, qleft, company, country))
                    conn.commit()
                    messagebox.showinfo("Success", "Album added succsessfully")
                    tree.delete(*tree.get_children())
                    all_albums = fetch_all_albums("AlbumID")
                    display_albums(all_albums)
                    update_window.destroy()
                except:
                    messagebox.showerror("Error", "That album already exists")
        
        update_window = tk.Toplevel(window)
        update_window.title("Add Album")
        update_window.configure(bg="white")

        # Calculate the center position of the screen
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        window_width = 400
        window_height = 420
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set the window size and position
        update_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        frame_inputs = tk.Frame(update_window, bg="white")
        frame_inputs.pack()

        # Create and place the input fields
        input_fields = [
            ("AlbumID", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Artist", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Album Name", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Album Version", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Price", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Release Date", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Quantity Bought", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Qouantity Left", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Company", tk.Entry(frame_inputs, font=("Arial", 12))),
            ("Country", tk.Entry(frame_inputs, font=("Arial", 12)))
        ]

        for i, (label_text, entry) in enumerate(input_fields):
            label = tk.Label(frame_inputs, text=label_text, font=("Arial", 12), bg="#ffffff", fg="#ff80ab")
            label.grid(row=i, column=0, padx=10, pady=5)
            entry.grid(row=i, column=1, padx=10, pady=5)
        
        btn_add = tk.Button(update_window, text="Add", command=validate_add, font=("Arial", 12), bg="#ff80ab", fg="#ffffff", relief="flat")
        btn_add.pack(pady=20, ipadx=30, ipady=5)

    def delete_album(album_id):
        query1 = """
            DELETE FROM Album
            WHERE AlbumID = %s;
        """
        query2 = """
            DELETE FROM apg
            WHERE AlbumID = %s;
        """
        cur.execute(query2, (album_id,))
        cur.execute(query1, (album_id,))
        conn.commit()
        tree.delete(*tree.get_children())
        all_albums = fetch_all_albums("AlbumID")
        display_albums(all_albums)

    def add_gift(album_id):
        update_window = tk.Toplevel(window)
        update_window.title("Add Gift")
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
        def updt():
            new_value = entry_update.get()
            cur.execute("SELECT MAX(apgid) FROM apg")
            max_apg_id = cur.fetchone()[0]
            if max_apg_id is None:
                apg_id = 1
            else:
                apg_id = max_apg_id + 1
            cur.execute("""SELECT pcname FROM gift WHERE giftid = %s""", (new_value,))
            try:
                gift = cur.fetchone()[0]
                cur.execute("INSERT INTO apg (apgid, albumid, giftid) VALUES (%s, %s, %s)",
                            (apg_id, album_id, new_value))
                conn.commit()
                update_window.destroy()
            except:
                messagebox.showerror("Error", "That gift doesn't exist")
        # Create and place the update button
        btn_update = tk.Button(update_window, text="Update", command=updt)
        btn_update.pack()
    
    def add_pc():
        update_window = tk.Toplevel(window)
        update_window.title("Add PC")
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
        def updt():
            new_value = entry_update.get()
            cur.execute("SELECT MAX(giftid) FROM gift")
            max_gift_id = cur.fetchone()[0]
            if max_gift_id is None:
                gift_id = 1
            else:
                gift_id = max_gift_id + 1
            try:
                cur.execute("INSERT INTO gift (giftid, pcname) VALUES (%s, %s)",
                            (gift_id, new_value))
                conn.commit()
                update_window.destroy()
            except:
                messagebox.showerror("Error", "That gift doesn't exist")
        # Create and place the update button
        btn_update = tk.Button(update_window, text="Add", command=updt)
        btn_update.pack()

    def edit_album(album_id):
        # Create a new window for updating the profile
        update_window = tk.Toplevel(window)
        update_window.title("Update Album")
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
        options = ["ID", "Artist", "Name", "Version", "Price", "Release Date", "Quantity Bought", "Quantity Left", "Company", "Country"]
        var = tk.StringVar()
        var.set(options[0])
        dropdown_menu = tk.OptionMenu(update_window, var, *options)
        dropdown_menu.pack(pady=20)

        def update_album():
            new_value = entry_update.get()
            # Determine the selected option and update the corresponding field in the database
            if var.get() == options[0]:
                query1 = """
                    UPDATE Albums
                    SET albumid = %s
                    WHERE albumid =  %s;
                """
                query2 = """
                    UPDATE apg
                    SET albumid = %s
                    WHERE albumid = %s;
                """
                cur.execute(query1, (new_value, album_id))
                cur.execute(query2, (new_value, album_id))
                conn.commit()
            elif var.get() == options[1]:
                query = """
                    UPDATE Album
                    SET artistid = %s
                    WHERE albumid =  %s;
                """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[2]:
                query = """UPDATE Album SET albumname = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[3]:
                query = """UPDATE Album SET albumver = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[4]:
                query = """UPDATE Album SET price = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[5]:
                query = """UPDATE Album SET releasedate = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[6]:
                query = """UPDATE Album SET qbought = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[7]:
                query = query = """UPDATE Album SET qleft = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[8]:
                query = """UPDATE Album SET company = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            elif var.get() == options[9]:
                query = """UPDATE Album SET country = %s WHERE albumid =  %s; """
                cur.execute(query, (new_value, album_id))
                conn.commit()
            update_window.destroy()
            tree.delete(*tree.get_children())
            all_albums = fetch_all_albums("AlbumID")
            display_albums(all_albums)

        # Create and place the update button
        btn_update = tk.Button(update_window, text="Update", command=update_album)
        btn_update.pack()

    window = tk.Tk()
    window.title("All Orders")
    window.state('normal')
    window.attributes('-zoomed', True)
    window.configure(bg="white")

    def sort_by_date():
        all_albums = fetch_all_albums("releasedate")
        display_albums(all_albums)
    
    def sort_by_price():
        all_albums = fetch_all_albums("price")
        display_albums(all_albums)

    def sort_by_id():
        all_albums = fetch_all_albums("AlbumID")
        display_albums(all_albums)

    def display_albums(albums):
        tree.delete(*tree.get_children())
        for album in albums:
            albumid, artistid, albumname, albumversion, price, releasedate, qbought, qleft, company, country = album
            tree.insert("", "end", values=(albumid, artistid, albumname, albumversion, price, releasedate, qbought, qleft, company, country))

    def logout():
        # Close the application
        window.destroy()
        from homepage import first_hp
        first_hp(conn, "")

    # Create the Treeview widget for the table
    tree = ttk.Treeview(window, show="headings", columns=("albumid", "artistid", "albumname", "albumversion", "price", "releasedate", "qbought", "qleft", "company", "country"))
    tree.heading("albumid", text="Album ID", command=sort_by_id)
    tree.heading("artistid", text="Artist")
    tree.heading("albumname", text="Name")
    tree.heading("albumversion", text="Version")
    tree.heading("price", text="Pricfe", command=sort_by_price)
    tree.heading("releasedate", text="Release Date", command=sort_by_date)
    tree.heading("qbought", text="Quantity Bought")
    tree.heading("qleft", text="Quantity Left")
    tree.heading("company", text="Company")
    tree.heading("country", text="Country")
    tree.pack(fill=tk.BOTH, expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="white",
                    foreground="#ed174f",
                    rowheight=25,
                    fieldbackground="white")
    style.map("Treeview", background=[("selected", "#ed174f")])

    # Fetch and display all orders
    all_albums = fetch_all_albums("albumid")
    display_albums(all_albums)

    # Buttons for editing and deleting orders
    add_button = tk.Button(window, text="Add Album", command=add_album, bg="#ff80ab", fg="white")
    edit_button = tk.Button(window, text="Edit Album", command=lambda: edit_album(tree.item(tree.focus())["values"][0]), bg="#ff80ab", fg="white")
    delete_button = tk.Button(window, text="Delete Album", command=lambda: delete_album(tree.item(tree.focus())["values"][0]), bg="#ff80ab", fg="white")
    connect_button = tk.Button(window, text="Connect Gift to Album", command=lambda: add_gift(tree.item(tree.focus())["values"][0]), bg="#ff80ab", fg="white")
    addpc_button = tk.Button(window, text="Add New Gift", command=add_pc, bg="#ff80ab", fg="white")
    logout_button = tk.Button(window, text="Logout", command=logout, bg="#ff80ab", fg="white")

    add_button.pack(side=tk.LEFT, padx=10, pady=10)
    edit_button.pack(side=tk.LEFT, padx=10, pady=10)
    delete_button.pack(side=tk.LEFT, padx=10, pady=10)
    connect_button.pack(side=tk.LEFT, padx=10, pady=10)
    addpc_button.pack(side=tk.LEFT, padx=10, pady=10)
    logout_button.pack(side=tk.LEFT, padx=10, pady=10)
    window.mainloop()
    # Close the database connection
    cur.close()