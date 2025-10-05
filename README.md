# 🗨️ Python Chat Application (Socket + Tkinter)

This project implements a **multi-client chat system** using **Python sockets** and **Tkinter** for the graphical interface.  
It includes both a **server** and a **client** application that communicate through TCP sockets, allowing multiple users to chat in real time.

---

## 📦 Features

### 🖥️ Server
- Accepts multiple client connections using **threads**  
- Displays the list of connected users in a **Tkinter GUI**  
- Handles connections, disconnections, and duplicate nickname prevention  
- Broadcasts messages from any client to all connected clients  
- Start and stop buttons for server control  

### 💬 Client
- GUI-based chat interface built with **Tkinter**  
- Prompts the user for a nickname when connecting  
- Sends and receives messages in real time  
- Supports a `"close"` command to disconnect gracefully  
- Displays messages from all users and the server  

---

## ⚙️ Requirements

- **Python 3.8+**
- Uses only built-in libraries:
  - `socket`
  - `threading`
  - `tkinter`

No external dependencies required ✅

---

## 🧩 File Structure

```
chat_app/
│
├── server.py     # GUI server that manages client connections
├── client.py     # GUI chat client for users
└── README.md     # Documentation (this file)
```

---

## 🚀 How to Run

### 🖥️ 1️⃣ Start the Server

1. Open a terminal and run:
   ```bash
   python server.py
   ```

2. In the GUI:
   - Click **Connect** to start the server  
   - The labels will display the **Host** (`localhost`) and **Port** (`9999`)  
   - Connected clients will appear in the list  
   - Click **Stop** to shut down the server  

---

### 💬 2️⃣ Start a Client

1. In another terminal (or another computer on the same network), run:
   ```bash
   python client.py
   ```

2. When prompted, enter a **nickname** (must be unique).

3. Type a message and click **Send** to broadcast it.

4. To disconnect gracefully, type:
   ```
   <your_nickname>: close
   ```
   or simply close the window.

---

## 🧠 How It Works

### 🖥️ Server Logic
- Creates a TCP socket with:
  ```python
  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  ```
- Binds to the host and port, and listens for incoming clients.  
- Each client is handled in its own thread (`handle()` function).  
- Broadcasts messages to all clients using:
  ```python
  client.send(message)
  ```
- Updates the GUI with the list of active nicknames in real time.

### 💻 Client Logic
- Connects to the server using the same host and port.  
- Server requests nickname with the `<NICK>` tag.  
- GUI thread (`gui_loop`) manages the user interface.  
- Receive thread (`receive`) constantly listens for new messages.  
- The **Send** button triggers `write()` to send input text.

---

## 🧱 System Architecture

Below is a simplified representation of how the system works:

```
          ┌──────────────────────────────┐
          │          Server GUI          │
          │  (Tkinter + Socket Thread)   │
          │  - Manages clients           │
          │  - Broadcasts messages       │
          │  - Updates client list       │
          └──────────────┬───────────────┘
                         │
           ┌─────────────┴─────────────┐
           │                           │
 ┌────────────────────┐       ┌────────────────────┐
 │      Client 1      │       │      Client 2      │
 │ (Tkinter GUI)      │       │ (Tkinter GUI)      │
 │ - Sends messages   │       │ - Sends messages   │
 │ - Receives updates │       │ - Receives updates │
 └────────────────────┘       └────────────────────┘
           │                           │
           └─────────── TCP ───────────┘
```

Each client runs in its own thread on the server.  
Messages from one client are broadcast to all others via the `broadcast()` function.

---

## 💡 Example Session

### 🖥️ Server Console Output
```
Server running.
Server address: localhost
Server listening in port: 9999
Accepted connection from ('127.0.0.1', 56789)
Client nickname: Alice
Accepted connection from ('127.0.0.1', 56810)
Client nickname: Bob
```

### 💬 Client Chat Example
```
Alice: Hello everyone!
Bob: Hi Alice!
```

---

## 🛠️ Customization

You can easily modify:

| Element | Description |
|----------|--------------|
| `HOST` / `PORT` | Change to match your network setup |
| GUI settings | Modify fonts, colors, and sizes in Tkinter |
| Logging | Add timestamps or file logging for message history |
| Protocol | Extend message handling for commands or private messages |

---

## ⚠️ Notes

- The **server must be running** before any clients try to connect.  
- Nicknames **must be unique** — duplicates are rejected.  
- For internet use or production, consider:
  - Encrypted connections (TLS)
  - Authentication
  - WebSocket-based servers (e.g., `FastAPI`, `Flask-SocketIO`)

---

## 📚 License

This project is provided for **educational purposes**.  
Feel free to modify and extend it for your own learning or projects.

---

👨‍💻 **Author:** Caio Castro
