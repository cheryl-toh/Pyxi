import socket
import threading
from Automation import common, spotify, basic  # Adjust imports as needed

server_socket = None
running = False

def start_server(host='0.0.0.0', port=12345):
    global server_socket, running

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print("Server started. Listening for incoming connections...")
        running = True

        while running:
            client_socket, addr = server_socket.accept()
            print(f"Connection established with {addr}")
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()

    except Exception as e:
        print(f"Error starting server: {e}")
        running = False
        if server_socket:
            server_socket.close()

def handle_client(client_socket, addr):
    try:
        while True:
            user_input = client_socket.recv(1024).decode().strip()
            print(f"Received input from {addr}: {user_input}")

            if not user_input:
                print(f"Connection closed by {addr}")
                break

            elif user_input.lower() == "stop":
                stop_server()
                break

            elif user_input.lower().startswith("open"):
                app_name = user_input[4:].strip()
                common.start_app(app_name)

            elif user_input.lower().startswith("play"):
                if user_input.lower() == "play me a song":
                    spotify.open_and_play()
                else:
                    song_name = user_input[4:].strip()
                    spotify.search_and_play(song_name)

            elif user_input.lower() == "screenshot":
                basic.screenshot()

            elif user_input.lower() == "record":
                basic.screen_record()

            elif user_input.lower() == "shutdown":
                basic.laptop("shutdown")

            elif user_input.lower() == "sleep":
                basic.laptop("sleep")
            elif user_input.lower() == "restart":
                basic.laptop("restart")
            

    except Exception as e:
        print(f"Error handling client {addr}: {e}")

    finally:
        client_socket.close()
        print(f"Connection closed with {addr}")

def stop_server():
    global running, server_socket

    try:
        running = False
        if server_socket:
            server_socket.close()
            print("Server stopped.")
    except Exception as e:
        print(f"Error stopping server: {e}")

