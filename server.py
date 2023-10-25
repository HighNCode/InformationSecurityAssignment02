import ssl
import socket
from cryptography.fernet import Fernet
import hashlib
from cryptography.hazmat.primitives.asymmetric import dh,rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.backends import default_backend

# Server configuration
HOST = 'localhost'
PORT = 1234
CERT_FILE = 'certificate.pem'

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wrap the socket with SSL/TLS
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile=CERT_FILE)
server_socket_ssl = context.wrap_socket(server_socket, server_side=True)

# Bind the SSL socket to a specific address and port
server_socket_ssl.bind((HOST, PORT))

# Listen for incoming connections
server_socket_ssl.listen()

print("Server is listening on {}:{}".format(HOST, PORT))

while True:
    # Accept a client connection
    client_socket_ssl, client_address = server_socket_ssl.accept()
    print("Accepted connection from {}:{}".format(client_address[0], client_address[1]))

    try:
        # Receive data from the client
        data = client_socket_ssl.recv(1024)
        print("Received data from client: {}".format(data.decode()))

        # Process the received data
        # ...

        # Send a response back to the client
        response = "Hello, client!"
        client_socket_ssl.send(response.encode())
        print("Sent response to client: {}".format(response))
    finally:
        # Close the client socket
        client_socket_ssl.close()
        print("Closed client connection")

# Close the SSL server socket (This code won't be reached in this example)
server_socket_ssl.close()
print("Server is shut down")