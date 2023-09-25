import socket
import threading

HOST = "localhost"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message, sender):
    for client in clients:
        # if client != sender:
            try:
                client.send(message)
            except:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                nicknames.remove(nickname)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            print(f"{nicknames[clients.index(client)]} says: {message.decode('utf-8')}")
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {str(addr)}")

        client.send("<NICK>".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        if nickname in nicknames:
            client.send("Nickname already in use.".encode("utf-8"))
            client.close()
            continue

        nicknames.append(nickname)
        clients.append(client)

        print(f"Client nickname: {nickname}")
        broadcast(f"{nickname} connected to the server.\n".encode("utf-8"), client)
        client.send("Connected to the server.".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running.")
receive()
