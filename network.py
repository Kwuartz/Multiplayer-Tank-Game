import socket
import pickle
import sys

class Network:
  def __init__(self, username):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = "localhost"
    self.port = 5555
    self.initialState = self.connect(username)

  def connect(self, username):
    try:
      self.client.connect((self.server, self.port))
      self.client.send(str.encode(username))
      return pickle.loads(self.client.recv(2048))
    except:
      raise

  def send(self, data):
    self.client.send(pickle.dumps(data))
    return pickle.loads(self.client.recv(2048))
    