import socket
import threading
import tkinter
import tkinter.scrolledtext

HOST = 'localhost'
PORT = 18000
HEADER = 64
FORMAT ='utf-8'

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Chat Client")

        # Host and Port info
        self.topFrame = tkinter.Frame(self.win)
        self.lblHost = tkinter.Label(self.topFrame, text = "Host: " + self.host)
        self.lblHost.pack(side=tkinter.LEFT)
        self.lblPort = tkinter.Label(self.topFrame, text = "Port: " + str(self.port))
        self.lblPort.pack(side=tkinter.LEFT)
        self.topFrame.pack(side=tkinter.TOP, pady=(5, 0))

        # Disconnect button
        self.middleFrame = tkinter.Frame(self.win)
        self.btnStop = tkinter.Button(self.middleFrame, text="Disconnect", command=lambda : self.disconnect())
        self.btnStop.pack(side=tkinter.LEFT)
        self.middleFrame.pack(side=tkinter.TOP, pady=(5, 0))

        # Chat window
        self.chatLabel = tkinter.Label(self.win, text="Chat:")
        self.chatLabel.pack()
        self.textArea = tkinter.scrolledtext.ScrolledText(self.win)
        self.textArea.pack()

        # Input area
        self.msg_label = tkinter.Label(self.win, text="Message:")
        self.msg_label.pack()       
        self.inputArea = tkinter.Text(self.win, height=3)
        self.inputArea.pack()
        self.sendButton = tkinter.Button(self.win, text="Send", command=self.write)
        self.win.bind('<Return>', self.write)
        self.sendButton.pack()

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.disconnect)

        self.win.mainloop()
            
    def disconnect(self):
        message = f":D".rstrip()
        msg_len = len(message)
        send_len = str(msg_len).encode("utf-8")
        send_len += b' ' * (HEADER - len(send_len))
        self.sock.send(send_len)
        self.sock.send(message.strip().encode("utf-8"))
        self.stop()
        pass

    def write(self, event):

        message = f"{self.inputArea.get('1.0', 'end')}"
        if message.rstrip() != f"":
            if message.rstrip() == f":D":
                message = message.rstrip()
            msg_len = len(message)
            send_len = str(msg_len).encode("utf-8")
            send_len += b' ' * (HEADER - len(send_len))

            self.sock.send(send_len)
            self.sock.send(message.strip().encode("utf-8"))

        if message == f":D":
            self.stop()
        self.inputArea.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode("utf-8")
                if self.gui_done:
                    self.textArea.config(state='normal')
                    self.textArea.insert('end', message + '\n')
                    self.textArea.yview('end')
                    self.textArea.config(state='disabled')
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
