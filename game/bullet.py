import pygame
import math

class Bullet:
  speed = 400
  width = 5
  height = 10
  
  def __init__(self, x, y, angle):
    self.x = x
    self.y = y
    self.angle = angle
    self.rect = pygame.Rect(x, y, self.width, self.height)
    
  def update(self):
    self.x += math.cos(self.angle) * self.speed / 60
    self.y += math.sin(self.angle) * self.speed / 60
    
    self.rect.update(self.x, self.y, self.width, self.height)
    