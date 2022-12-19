import pygame
import math
import random

from config import screenWidth, screenHeight

# Obstacles
obstacles = []

# Border
obstacles.append(pygame.Rect(0, 0, screenWidth, 25))
obstacles.append(pygame.Rect(0, screenHeight - 25, screenWidth, 25))
obstacles.append(pygame.Rect(0, 0, 25, screenHeight))
obstacles.append(pygame.Rect(screenWidth - 25, 0, 25, screenHeight))

# Random
totalObstacles = 40
for _ in range(totalObstacles):
    obstacles.append(pygame.Rect(random.randint(0, screenWidth), random.randint(100, screenHeight), random.randint(25, 75), random.randint(25, 75)))

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.players = {}
        self.projectiles = []
        self.obstacles = obstacles

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
        self.players[username] = Player(30, 30, username)
        return self.players, self.projectiles, self.obstacles
    
    def killPlayer(self, username):
        if username in self.players:
            del self.players[username]

    def gameloop(self):
        while True:
            delta = self.clock.tick(60) / 1000

            for projectile in self.projectiles:
                projectile.update(delta)

                for player in self.players.values():
                    if player.rect.colliderect(projectile.rect):
                        player.health -= 10
                        self.projectiles.remove(projectile)
                        break
                    
                for obstacle in self.obstacles:
                    if obstacle.colliderect(projectile.rect):
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)
                        break
                        
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
    turretRotateSpeed = 75

    width = 64
    height = 64

    def __init__(self, x, y, username):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.username = username

    def update(self, delta, obstacles):
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
        
        xDirection = self.vel * self.speed * delta * \
            math.sin(math.radians(self.angle))
        
        yDirection = self.vel * self.speed * delta * \
            math.cos(math.radians(self.angle))
        
        # Collisions
        for obstacle in obstacles:
            if obstacle.colliderect(self.x + xDirection, self.y, self.width, self.height):
                if xDirection > 0:
                    xDirection = obstacle.left - self.rect.right
                else:
                    xDirection = self.rect.left - obstacle.right
                    
            if obstacle.colliderect(self.x, self.y + yDirection, self.width, self.height):
                if yDirection > 0:
                    yDirection = obstacle.top - self.rect.bottom
                else:
                    yDirection = self.rect.top - obstacle.bottom
        
        self.x += xDirection
        self.y += yDirection
        
        # Updating rect
        self.rect.x, self.rect.y = self.x, self.y
