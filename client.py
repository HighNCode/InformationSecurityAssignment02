import socket
from cryptography.fernet import Fernet
import hashlib
from cryptography.hazmat.primitives.asymmetric import dh,rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.backends import default_backend
import ssl

# Server configuration
HOST = 'localhost'
PORT = 1234
CERT_FILE = 'certificate.pem'

# Generating an AES key
key = Fernet.generate_key()

# Creating a Cipher Object
cipher = Fernet(key)

# Defining a message to be encrypted and decrypted
msg = b"This is a demo sentence for AES"

#AES ENCRYPTION
# Encrypting the above defined message
encryptedmsg = cipher.encrypt(msg)

#AES DECRYPTION
# Decrypting the above encrypted message
decryptedmsg = cipher.decrypt(encryptedmsg)

print(decryptedmsg)

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

# Accept a client connection
client_socket_ssl, client_address = server_socket_ssl.accept()

# Receive data from the client
data = client_socket_ssl.recv(1024)

# Process the received data
# ...

# Send a response back to the client
response = "Hello, client!"
client_socket_ssl.send(response.encode())

# Close the client socket
client_socket_ssl.close()

# Close the SSL server socket
server_socket_ssl.close()