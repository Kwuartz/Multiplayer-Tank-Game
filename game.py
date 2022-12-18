import pygame
from config import screenWidth, screenHeight
import math

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.players = {}
        self.projectiles = []

    def updatePlayer(self, updatedPlayer):
        player = self.players[updatedPlayer.username]
        player.angle, player.turretAngle = updatedPlayer.angle, updatedPlayer.turretAngle
        player.x, player.y = updatedPlayer.x, updatedPlayer.y
        player.rect = updatedPlayer.rect
        return self.players, self.projectiles

    def updateProjectiles(self, projectile):
        self.projectiles.append(projectile)
        return self.projectiles

    def joinPlayer(self, username):
        self.players[username] = Player(100, 100, username)
        return self.players, self.projectiles
    
    def killPlayer(self, username):
        if username in self.players:
            del self.players[username]

    def gameloop(self):
        while True:
            delta = self.clock.tick(60) / 1000

            for projectile in self.projectiles:
                projectile.update(delta)

                if (projectile.rect.x > screenWidth or projectile.rect.x < 0) or (projectile.rect.y < 0 or projectile.rect.y > screenHeight):
                    self.projectiles.remove(projectile)
                    continue

                for player in self.players.values():
                    if pygame.Rect.colliderect(player.rect, projectile.rect):
                        player.health -= 10
                        self.projectiles.remove(projectile)
                        
            for player in self.players.values():
                pass


class Projectile:
    speed = 300
    width = 5
    height = 5
    color = (100, 100, 100)

    def __init__(self, x, y, angle):
        self.angle = angle
        # Making the bullet start at the end of the turret
        self.x = x + math.cos(self.angle) * 50
        self.y = y + math.sin(self.angle) * 50
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, delta):
        self.x += math.cos(self.angle) * self.speed * delta
        self.y += math.sin(self.angle) * self.speed * delta

        self.rect.x, self.rect.y = self.x, self.y


class Player:
    speed = 100
    health = 100
    angle = turretAngle = 0
    
    rotateSpeed = 125
    turretRotateSpeed = 50

    width = 64
    height = 64

    def __init__(self, x, y, username):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.username = username

    def update(self, delta):
        # Rotating turret and tank
        mouseDistance = pygame.mouse.get_pos() - pygame.Vector2(self.rect.center)
        mouseAngle = math.degrees(math.atan2(mouseDistance.y, mouseDistance.x))
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += delta * self.rotateSpeed
            self.turretAngle -= delta * self.rotateSpeed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= delta * self.rotateSpeed
            self.turretAngle += delta * self.rotateSpeed
        
        rotateDirection = -1 if self.turretAngle > mouseAngle else 1
        self.turretAngle += delta * self.turretRotateSpeed * rotateDirection
          

        # Moving player
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = 1
        else:
            self.vel = 0

        # Factoring in rotation
        self.y += self.vel * self.speed * delta * \
            math.cos(math.radians(self.angle))
        self.x += self.vel * self.speed * delta * \
            math.sin(math.radians(self.angle))

        if self.x + self.width > screenWidth:
            self.x = screenWidth - self.width
        elif self.x < 0:
            self.x = 0
        
        if self.y + self.height > screenHeight:
            self.y = screenHeight - self.height
        elif self.y < 0:
            self.y = 0
        
        # Updating rect
        self.rect.x, self.rect.y = self.x, self.y
