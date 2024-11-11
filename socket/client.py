import socket

def start_client():
    # Define host and port to connect to
    host = '127.0.0.1'  # Server's IP address
    port = 12345        # The same port as the server

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    # Send a message to the server
    message = input("Enter a message to send to the server: ")
    client_socket.send(message.encode('utf-8'))

    # Receive the echoed message from the server
    echoed_message = client_socket.recv(1024).decode('utf-8')
    print(f"Received from server: {echoed_message}")

    # Close the connection
    client_socket.close()

# Start the client
if __name__ == "__main__":
    start_client()
