from tkinter import Tk, Button, Label, Frame, Canvas, Scrollbar
from PIL import Image, ImageTk
from login import *
from signup import *
from profile import *
from releasedalbums import *

def first_hp(connection, username):
    def lg():
        root.destroy()
        login(connection)

    def sp():
        root.destroy()
        signup(connection)

    def pf():
        root.destroy()
        prof(connection, username)

    def relalb():
        root.destroy()
        albums(connection, username, 0)

    def prealb():
        root.destroy()
        albums(connection, username, 1)

    # Create the main window
    root = Tk()
    root.title("Home Page")
    root.attributes("-zoomed", True)  # Maximize the window

    # Set the color scheme
    root.configure(bg="white")

    # Create a frame for the buttons
    button_frame = Frame(root, bg="white")
    button_frame.pack(side="top", padx=10, pady=10)

    # Create a frame to hold the content
    content_frame = Frame(root, bg="white")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Load the banner image
    banner_image = Image.open("img/logo.png")
    banner_image = banner_image.resize((360, 360))
    banner_photo = ImageTk.PhotoImage(banner_image)

    # Load image1 and resize to 6x6 cm
    image1 = Image.open("img/image1.jpg")
    image1 = image1.resize((360, 360))  # Adjust the size to 6x6 cm
    photo1 = ImageTk.PhotoImage(image1)

    # Load image2 and resize to 6x6 cm
    image2 = Image.open("img/image2.jpg")
    image2 = image2.resize((360, 360))  # Adjust the size to 6x6 cm
    photo2 = ImageTk.PhotoImage(image2)

    if username == "":
        # Create the login button
        login_button = Button(button_frame, text="Login", command=lg, bg="#ff80ab", fg="white")
        login_button.pack(side="left", padx=5, pady=5)

        # Create the signup button
        signup_button = Button(button_frame, text="Signup", command=sp, bg="#ff80ab", fg="white")
        signup_button.pack(side="right", padx=5, pady=5)
    else:
        username_label=tk.Label(button_frame, text="Hello, {0}!".format(username), font=("Arial", 16), bg="white")
        username_label.pack(side="top", padx=5, pady=5)
        profile_button = Button(button_frame, text="Profile", command=pf, bg="pink")
        profile_button.pack(side="top", padx=5, pady=5)


    # Create the banner label
    banner_label = Label(content_frame, image=banner_photo, bg="white")
    banner_label.pack(pady=10, padx=10, fill="x")

    # Create a frame for image labels and buttons
    images_frame = Frame(content_frame, bg="white")
    images_frame.pack(pady=10)


    label1=tk.Label(images_frame, text="Released Albums", font=("Arial", 16), bg="white")
    label1.grid(padx=5, pady=5)
    # Create the image labels and buttons
    image1_label = Label(images_frame, image=photo1, bg="white")
    image1_label.grid(row=1, column=0, padx=10)
    button1 = Button(images_frame, text="Go", command=relalb, bg="#ff80ab", fg="white")
    button1.grid(row=2, column=0, pady=5)

    label2=tk.Label(images_frame, text="Preorder Albums", font=("Arial", 16), bg="white")
    label2.grid(row=0, column=1, padx=5, pady=5)
    image2_label = Label(images_frame, image=photo2, bg="white")
    image2_label.grid(row=1, column=1, padx=10)
    button2 = Button(images_frame, text="Go", command=prealb, bg="#ff80ab", fg="white")
    button2.grid(row=2, column=1, pady=5)

    # Run the Tkinter event loop
    root.mainloop()
