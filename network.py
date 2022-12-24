from pickle import loads, dumps
import socket
import sys


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ("localhost", 5555) # 35.246.37.250 3389 this google one

    def connect(self, username):
        try:
            self.client.connect(self.address)
            self.client.send(dumps(username))
            return loads(self.client.recv(500000))
        except:
            raise

    def send(self, payload, recieving=True, size=1024):
        self.client.send(dumps(payload))

        if recieving:
            return loads(self.client.recv(size))
