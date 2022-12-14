import socket
import pickle
from _thread import *
import sys

from gameserver import Game

server = "localhost"
port = 5555
maxConnections = 5

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((server, port))

s.listen(maxConnections)
print(f"Waiting for a connection, server started on port {port} with max connections {maxConnections}")

def threaded_client(conn):
    reply = game.getState()
    conn.send(pickle.dumps(reply))
    
    while True:
        try:
            data = pickle.loads(conn.recv(512))
            
            if data:
                game.updateState(data)
                payload = game.getState()
            else:
                print("Disconnected")
                break

            conn.sendall(pickle.dumps(payload))
        except:
            break

    print(f"Lost connection!")
    conn.close()

game = Game()
start_new_thread(game.gameloop, ())

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))