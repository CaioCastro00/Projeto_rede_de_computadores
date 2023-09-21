import socket
import threading

HOST = "localhost"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[client.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
            # accept a client connection
            client, addr = server.accept()
            print(f"Accepted connection from {str(addr)}")

            client.send("<NICK>".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")
           
            nicknames.append(nickname)
            clients.append(client)

            print(f"Client nickname: {nickname}")
            broadcast(f"{nickname} connected to the server.\n".encode("utf-8"))
            client.send("Connected to the server.".encode("utf-8"))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

print(f"Server running.")
receive()