import socket
from _thread import *
import time

host = '127.0.0.1'
port = 1233
ThreadCount = 0
clients = []  # List to store connected clients

def client_handler(connection):
    #connection.send(str.encode('You are now connected to the replay server... Type BYE to stop'))
    clients.append(connection)  # Add the connected client to the list
    try:
        while True:
            data = connection.recv(2048)
            message = data.decode('utf-8')
            if message == 'BYE':
                break
            broadcast(message, connection)
    finally:
        clients.remove(connection)  # Remove the client from the list when the connection is closed
        connection.close()

def broadcast(message, sender_connection):
    for client in clients:
        if client != sender_connection:
            try:
                client.sendall(str.encode(message))
            except:
                # Handle any potential errors (e.g., if a client disconnects)
                continue

def connect_to_other_server():
    other_server_host = '192.168.1.14'
    other_server_port = 7777  # Adjust to the actual port of the other server

    other_server_socket = socket.socket()
    try:
        other_server_socket.connect((other_server_host, other_server_port))
        while True:
            data = other_server_socket.recv(2048)
            other_server_socket.send("OK".encode("ascii"))
            if not data:
                break
            message = data.decode('utf-8')
            # Broadcast the received message from the other server to all clients
            broadcast(message, None)
            time.sleep(1)
    finally:
        other_server_socket.close()

def accept_connections(ServerSocket):
    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(client_handler, (Client, ))

def start_server(host, port):
    ServerSocket = socket.socket()
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))
    print(f'Server is listing on the port {port}...')
    ServerSocket.listen()

    # Start a thread to connect to the other server and receive data constantly
    start_new_thread(connect_to_other_server, ())

    # Accept connections from clients
    accept_connections(ServerSocket)

start_server(host, port)
