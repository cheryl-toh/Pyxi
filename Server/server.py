import sys
from Automation import common, spotify, basic
import socket
import subprocess

def start_server():
    host = '0.0.0.0'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Server started. Listening for incoming connections...")
    # Accept connection
    client_socket, addr = server_socket.accept()
    print("Connection established with", addr)

    running = True
    while running:
        # Handle client request
        running = handle_client_request(client_socket)

    server_socket.close()
    print("SERVER STOPPED. RUN START AGAIN")

def handle_client_request(client_socket):
    try:
        # Receive user input
        user_input = client_socket.recv(1024).decode()
        print("Received input:", user_input)

        # Execute corresponding script
        if user_input.lower().startswith("open"):
            print("Running open app function")
            app_name = user_input[4:].strip()
            common.start_app(app_name)

        elif user_input.lower().startswith("play"):
            print("In spotify function")
            if user_input.lower() != "play me a song":
                song_name = user_input[4:].strip()
                spotify.search_and_play(song_name)
            else:
                spotify.open_and_play()

        elif user_input.lower() == "screenshot":
            basic.screenshot()

        elif user_input.lower() == "record":
            basic.screen_record()

        elif user_input.lower() == "stop":
            print("client stopped the server")
            return False

        return True

    except Exception as e:
        print("Error occurred:", e)
        return False
        
