import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = 'localhost'
PORT = 18000
HEADER = 64
FORMAT ='utf-8'

class Client:

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        # msg = tkinter.Tk()
        # msg.withdraw()

        # self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname:", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Chat Client")

        self.chat_label = tkinter.Label(self.win, text="Chat:")
        self.chat_label.pack()

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack()

        self.msg_label = tkinter.Label(self.win, text="Message:")
        self.msg_label.pack()

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack()

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.pack()

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):

        # message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        message = f"{self.input_area.get('1.0', 'end')}"
        if message.rstrip() == f":D":
            message = message.rstrip()
        msg_len = len(message)
        send_len = str(msg_len).encode("utf-8")
        send_len += b' ' * (HEADER - len(send_len))

        self.sock.send(send_len)
        self.sock.send(message.strip().encode("utf-8"))
        print(message)
        # if message.rstrip() == f"{self.nickname}: :D":
        if message == f":D":
            self.stop()
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                # print(message)
                # if message == "<NICK>":
                #     self.sock.send(self.nickname.encode("utf-8"))
                # else:
                if self.gui_done:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', message + '\n')
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except ConnectionRefusedError:
                break
            except Exception as e:
                print(f"Error when handling client: {e}")
                self.running = False
                self.win.destroy()
                self.sock.close()
                break

client = Client(HOST, PORT)
