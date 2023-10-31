import socket
import threading
import os
import time

PORTA = 18000
SERVER = 'localhost'
ADDR = (SERVER, PORTA)
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT = ':D'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []

def handler(conn, addr):
    try:
        print(f'[NOVA CONEXÃO]: {addr} se conectou!')

        conectado = True
        conexoes.append(conn)
        
        while conectado:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT:
                    conectado = False
                    print(f"Desconctando: {addr}")
                    continue

                print(f'[{time.ctime()}][{addr}]: {msg}')
                
                for conexao in conexoes:
                    conexao.send(f'[{time.ctime()}][{addr}]: {msg}'.encode(FORMAT))

    except Exception as e:
        print(f"Erro: {e}")
    finally:
        if conn in conexoes:
            conexoes.remove(conn)
        conn.close()


def start():
    server.listen()
    print(f'O servidor está no endereço {SERVER}')
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handler, args=(conn, addr))
        thread.start()
        print(f'Conexões ativas: {threading.active_count() - 1}')

print('Iniciando o servidor ...')
print('--------------------------')
start()