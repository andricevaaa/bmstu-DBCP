from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
from prof import *

def show_basket(apg_ids, conn, username, inx):
    # Create a cursor object
    cur = conn.cursor()

    # Create a new window for the basket page
    basket_window = Tk()
    basket_window.title("Basket")
    basket_window.state('normal')  # Maximize the window
    basket_window.attributes("-zoomed", True)

    # Create a canvas for the scrollable area
    canvas = Canvas(basket_window, bg="white")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a scrollbar
    scrollbar = Scrollbar(basket_window, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Configure the canvas to use the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Create a frame to hold the album information
    frame = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Create a label for the total price
    total_price_label = Label(basket_window, text="Total Price: $0.00", bg="white", font=("Arial", 16))
    total_price_label.pack(anchor="e", padx=20, pady=20)

    # Create a function to update the total price label
    def update_total_price():
        total_price = sum(album['price'] for album in albums)
        total_price_label.config(text="Total Price: ${:.2f}".format(total_price))

    # Retrieve album information from the database based on apg IDs
    albums = []
    podorder = []
    for apg_id in apg_ids:
        cur.execute("""
            SELECT a.albumid, a.albumname, a.albumver, a.price, a.qleft, g.pcname
            FROM apg ag
            INNER JOIN album a ON ag.albumid = a.albumid
            INNER JOIN gift g ON ag.giftid = g.giftid
            WHERE ag.apgid = %s
        """, (apg_id,))
        album_info = cur.fetchone()
        if album_info:
            album_id, album_name, version, price, qleft, pc_name = album_info
            albums.append({
                'apg_id': apg_id,
                'album_id': album_id,
                'album_name': album_name,
                'version': version,
                'price': price,
                'qleft': qleft,
                'pc_name': pc_name
            })

    # Create album thumbnails, labels, and price labels
    albums_per_row = 7
    for i, album in enumerate(albums):
        apg_id = album['apg_id']
        album_id = album['album_id']
        album_name = album['album_name']
        version = album['version']
        price = album['price']
        qleft = album['qleft']
        pc_name = album['pc_name']

        # Create a frame for each album
        album_frame = Frame(frame, bg="white")
        album_frame.grid(row=i // albums_per_row, column=i % albums_per_row, padx=20, pady=20)

        # Load and display album thumbnail
        image_file = 'img/albums/' + album_name + '.jpg'
        image = Image.open(image_file)
        image = image.resize((100, 100), Image.ANTIALIAS)
        thumbnail = ImageTk.PhotoImage(image)
        thumbnail_label = Label(album_frame, image=thumbnail, borderwidth=2, relief="solid")
        thumbnail_label.image = thumbnail
        thumbnail_label.pack(side=TOP)

        # Create label for album name and version
        if version == 'null':
            album_label = Label(album_frame, text=album_name, bg="white", font=("Arial", 14))
        else:
            album_label = Label(album_frame, text="{} (Version: {})".format(album_name, version), bg="white",
                                font=("Arial", 14))
        album_label.pack(side=TOP)

        # Create label for PC name
        pc_label = Label(album_frame, text="PC: {}".format(pc_name), bg="white", font=("Arial", 12))
        pc_label.pack(side=TOP)

        # Create label for album price
        price_label = Label(album_frame, text="${:.2f}".format(price), bg="white", font=("Arial", 14))
        price_label.pack(side=TOP)

        # Function to handle the "Remove" button click
        def remove_album(album_frame, apg_id, price):
            apg_ids.remove(apg_id)
            album_frame.destroy()
            update_total_price()
            # Remove the album's price from the total price
            total_price_label.config(
                text="Total Price: ${:.2f}".format(float(total_price_label.cget("text").split("$")[1]) - price))

        # Create a "Remove" button
        remove_button = Button(album_frame, text="Remove", bg="pink", fg="white", font=("Arial", 12), padx=10, pady=5,
                               relief="solid", bd=0, command=lambda af=album_frame, aid=apg_id, p=price: remove_album(
                af, aid, p))
        remove_button.pack(side=TOP)

        # Check album availability
        if qleft == 0:
            album_label.config(fg="red")
            price_label.config(fg="red")
            apg_ids.remove(apg_id)
            podorder.append(apg_id)

    # Update the total price label
    update_total_price()

    # Function to handle the "Buy" button click
    def buy_albums():
        # Create a new order in the database
        order_date = datetime.date.today()
        if not inx:
            create_order(conn, username, order_date, apg_ids, "normal")
        else:
            create_order(conn, username, order_date, apg_ids, "preorder")
        if podorder:
            create_order(conn, username, order_date, podorder, "addorder")
         # Update the qbought and qleft values for each bought album
        for apg_id in apg_ids:
            cur.execute("CALL update_album_qbought(%s)", (apg_id,))
        for addod in podorder:
            cur.execute("CALL update_podorder_qbought(%s)", (addod,))
        conn.commit()
        messagebox.showinfo("Buy Albums", "Albums successfully purchased!")
        basket_window.destroy()
        prof(conn, username)

    # Create a "Buy" button
    buy_button = Button(basket_window, text="Buy", bg="pink", fg="white", font=("Arial", 16), padx=20, pady=10,
                        relief="solid", bd=0, command=buy_albums)
    buy_button.pack(anchor="e", padx=20, pady=20)

    # Run the mainloop for the basket window
    basket_window.mainloop()


def create_order(conn, username, order_date, apg_ids, order_type):
    # Create a cursor object
    cur = conn.cursor()

    # Get the next order ID
    cur.execute("SELECT MAX(orderid) FROM orders")
    max_order_id = cur.fetchone()[0]
    if max_order_id is None:
        order_id = 1
    else:
        order_id = max_order_id + 1

    # Insert the order into the orders table
    cur.execute("INSERT INTO orders (orderid, orderdate, ordertype) VALUES (%s, %s, %s)",
                (order_id, order_date, order_type))

    cur.execute("SELECT MAX(ordalbid) FROM ordalb")
    max_ordalb_id = cur.fetchone()[0]
    if max_ordalb_id is None:
        ordalb_id = 1
    else:
        ordalb_id = max_ordalb_id + 1

    # Insert the album-order mapping into the ordalb table
    for apg_id in apg_ids:
        cur.execute("INSERT INTO ordalb (ordalbid, orderid, apg, username) VALUES (%s, %s, %s, %s)",
                    (ordalb_id, order_id, apg_id, username))
        ordalb_id += 1

    # Commit the changes to the database
    conn.commit()