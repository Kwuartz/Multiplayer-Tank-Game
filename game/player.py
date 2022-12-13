import pygame
from game.config import screenWidth, screenHeight

class Player():
    speed = 100
    
    def __init__(self, x, y, width, height, color, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x,y,width,height)
        self.vel = 3
        
        self.name = name

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

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)