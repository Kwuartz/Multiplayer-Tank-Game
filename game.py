import pygame
import math
import noise
import random

from config import mapWidth, mapHeight

def generateMap(width, height, threshold = 0.575, scale = 10):
    obstacles = []

    # Border
    obstacles.append(Obstacle(-25, -25, mapWidth, 50, (0, 0, 0)))
    obstacles.append(Obstacle(-25, mapHeight - 25, mapWidth + 25, 50, (0, 0, 0)))
    obstacles.append(Obstacle(-25, -25, 50, mapHeight + 25, (0, 0, 0)))
    obstacles.append(Obstacle(mapWidth - 25, -25, 50, mapHeight + 25, (0, 0, 0)))

    blockWidth = mapWidth / width
    blockHeight = mapHeight / height

    seed = random.randint(1, 100)
        
    for x in range(width):
        for y in range(height):
            value = (noise.pnoise2(x / scale, y / scale, base=seed) + 1) / 2

            if value > threshold:
                color = (round(value * 20), round(value * 190), round(value * 145))
                obstacles.append(Obstacle(x * blockWidth, y * blockHeight, blockWidth, blockHeight, color))

    return obstacles

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.players = {}
        self.gameEvents = {}
        self.projectiles = []
        self.obstacles = generateMap(100, 100)

    def updatePlayer(self, data):
        player = self.players[data.username]
        
        player.angle, player.turretAngle = data.angle, data.turretAngle
        player.x, player.y, player.rect = data.x, data.y, data.rect
        
        try:
            return self.players, self.gameEvents[player.username]
        finally:
            self.gameEvents[player.username] = []

    def updateProjectiles(self, projectile):
        self.projectiles.append(projectile)
        self.addEvent("new-projectile", projectile)

    def joinPlayer(self, username):
        found = False
        while not found:
            x = random.randint(25, mapWidth - 25)
            y = random.randint(25, mapHeight - 25)
            player = Player(x, y, username)
            
            # Getting player spawn
            if player.rect.collidelist(self.obstacles) == -1:
                found = True
                
        self.players[username] = player
        self.gameEvents[username] = []
        return self.players, self.projectiles, self.obstacles
    
    def addEvent(self, name, data, player = False):
        event = GameEvent(name, data)
        
        if player:
            self.gameEvents[player].append(event)
        else:
            for eventList in self.gameEvents.values():
                eventList.append(event)
    
    def killPlayer(self, username):
        if username in self.players:
            player = self.players[username]
            player.dead = True
            self.addEvent("player-death", player)
            self.addEvent("death", None, username)

    def gameloop(self):
        while True:
            delta = self.clock.tick(60) / 1000

            for index, projectile in enumerate(self.projectiles):
                projectile.update(delta)

                for player in self.players.values():
                    if not player.dead and player.rect.colliderect(projectile.rect) and projectile.origin != player.username:
                        self.projectiles.remove(projectile)
                        self.addEvent("projectile-destroyed", index)
                        
                        player.health -= 10
                        if player.health <= 0:
                            self.killPlayer(player.username)
                        
                        break
                    
                for obstacle in self.obstacles:
                    if obstacle.rect.colliderect(projectile.rect):
                        if projectile in self.projectiles:
                            self.projectiles.remove(projectile)
                            self.addEvent("projectile-destroyed", index)
                            break
                        
            for player in self.players.values():
                pass

class GameEvent:
    def __init__(self, name, data):
        self.name = name
        self.data = data

class Obstacle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

class Projectile:
    speed = 300
    width = 5
    height = 5
    color = (100, 100, 100)

    def __init__(self, x, y, angle, origin):
        self.angle = angle
        # Making the bullet start at the end of the turret
        self.x = x + math.cos(self.angle) * 32
        self.y = y + math.sin(self.angle) * 32
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.origin = origin

    def update(self, delta):
        self.x += math.cos(self.angle) * self.speed * delta
        self.y += math.sin(self.angle) * self.speed * delta

        self.rect.x, self.rect.y = self.x, self.y
        
class Player:
    speed = 100
    health = 100
    dead = False
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

    def update(self, delta, obstacles, cameraOffset):
        # Rotating turret
        mouseDistance = pygame.mouse.get_pos() - pygame.Vector2(self.rect.center) + cameraOffset # When scrolling the mouse position is different
        mouseAngle = math.degrees(math.atan2(mouseDistance.y, mouseDistance.x))
        
        self.turretAngle = mouseAngle
        
        # Rotating tank
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += delta * self.rotateSpeed
            # self.turretAngle -= delta * self.rotateSpeed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= delta * self.rotateSpeed
            # self.turretAngle += delta * self.rotateSpeed
        
        # Uncomment these if you want turret to slowly follow the mouse
        # rotateDirection = -1 if self.turretAngle > mouseAngle else 1
        # self.turretAngle += delta * self.turretRotateSpeed * rotateDirection
        
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
            if obstacle.rect.colliderect(self.x + xDirection, self.y, self.width, self.height):
                if xDirection > 0:
                    xDirection = obstacle.rect.left - self.rect.right
                else:
                    xDirection = self.rect.left - obstacle.rect.right
                    
            if obstacle.rect.colliderect(self.x, self.y + yDirection, self.width, self.height):
                if yDirection > 0:
                    yDirection = obstacle.rect.top - self.rect.bottom
                else:
                    yDirection = self.rect.top - obstacle.rect.bottom
        
        self.x += xDirection
        self.y += yDirection
        
        # Updating rect
        self.rect.x, self.rect.y = self.x, self.y

class Explosion:
    def __init__(self, x, y, size, color, duration):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.duration = duration
        self.radius = 0
        self.time_elapsed = 0

    def update(self, dt):
        self.time_elapsed += dt
        if self.time_elapsed > self.duration:
            self.time_elapsed = 0
            self.duration = -1
            
        self.radius = int(self.size * self.time_elapsed / self.duration)