import socket
import threading
import json

PORT = 5000
SERVER = socket.gethostbyname(socket.gethostname())

ADDRESS = ('', PORT)
FORMAT = 'utf-8'


clients, names = [], []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDRESS)


def StartChat():
    print(f'server is working on: {SERVER}')
    b = b''

    server.listen()

    while True:
        try:
            conn, addr = server.accept()
            try:
                data = conn.recv(1024)
                message_data = json.loads(data.decode(FORMAT))
                if len(clients) >= 1:
                    join_message = {
                        'welcome_message': f'{message_data["username"]} Joined the chat'}
                    join_send_obj = json.dumps(join_message).encode(FORMAT)
                    broadcastMessage(join_send_obj)
            except:
                continue

            message = {'welcome_message': 'Connected Successfully!'}
            send_obj = json.dumps(message).encode(FORMAT)
            conn.send(send_obj)

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
            print(message)
            client.send(message)
        except:
            print('opss')
            remove_connection(client)
        finally:
            continue


StartChat()
