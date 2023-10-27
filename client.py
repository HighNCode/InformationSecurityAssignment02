import socket
from cryptography.fernet import Fernet
import hashlib
from cryptography.hazmat.primitives.asymmetric import dh,rsa,padding
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.backends import default_backend
import ssl
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


def AES():
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