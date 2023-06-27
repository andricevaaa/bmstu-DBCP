import tkinter as tk
from tkinter import ttk
from datetime import *

def manager(conn):
    cur = conn.cursor()

    def fetch_all_orders(order_by):
        query = """
            SELECT oa.ordalbid, o.orderid, o.orderdate, o.ordertype, oa.username, a.albumname, a.albumver, g.pcname
            FROM ordalb oa
            INNER JOIN orders o ON oa.orderid = o.orderid
            INNER JOIN apg p ON oa.apg = p.apgid
            INNER JOIN album a ON p.albumid = a.albumid
            INNER JOIN gift g ON p.giftid = g.giftid
            ORDER BY {0};
            """.format(order_by)
        cur.execute(query)
        all_orders = cur.fetchall()
        return all_orders

    def delete_order(order_id):
        query1 = """
            DELETE FROM Orders
            WHERE orderid = %s;
        """
        query2 = """
            DELETE FROM OrdAlb
            WHERE orderid = %s;
        """
        cur.execute(query2, (order_id,))
        cur.execute(query1, (order_id,))
        conn.commit()
        tree.delete(*tree.get_children())
        all_orders = fetch_all_orders("orderdate")
        display_orders(all_orders)

    def edit_order(oa_id):
        # Create a new window for updating the profile
        update_window = tk.Toplevel(window)
        update_window.title("Update Order")
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
        options = ["Order Date", "Order Type", "Album"]
        var = tk.StringVar()
        var.set(options[0])
        dropdown_menu = tk.OptionMenu(update_window, var, *options)
        dropdown_menu.pack(pady=20)

        def update_order():
            new_value = entry_update.get()
            # Determine the selected option and update the corresponding field in the database
            if var.get() == options[0]:
                query = """
                    UPDATE Orders
                    SET orderdate = %s
                    WHERE orderid = (
                        SELECT orderid
                        FROM ordalb
                        WHERE ordalbid = %s
                    );
                """
                cur.execute(query, (new_value, oa_id))
                conn.commit()
            elif var.get() == options[1]:
                query = query = """
                    UPDATE Orders
                    SET ordertype = %s
                    WHERE orderid = (
                        SELECT orderid
                        FROM ordalb
                        WHERE ordalbid = %s
                    );
                """
                cur.execute(query, (new_value, oa_id))
                conn.commit()
            elif var.get() == options[2]:
                query = query = """UPDATE OrdAlb SET apg = %s WHERE ordalbid =  %s; """
                cur.execute(query, (new_value, oa_id))
                conn.commit()
            update_window.destroy()
            tree.delete(*tree.get_children())
            all_orders = fetch_all_orders("orderdate")
            display_orders(all_orders)

        # Create and place the update button
        btn_update = tk.Button(update_window, text="Update", command=update_order)
        btn_update.pack()

    window = tk.Tk()
    window.title("All Orders")
    window.state('normal')
    window.attributes('-zoomed', True)
    window.configure(bg="white")

    def sort_by_date():
        all_orders = fetch_all_orders("orderdate")
        display_orders(all_orders)
    
    def sort_by_username():
        all_orders = fetch_all_orders("oa.username")
        display_orders(all_orders)

    def display_orders(orders):
        tree.delete(*tree.get_children())
        for order in orders:
            apgid, order_id, order_date, order_type, username, album_name, album_version, gift_name = order
            tree.insert("", "end", values=(apgid, order_id, order_date, order_type, username, album_name, album_version, gift_name))

    def logout():
        # Close the application
        window.destroy()
        from homepage import first_hp
        first_hp(conn, "")


    # Create the Treeview widget for the table
    tree = ttk.Treeview(window, show="headings", columns=("apgid", "id", "date", "type", "username", "album", "version", "gift"))
    tree.heading("apgid", text="Album + Gift ID")
    tree.heading("id", text="Order ID")
    tree.heading("date", text="Date", command=sort_by_date)
    tree.heading("type", text="Type")
    tree.heading("username", text="Username", command=sort_by_username)
    tree.heading("album", text="Album")
    tree.heading("version", text="Version")
    tree.heading("gift", text="Gift")
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
    all_orders = fetch_all_orders("orderdate")
    display_orders(all_orders)

    # Get today's date and yesterday's date
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # Buttons for editing and deleting orders
    edit_button = tk.Button(window, text="Edit Order", command=lambda: edit_order(tree.item(tree.focus())["values"][0]), bg="#ff80ab", fg="white")
    delete_button = tk.Button(window, text="Delete Order", command=lambda: delete_order(tree.item(tree.focus())["values"][1]), bg="#ff80ab", fg="white")
    logout_button = tk.Button(window, text="Logout", command=logout, bg="#ff80ab", fg="white")

    tree.bind("<<TreeviewSelect>>", lambda event: enable_disable_buttons())
    # Check if the selected order was made today or yesterday to enable/disable the buttons
    def enable_disable_buttons():
        selected_order = tree.item(tree.focus())["values"]
        if selected_order:
            order_date = datetime.strptime(selected_order[2], "%Y-%m-%d").date()
            if order_date in (today, yesterday):
                edit_button.config(state="normal")
                delete_button.config(state="normal")
            else:
                edit_button.config(state="disabled")
                delete_button.config(state="disabled")
    

    edit_button.pack(side=tk.LEFT, padx=10, pady=10)
    delete_button.pack(side=tk.LEFT, padx=10, pady=10)
    logout_button.pack(side=tk.LEFT, padx=10, pady=10)
    window.mainloop()
    # Close the database connection
    cur.close()
