from tkinter import *
from PIL import ImageTk, Image
from datetime import date
from prof import *
from basket import *
from login import *

def albums(conn, username, inx):
    bskt = []
    # Create a cursor object
    cur = conn.cursor()
    def prfl():
        root.destroy()
        prof(conn, username)

    def show_album_info(album_name):
        # Create a cursor object
        cur = conn.cursor()

        # Retrieve album information from the database based on album name
        cur.execute("SELECT albumid, artistid, albumname, albumver, price, releasedate, country, company FROM album WHERE albumname = %s", (album_name,))
        album_info = cur.fetchall()

        # Close the cursor and connection

        if album_info:
            # Create a popup window
            popup = Toplevel()
            popup.title("Album Information")

            # Load and display album image
            album_id, artist_name, album_name, album_ver, price, release_date, country, company = album_info[0]
            image_file = 'img/albums/' + album_name + '.jpg'
            image = Image.open(image_file)
            image = image.resize((200, 200), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            album_image_label = Label(popup, image=photo)
            album_image_label.pack(side=LEFT, padx=10, pady=10)
            album_image_label.image = photo

            # Create album information labels
            album_name_label = Label(popup, text="Album Name: " + album_name)
            album_name_label.pack(anchor="w", padx=10, pady=5)

            artist_name_label = Label(popup, text="Artist Name: " + artist_name)
            artist_name_label.pack(anchor="w", padx=10, pady=5)

            price_label = Label(popup, text="Price: $" + str(price))
            price_label.pack(anchor="w", padx=10, pady=5)

            release_date_label = Label(popup, text="Release Date: " + str(release_date))
            release_date_label.pack(anchor="w", padx=10, pady=5)

            country_label = Label(popup, text="Country: " + country)
            country_label.pack(anchor="w", padx=10, pady=5)

            company_label = Label(popup, text="Company: " + company)
            company_label.pack(anchor="w", padx=10, pady=5)

            # Create dropdown menu to choose album versionž
            if str(album_info[0][3]) == 'null':
                versions = [album_name]
            else:
                versions = [str(album[3]) for album in album_info]
            version_var = StringVar()
            version_var.set(versions[0])
            version_dropdown = ttk.Combobox(popup, textvariable=version_var, values=versions)
            version_dropdown.pack(anchor="w", padx=10, pady=5)

            cur.execute("SELECT g.pcname FROM gift g INNER JOIN apg a ON g.giftid = a.giftid WHERE a.albumid = %s", (album_id,))
            pc_info = [row[0] for row in cur.fetchall()]
            pc_var = StringVar()
            pc_var.set(pc_info[0])
            pc_dropdown = ttk.Combobox(popup, textvariable=pc_var, values=pc_info)
            pc_dropdown.pack(anchor="w", padx=10, pady=5)

            if username != "":
                # Create a button
                button = Button(popup, text="Add to Basket", command=lambda: add_to_basket(album_name, version_var.get(), pc_var.get()))
                button.pack(side=RIGHT, padx=10, pady=10)

            # Function to add the album to the basket
            def add_to_basket(album_name, version, pc_name):
                # Add the album to the basket
                if version != album_name:
                    cur.execute("SELECT albumid FROM album WHERE albumname = %s AND albumver = %s", (album_name, version,))
                else:
                    cur.execute("SELECT albumid FROM album WHERE albumname = %s", (album_name,))
                album_id = cur.fetchall()[0][0]
                cur.execute("""
                    SELECT a.apgid
                    FROM apg a
                    INNER JOIN gift g ON a.giftid = g.giftid
                    WHERE a.albumid = %s AND g.pcname = %s
                """, (album_id, pc_name))
                bskt.append(cur.fetchall()[0][0])
                messagebox.showinfo("Basket", "Album: {} (Version: {}) added to basket!".format(album_name, version))

        else:
            messagebox.showerror("Error", "Album information not found.")
        # Create the root window
    root = Tk()
    root.title("Album Page")
    root.attributes("-zoomed", True)  # Maximize the window
    root.configure(bg="white")

    # Create a canvas with a scrollbar
    canvas = Canvas(root)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    canvas.configure(bg="white")

    # Create a frame inside the canvas
    frame = Frame(canvas)
    frame.pack(side=TOP, padx=10, pady=10)
    frame.configure(bg="white")

    # Configure the scrollbar
    scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    button_frame = Frame(root, bg="white")
    button_frame.pack(side="top", padx=10, pady=10)

    # Create the basket button
    def bkt():
        root.destroy()
        show_basket(bskt, conn, username, inx)
    if username != "":
        basket_button = Button(button_frame, text="Basket", command=bkt)
        basket_button.pack(side="right", padx=10, pady=10)

    # Create the profile button
    if username != "":
        profile_button = Button(button_frame, command=prfl, text="Profile")
        profile_button.pack(side="right", padx=10, pady=10)
    else:
        def lgn():
            root.destroy()
            login(conn)
        profile_button = Button(button_frame, command=lgn, text="LogIn")
        profile_button.pack(side="right", padx=10, pady=10)



    # Get today's date
    today = date.today()

    if inx:
        # Retrieve album data from the database
        cur.execute("SELECT DISTINCT ON (albumname) albumname FROM album WHERE releasedate > %s", (today,))
    else:
        cur.execute("SELECT DISTINCT ON (albumname) albumname FROM album WHERE releasedate < %s", (today,))
    albums = cur.fetchall()
    row = 0
    col = 0

    # Create album buttons
    for album in albums:
        album_name = album[0]

        album_button = Button(frame, text=album_name)

        # Load and display album image
        image = Image.open('img/albums/' + album_name + '.jpg')
        image = image.resize((200, 200), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        album_button.config(image=photo, width=200, height=210, compound="top", command=lambda name=album_name: show_album_info(name))
        album_button.image = photo

        # Position the album button
        album_button.grid(row=row+1, column=col, padx=5, pady=10)

        col += 1

        # Move to the next row after 3 columns
        if col > 6:
            col = 0
            row += 2

    # Close the cursor and connection
    cur.close()
    root.mainloop()