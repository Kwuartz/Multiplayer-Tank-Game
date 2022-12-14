import socket
import pickle
import sys

class Network:
  def __init__(self):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = "localhost"
    self.port = 5555
    self.initialState = self.connect()

  def connect(self):
    try:
      self.client.connect((self.server, self.port))
      return pickle.loads(self.client.recv(2048))
    except:
      raise

  def send(self, data):
    try:
      self.client.send(pickle.dumps(data))
      return pickle.loads(self.client.recv(2048))
    except socket.error as err:
      raise err