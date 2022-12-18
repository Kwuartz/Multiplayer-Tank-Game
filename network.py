import socket
import pickle
import sys

from game import Projectile, Player

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
      return pickle.loads(self.client.recv(4096))
    except:
      raise
  
  def getState(self):
    return self.initialState

  def send(self, payload : Player or Projectile):
    self.client.send(pickle.dumps(payload))
    
    if isinstance(payload, Player):
      return pickle.loads(self.client.recv(4096))
    