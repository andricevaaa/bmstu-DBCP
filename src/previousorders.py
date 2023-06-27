import tkinter as tk
from tkinter import ttk

def prev_ord(conn, username):
    cur = conn.cursor()

    def fetch_previous_orders():
        query = """
            SELECT o.orderid, o.orderdate, o.ordertype, a.albumname, a.albumver, g.pcname
            FROM ordalb oa
            INNER JOIN orders o ON oa.orderid = o.orderid
            INNER JOIN apg p ON oa.apg = p.apgid
            INNER JOIN album a ON p.albumid = a.albumid
            INNER JOIN gift g ON p.giftid = g.giftid
            WHERE oa.username = %s;
        """
        cur.execute(query, (username,))
        previous_orders = cur.fetchall()
        return previous_orders

    window = tk.Tk()
    window.title("Previous Orders")

    # Create the Treeview widget for the table
    tree = ttk.Treeview(window)
    tree["columns"] = ("orderid", "date", "type", "album", "version", "gift")
    tree.heading("orderid", text="Order ID")
    tree.heading("date", text="Date")
    tree.heading("type", text="Type")
    tree.heading("album", text="Album")
    tree.heading("version", text="Version")
    tree.heading("gift", text="Gift")
    tree.pack()

    # Fetch and display the previous orders
    previous_orders = fetch_previous_orders()
    for order in previous_orders:
        order_id, order_date, order_type, album_name, album_version, gift_name = order
        tree.insert("", "end", values=(order_id, order_date, order_type, album_name, album_version, gift_name))

    window.mainloop()

    # Close the database connection
    cur.close()
