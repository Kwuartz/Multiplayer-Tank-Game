import pygame

class Game:
  def __init__(self):
    self.players = {}
    self.bullets = []
    self.newBullets = []
    self.clock = pygame.time.Clock()
  
  def updateState(self, values):
    player = values.get("player")
    bullets = values.get("bullets")
    
    self.players[player.name] = player
    
    for bullet in bullets:
      self.bullets.append(bullet)
  
  def gameloop(self):
    while True:
      for bullet in self.bullets:
        bullet.update()
        for player in self.players.values():
          if pygame.Rect.colliderect(player.rect, bullet.rect):
            print("HIT")
      
      self.clock.tick(60)
  
  def getState(self):
    state = {}
    state["players"] = self.players
    state["bullets"] = self.bullets
    
    return state