import socket
import threading

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())

ADDRESS = ('', PORT)
FORMAT = 'utf-8'


clients, names = [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDRESS)

threads = {}


def StartChat():
    print(f'server is working on: {SERVER}')

    server.listen()

    while True:
        try:
            conn, addr = server.accept()
            conn.send('NAME'.encode(FORMAT))

            name = conn.recv(1024).decode(FORMAT)

            names.append(name)

            broadcastMessage(f'{name} has joined the chat!\n'.encode(FORMAT))

            conn.send('Connected Successfully!'.encode(FORMAT))

            thread = threading.Thread(target=handle, args=(conn, addr))

            thread.daemon = True

            thread.start()
            clients.append(conn)
            print(f'active connections: {threading.active_count()-1}')
        except:
            continue


def handle(conn, addr):
    print(f'new connection {addr}')
    connected = True
    while connected:
        message = conn.recv(1024)
        if message:
            broadcastMessage(message)
        else:
            remove_connection(conn)
            connected = False
            print(f'active connections: {threading.active_count()-1}')


def remove_connection(conn):
    for client in clients:
        clients.remove(client)


def broadcastMessage(message):
    for client in clients:
        try:
            client.send(message)
        except:
            remove_connection(client)
        finally:
            continue


StartChat()
