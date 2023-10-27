import socket
import json
import random

def DiffieHellman(q,alpha,publickeyA):
    
    #Generating private keys for server, which is less than the prime no q and also different (as private keys for both can never be the same).
    privatekeyB = random.randint(0, q-1)

    #Generating public keys for server, using the private keys generated above.
    publickeyB = (pow(alpha,privatekeyB) % q) #(alpha^privatekeyA)modq
    sharedsecretB = (pow(publickeyA,privatekeyB) % q)
    
    return sharedsecretB

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
host = '127.0.0.1'
port = 12345
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(5)

print(f"Server is listening on {host}:{port}")

while True:
    # Accept a connection from a client
    client_socket, client_address = server_socket.accept()
    print(f"Received connection from {client_address}")

    while True:
        
        message =  client_socket.recv(1024)
        hasvalue = client_socket.recv(1024)
        
        # Receive data from the client
        json_data = client_socket.recv(1024).decode('utf-8')
        if not json_data:
            break
        # Parse the JSON data
        received_data = json.loads(json_data)

        # Access the prime number and primitive root
        prime_number = received_data['prime_number']
        primitive_root = received_data['primitive_root']
        publickeyA = received_data['publickeyA']
        
        publickeyB = DiffieHellman(prime_number,primitive_root,publickeyA)
        # Send the received data back to the client
        client_socket.send(publickeyB)
        if json_data == "exit":
            break

    # Close the client socket
    client_socket.close()

    # Close the server socket
    server_socket.close()
    break