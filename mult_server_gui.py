import socket
import threading
import tkinter as tk

HOST = "localhost"
PORT = 9999

clients = []
ips = []
nicknames = []

window = tk.Tk()
window.title("Server")

# Start and Stop buttons
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Host and Port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# Client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="---------- Client List ----------").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=15, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


def start_server():
    global server, HOST, PORT
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print("Server running.\n")
    print(f"Server address: {HOST}\nServer listening in port: {PORT}\n")

    # threading._start_new_thread(receive_clients, (server,))

    receive = threading.Thread(target=receive_clients, args=(server,))
    receive.start()

    lblHost["text"] = "Host: " + HOST
    lblPort["text"] = "Port: " + str(PORT)


def stop_server():
    global server, event
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)

    lblHost["text"] = "Host: X.X.X.X"
    lblPort["text"] = "Port: XXXX"
        
    # server.close()
    print("Server stopped.\n")


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
        index = clients.index(client)
        nickname = nicknames[index]
        ip = ips[index]

        try:
            message = client.recv(1024)
            if message.decode('utf-8').rstrip() != f"{nickname}:":
                if message.decode('utf-8').rstrip() == f"{nickname}: close":
                    clients.remove(client)
                    client.close()
                    
                    nicknames.remove(nickname)
                    ips.remove(ip)
                    
                    print(f"{nickname} left the server.\n")
                    print(nicknames)
                    broadcast(f"{nickname} left the server.\n".encode("utf-8"), client)
                    update_client_display(nicknames)

                    break
                print(f"{nicknames[clients.index(client)]} says: {message.decode('utf-8')}")
                broadcast(message, client)
        except:
            
            clients.remove(client)
            client.close()
            
            nicknames.remove(nickname)

            ip = ips[index]
            ips.remove(ip)
            
            print(f"{nickname} left the server.\n")
            broadcast(f"{nickname} left the server.\n".encode("utf-8"), client)

            update_client_display(nicknames)

            break


def receive_clients(server,):
 
    while True:

        client, addr = server.accept()
        ip = addr[0]
        print(f"Accepted connection from {str(addr)}")

        client.send("<NICK>".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")

        if nickname in nicknames:
            client.send("Nickname already in use.".encode("utf-8"))
            client.close()
            continue
        
        ips.append(ip)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Client nickname: {nickname}")
        broadcast(f"{nickname} connected to the server.\n".encode("utf-8"), client)
        client.send("Connected to the server.".encode("utf-8"))

        update_client_display(nicknames)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


def update_client_display(nick_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for nick in nick_list:
        tkDisplay.insert(tk.END, nick+"\n")
    tkDisplay.config(state=tk.DISABLED)
    print(nick_list)

window.mainloop()