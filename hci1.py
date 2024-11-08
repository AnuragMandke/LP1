import tkinter as tk
from tkinter import messagebox

# Create the main application window
window = tk.Tk()
window.title("Simple User Interface")
window.geometry("300x200")

# Function to display greeting message
def display_greeting():
    user_name = name_entry.get()
    if user_name:
        greeting_label.config(text=f"Hello, {user_name}!")
    else:
        messagebox.showwarning("Input Error", "Please enter your name!")

# Create a label asking for the user's name
name_label = tk.Label(window, text="Enter your name:")
name_label.pack(pady=10)

# Create a text entry widget for user input
name_entry = tk.Entry(window, width=30)
name_entry.pack(pady=5)

# Create a button that triggers the display_greeting function
submit_button = tk.Button(window, text="Submit", command=display_greeting)
submit_button.pack(pady=10)

# Create a label to display the greeting message
greeting_label = tk.Label(window, text="")
greeting_label.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
