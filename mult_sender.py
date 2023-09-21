import socket

def run_client():
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP Socket

    server_ip = "localhost"  # replace with the server's public IP address (go to myip.is in server machine)
    server_port = 9999  # replace with the server's port number

    # establish connection with server
    client.connect((server_ip, server_port))

    try:
        while True:
            # get input message from user and send it to the server
            msg = input("Enter message: ")
            client.send(msg.encode("utf-8")[:1024])

            # receive message from the server
            response = client.recv(1024)
            response = response.decode("utf-8")

            # if server sent "closed" in the payload, break out of
            # the loop and close the socket
            if response.lower() == "closed":
                break

            print(f"Received: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # close client socket (connection to the server)
        client.close()
        print("Connection to server closed")

run_client()