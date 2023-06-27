import tkinter as tk
from tkinter import messagebox

def update_choice():
    selected_option = var.get()
    messagebox.showinfo("Selection", f"You selected: {selected_option}")

window = tk.Tk()
window.title("Dropdown Menu")

# Define the options for the dropdown menu
options = ["Option 1", "Option 2", "Option 3"]

# Create a variable to store the selected option
var = tk.StringVar(window)
var.set(options[0])  # Set the initial value

# Create the dropdown menu
dropdown_menu = tk.OptionMenu(window, var, *options)
dropdown_menu.pack(pady=20)

# Create the button to update the choice
button = tk.Button(window, text="Update Choice", command=update_choice)
button.pack()

window.mainloop()
