import socket
from flask import render_template

def clientFun(message):
    # Define the server address and port
    server_address = '127.0.0.1'
    server_port = 12345
        
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_address, server_port))

        # Send the message to the server
        client_socket.send(message.encode('utf-8'))

        # Receive the response from the server
        response = client_socket.recv(1024)
    except ConnectionRefusedError:
        response = b"Server is not available."

    finally:
        # Close the client socket
        client_socket.close()

    return render_template('index.html', message=message, response=response.decode('utf-8'))















# # Create a socket object
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Define the server address and port
# server_address = '127.0.0.1'
# server_port = 12345

# # Connect to the server
# client_socket.connect((server_address, server_port))

# while True:
#     message = input("Enter a message to send to the server (or 'exit' to quit): ")
#     if message == 'exit':
#         break

#     # Send the message to the server
#     client_socket.send(message.encode('utf-8'))

#     # Receive the response from the server
#     response = client_socket.recv(1024)
#     print(f"Server response: {response.decode('utf-8')}")

# # Close the client socket
# client_socket.close()