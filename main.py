# frontend.py

import socket
from tkinter import messagebox
import tkinter as tk
from customtkinter import *
import threading
from Server import server

server_running = False

def start_server():
    global server_running

    server_running = True
    update_button_state()
    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.start_server)
    server_thread.daemon = True  # Daemonize the thread so it exits when the main thread exits
    server_thread.start()
    messagebox.showinfo("Server Started", "Server started successfully!")

def stop_server():
    global server_running

    try:
        server_running = False
        update_button_state()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", 12345))  # Connect to the server
        client_socket.send("stop".encode())  # Send the "stop" command
        client_socket.close()
        messagebox.showinfo("Server Stopped", "Server stopped successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to stop server: {e}")
    # Send "stop" command to the server
    # Here, you need to implement the logic to send the "stop" command to the server
    # For this example, I'll just print a message
    print("Stop server button clicked")

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
