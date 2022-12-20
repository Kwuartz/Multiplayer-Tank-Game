import pygame
import math
import random
import time

from config import (
    screenWidth, screenHeight,
    projectileExplosionColor, projectileExplosionDuration, projectileExplosionSize,
    totalPlayerExplosions, playerExplosionColors, playerExplosionDuration, playerExplosionRadius, playerExplosionSize
)
from game import Player, Projectile, Explosion, GameEvent
from network import Network


def main():
    network = Network()
    
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Multiplayer")
    clock = pygame.time.Clock()
    
    font16 = pygame.font.Font("assets/font/font.otf", 16)

    tankImage = pygame.image.load("assets/gfx/tank.png").convert_alpha()
    turretImage = pygame.image.load("assets/gfx/turret.png").convert_alpha()
    projectileImage = pygame.image.load("assets/gfx/projectile.png").convert_alpha()
    
    username = input("Enter username: ")
    players, projectiles, obstacles = network.connect(username)
    localPlayer = players[username]
    explosions = []
    
    playing = True
    
    while True:
        if playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    network.send(Projectile(localPlayer.rect.centerx, localPlayer.rect.centery, math.radians(localPlayer.turretAngle)), False)
            
            # Logic
            delta = clock.tick(60) / 1000
            
            for projectile in projectiles:
                projectile.update(delta)
                
            for explosion in explosions:
                explosion.update(delta)
                
                if explosion.duration < 0:
                    explosions.remove(explosion)
            
            localPlayer.update(delta, obstacles)
            
            # Getting changes from server
            players, gameEvents = network.send(localPlayer)
            localPlayer = players[username]
            
            # Event handling
            for event in gameEvents:
                if event.name == "new-projectile":
                    projectiles.append(event.data)
                elif event.name == "projectile-destroyed":
                    projectile = projectiles[event.data]
                    explosions.append(Explosion(projectile.x, projectile.y, projectileExplosionSize, projectileExplosionColor, projectileExplosionDuration))
                    projectiles.remove(projectile)
                elif event.name == "player-death":
                    player = event.data
                    
                    for _ in range(totalPlayerExplosions):
                        xOffset = random.randint(playerExplosionRadius[0], playerExplosionRadius[1])
                        yOffset = random.randint(playerExplosionRadius[0], playerExplosionRadius[1])
                        explosionSize = random.randint(playerExplosionSize[0], playerExplosionSize[1])
                        explosionDuration = random.randint(playerExplosionDuration[0], playerExplosionDuration[1])
                        explosions.append(Explosion(player.x + xOffset, player.y + yOffset, explosionSize, random.choice(playerExplosionColors), explosionDuration))
                elif event.name == "death":
                    playing = False
            
            screen.fill((255,255,255))
            
            for player in players.values():
                # Rotating turret and tank
                rotatedTank = pygame.transform.rotate(tankImage, player.angle)
                rotatedTurret = pygame.transform.rotate(turretImage, player.turretAngle * -1 - 90)
                
                screen.blit(rotatedTank, rotatedTank.get_rect(center=player.rect.center))
                screen.blit(rotatedTurret, rotatedTurret.get_rect(center=player.rect.center))

                # Health bar
                pygame.draw.rect(screen, (255, 0, 0), (player.rect.x, player.rect.y - player.height * 0.25, player.width, 10))
                pygame.draw.rect(screen, (0, 255, 0), (player.rect.x, player.rect.y - player.height * 0.25, player.width * player.health / 100, 10))
            
            for projectile in projectiles:
                screen.blit(projectileImage, projectile.rect)
                
            for obstacle in obstacles:
                pygame.draw.rect(screen, (0, 0, 0), obstacle)
            
            for explosion in explosions:
                pygame.draw.circle(screen, explosion.color, (explosion.x, explosion.y), explosion.radius)
            
            pygame.display.update()
        
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            network.send("keep-alive", False)
            
            players, projectiles, obstacles = network.send(GameEvent("player-respawn", username))
            localPlayer = players[username]
            explosions = []
            playing = True

def writeText(text, font, x, y):
  renderedText = font.render(text, True, (0, 0, 0))
  screen.blit(renderedText, (x, y))

main()