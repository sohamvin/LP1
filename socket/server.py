import socket
import threading

# Function to handle each client connection
def handle_client(client_socket):
    # Receive the client's message
    message = client_socket.recv(1024).decode('utf-8')
    print(f"Received message: {message}")

    # Send the same message back to the client (echo)
    client_socket.send(message.encode('utf-8'))

    # Close the client connection
    client_socket.close()

# Main server function
def start_server():
    # Define host and port
    host = '127.0.0.1'  # Localhost
    port = 12345        # Any available port

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((host, port))

    # Listen for incoming connections (maximum of 5 clients in the queue)
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    # Accept connections and start a new thread for each client
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# Start the server
if __name__ == "__main__":
    start_server()
