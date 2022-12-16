import pygame
from config import screenWidth, screenHeight
import math

class Game:
  def __init__(self):
    self.clock = pygame.time.Clock()
    self.players = {}
    self.projectiles = []
    
  def updatePlayer(self, player):
    self.players[player.username] = player
    return self.players, self.projectiles
  
  def updateProjectiles(self, projectile):
    self.projectiles.append(projectile)
    return self.projectiles
    
  def joinPlayer(self, username):
    self.players[username] = Player(100, 100, username)
    return self.players, self.projectiles
  
  def gameloop(self):
    while True:
      delta = self.clock.tick(60) / 1000
      
      for projectile in self.projectiles:
        projectile.update(delta)
        
        if (projectile.x > screenWidth or projectile.x < 0) or (projectile.y < 0 or projectile.y > screenHeight):
          self.projectiles.remove(projectile)
        
        for player in self.players.values():
          if pygame.Rect.colliderect(player.rect, projectile.rect):
            print("HIT")

class Projectile:
  speed = 400
  width = 5
  height = 10
  
  def __init__(self, x, y, angle):
    self.angle = angle
    self.x = x + math.cos(self.angle) * 100
    self.y = y + math.sin(self.angle) * 100
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
  def update(self, delta):
    self.x += math.cos(self.angle) * self.speed * delta
    self.y += math.sin(self.angle) * self.speed * delta
    
    self.rect.update(self.x, self.y, self.width, self.height)

class Player:
    speed = 100
    width = 100
    height = 100
    color = (255, 255, 0)
    
    def __init__(self, x, y, username):
        self.x = x
        self.y = y
        self.rect =  pygame.Rect(x, y, self.width, self.height)
        self.vel = 3
        self.username = username

    def move(self, delta):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velX = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velX = 1
        else:
            self.velX = 0
            
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velY = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velY = 1
        else:
            self.velY = 0
            
        if not (self.x < 0 and self.velX == -1) and not (self.x > screenWidth and self.velX == 1):
            self.x += self.velX * self.speed * delta

        if not (self.y < 0 and self.velY == -1) and not (self.y > screenWidth and self.velY == 1):
            self.y += self.velY * self.speed * delta

        self.rect.update(self.x, self.y, self.width, self.height)