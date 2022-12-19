import socket
import pickle
import sys

from game import Projectile, Player

class Network:
  def __init__(self, username):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.address = ("localhost", 5555) # ("35.246.37.250", 3389) google one
    self.initialState = self.connect(username)

  def connect(self, username):
    try:
      self.client.connect(self.address)
      self.client.send(str.encode(username))
      return pickle.loads(self.client.recv(4096))
    except:
      raise
  
  def getState(self):
    return self.initialState

  def send(self, payload, recieving = True):
    self.client.send(pickle.dumps(payload))
    
    if recieving:
      return pickle.loads(self.client.recv(4096))
    