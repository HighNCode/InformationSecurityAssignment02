import socket
import json
import cryptography
from cryptography.fernet import Fernet
import hashlib
from flask import render_template
import random
from sympy import isprime, primitive_root

    
def AES(message):
    # Generating an AES key
    key = Fernet.generate_key()
    # Creating a Cipher Object
    cipher = Fernet(key)

    #AES ENCRYPTION
    # Encrypting the received message
    encryptedmsg = cipher.encrypt(message)

    return key,encryptedmsg

def DiffieHellman(client_socket):
    #Generating a random prime number using isprime inbuilt function
    #q is the Prime Number
    #While loop to check if the random number generated is Prime or not, if not continue traversing the loop and if it is then break the loop.
    while (True):
        q = random.randint(1,200)
        if (isprime(q)):
            break

    #Finding the primitive root of the prime number generated above using primitive_root inbuilt function
    #alpha is the Primitive Root of q
    alpha = primitive_root(q)
    
    #Generating private keys for client, which is less than the prime no q and also different (as private keys for both can never be the same).
    privatekeyA = random.randint(0, q-1)

    #Generating public keys for client, using the private keys generated above.
    publickeyA = (pow(alpha,privatekeyA) % q) #(alpha^privatekeyA)modq
    data = {
    'prime_number': q,
    'primitive_root': alpha,
    'publickeyA' : publickeyA,
     }

# Serialize the data to a JSON string
    json_data = json.dumps(data)
    client_socket.send(json_data.encode('utf-8'))
    publickeyB = client_socket.recv(1024)
    sharedsecretA = (pow(publickeyB,privatekeyA) % q)
    
def SHA256(encryptedmessage):
    sha256 = hashlib.sha256()

# Update the hash object with the string bytes
    sha256.update(encryptedmessage.encode())

# Get the hexadecimal representation of the hash
    hashed_message = sha256.hexdigest()

def clientFun(message):
    # Define the server address and port
    server_address = '127.0.0.1'
    server_port = 12345

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((server_address, server_port))

        #encrypting the message received from the Flask App using AES
        key,encryptedmsg = AES(message.encode('utf-8'))
        client_socket.send(encryptedmsg.encode('utf-8'))
        
        #generating hash using SHA256 
        hashvalue = SHA256(message.encode('utf-8'))
        client_socket.send(hashvalue.encode('utf-8'))       
        
        DiffieHellman(client_socket)
        
        # Receive the response from the server
        response = client_socket.recv(1024)
    
    except ConnectionRefusedError:
        response = b"Server is not available."

    finally:
        # Close the client socket
        client_socket.close()

    return render_template('index.html', message=message, response=response.decode('utf-8'))


