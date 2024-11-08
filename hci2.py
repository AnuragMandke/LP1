import tkinter as tk
from tkinter import ttk

def show_message(tab_name):
    message_label.config(text=f"You applied changes on the {tab_name} tab.")
    
def show_name(name):
    message_label.config(text = f"Welcome Back!")

def apply_theme():
    theme = theme_var.get()
    if theme == "Light":
        root.config(bg="white")
        for widget in root.winfo_children():
            widget.config(bg="white", fg="black")
    elif theme == "Dark":
        root.config(bg="black")
        for widget in root.winfo_children():
            widget.config(bg="black", fg="white")
    elif theme == "Blue":
        root.config(bg="light blue")
        for widget in root.winfo_children():
            widget.config(bg="light blue", fg="black")
    elif theme == "Yellow":
        root.config(bg="light yellow")
        for widget in root.winfo_children():
            widget.config(bg="light yellow", fg="white")    

    show_message("Preferences")

def apply_brightness(value):
    brightness = int(float(value))
    bg_color = f'#{brightness:02x}{brightness:02x}{brightness:02x}'
    root.config(bg=bg_color)
    for widget in root.winfo_children():
        widget.config(bg=bg_color)

    show_message("Settings")

root = tk.Tk()
root.title("Redesigned UI")
root.geometry("600x400")
root.config(bg="white") 

notebook = ttk.Notebook(root)


tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="User Info")


label1 = ttk.Label(tab1, text="Enter your name:")
label1.grid(column=0, row=0, padx=10, pady=10)

name_entry = ttk.Entry(tab1, width=30)
name_entry.grid(column=1, row=0, padx=10, pady=10)
name = name_entry.get()
print(name)

submit_button1 = ttk.Button(tab1, text="Submit", command=lambda: show_name(name))
submit_button1.grid(column=1, row=1, padx=10, pady=10)

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Preferences")

label2 = ttk.Label(tab2, text="Select your theme:")
label2.grid(column=0, row=0, padx=10, pady=10)

theme_var = tk.StringVar()
theme_dropdown = ttk.Combobox(tab2, textvariable=theme_var, values=["Light", "Dark", "Blue", "Yellow"], width=27)
theme_dropdown.grid(column=1, row=0, padx=10, pady=10)

apply_theme_button = ttk.Button(tab2, text="Apply Theme", command=apply_theme)
apply_theme_button.grid(column=1, row=1, padx=10, pady=10)

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Settings")

label3 = ttk.Label(tab3, text="Adjust screen brightness:")
label3.grid(column=0, row=0, padx=10, pady=10)

brightness_scale = ttk.Scale(tab3, from_=0, to=255, orient="horizontal", command=apply_brightness)
brightness_scale.grid(column=1, row=0, padx=10, pady=10)

message_label = tk.Label(root, text="", foreground="blue", bg="white")
message_label.pack(pady=20)

notebook.pack(expand=1, fill="both")

root.mainloop()
