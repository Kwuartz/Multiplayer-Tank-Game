import socket
import pickle
from _thread import *
import sys

server = "localhost"
port = 5555
maxConnections = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(maxConnections)
print(f"Waiting for a connection, server started on port {port} with max connections {maxConnections}")

players = {}

def threaded_client(conn):
    conn.send(pickle.dumps(players))
    reply = ""
    
    while True:
        try:
            data = pickle.loads(conn.recv(512))
            
            if not data:
                print("Disconnected")
                break
            else:
                players[data.name] = data
                reply = players  

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print(f"Lost connection!")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))