import socket
from tkinter import messagebox
import tkinter as tk
from customtkinter import *
import threading
from Server import server

server_running = False
server_thread = None  # Global variable to hold the server thread

def start_server():
    global server_running, server_thread

    if server_running:
        messagebox.showinfo("Server Already Running", "Server is already running!")
        return

    try:
        server_thread = threading.Thread(target=start_server_thread)
        server_thread.daemon = True  # Daemonize the thread so it exits when the main thread exits
        server_thread.start()
        server_running = True
        update_button_state()
        messagebox.showinfo("Server Started", "Server started successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start server: {e}")

def start_server_thread():
    server.start_server()

def stop_server():
    global server_running, server_thread

    if not server_running:
        messagebox.showinfo("Server Not Running", "Server is not running!")
        return

    try:
        server.stop_server()
        server_thread.join()  # Wait for the server thread to complete
        server_running = False
        update_button_state()
        messagebox.showinfo("Server Stopped", "Server stopped successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop server: {e}")

def update_button_state():
    if server_running:
        start_button.configure(state='disabled')
        stop_button.configure(state='normal')
    else:
        start_button.configure(state='normal')
        stop_button.configure(state='disabled')

# Create the main window
root = CTk()
root._state_before_windows_set_titlebar_color = 'zoomed'
root.title("Server Control")

# # Set window size and position
root.geometry("400x200")

# Set background image
bg_image = tk.PhotoImage(file="Images\\background.png")
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

set_appearance_mode("dark")

# Create Start Server button
start_button = CTkButton(master=root, text="Start Server", height=50, width=150, corner_radius=10, command=start_server)
start_button.place(relx=0.45, rely=0.5, anchor="center")

# Create Stop Server button
stop_button = CTkButton(root, text="Stop Server", height=50, width=150, corner_radius=10, command=stop_server)
stop_button.place(relx=0.6, rely=0.5, anchor="center")

root.mainloop()
