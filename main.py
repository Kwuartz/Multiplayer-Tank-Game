import pygame
import math
import random
import time

from config import (
    screenWidth, screenHeight, mapWidth, mapHeight,
    projectileExplosionColor, projectileExplosionDuration, projectileExplosionSize,
    totalPlayerExplosions, playerExplosionColors, playerExplosionDuration, playerExplosionRadius, playerExplosionSize
)
from game import Player, Projectile, Explosion, GameEvent, Obstacle
from gui import Button, TextInputBox, Minimap
from network import Network


def main():
    network = Network()
    
    pygame.init()
    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Multiplayer")
    clock = pygame.time.Clock()
    
    font16 = pygame.font.Font("assets/font/font.otf", 16)

    
    usernameBox = TextInputBox(screenWidth / 2 - 150, screenHeight / 2 + 55, 300, 100, font16, (255, 255, 255), (255, 255, 255), 5)
    playButton = Button(screenWidth / 2 - 150, screenHeight / 2 - 55, 300, 100, "Play", font16, (255, 255, 255), (255, 255, 255), 5)
    respawnButton = Button(screenWidth / 2 - 150, screenHeight / 2 - 50, 300, 100, "Respawn", font16, (255, 255, 255), (255, 255, 255), 5)

    tankImage = pygame.image.load("assets/gfx/tank.png").convert_alpha()
    turretImage = pygame.image.load("assets/gfx/turret.png").convert_alpha()
    projectileImage = pygame.image.load("assets/gfx/projectile.png").convert_alpha()
    
    playing = False
    running = True

    while not playing and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif (usernameBox.handleEvent(event) or (event.type == pygame.MOUSEBUTTONDOWN and playButton.rect.collidepoint(pygame.mouse.get_pos()))) and len(usernameBox.text) > 0:
                username = usernameBox.text
                players, projectiles, obstacles = network.connect(username)
                localPlayer = players[username]
                explosions = []

                playing = True
        
        clock.tick(60)
        screen.fill((0, 0, 0))
        usernameBox.draw(screen)
        playButton.draw(screen)
        pygame.display.update()

    minimap = Minimap(20, 20, 200, 200, username)

    cameraOffset = pygame.Vector2(0, 0)

    while running:
        if playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    network.send(Projectile(localPlayer.rect.centerx, localPlayer.rect.centery, math.radians(localPlayer.turretAngle)), False)
            
            # Logic
            delta = clock.tick(60) / 1000
            
            # For scrolling
            trueCameraOffset = pygame.Vector2(max(min(localPlayer.x - screenWidth / 2, mapWidth - screenWidth), 0), max(min(localPlayer.y - screenHeight / 2, mapHeight - screenHeight), 0))
            cameraOffset[0] += (trueCameraOffset[0] - cameraOffset[0]) / 30
            cameraOffset[1] += (trueCameraOffset[1] - cameraOffset[1]) / 30

            for projectile in projectiles:
                projectile.update(delta)
                
            for explosion in explosions:
                explosion.update(delta)
                
                if explosion.duration < 0:
                    explosions.remove(explosion)
            
            
            # Getting changes from server
            localPlayer.update(delta, obstacles, cameraOffset)
            players, gameEvents = network.send(localPlayer)

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

            # Graphics
            screen.fill((200, 200, 200))

            for player in players.values():
                if not player.dead:
                    # Rotating turret and tank
                    rotatedTank = pygame.transform.rotate(tankImage, player.angle)
                    rotatedTurret = pygame.transform.rotate(turretImage, player.turretAngle * -1 - 90)
                    
                    screen.blit(rotatedTank, rotatedTank.get_rect(center=player.rect.center - cameraOffset))
                    screen.blit(rotatedTurret, rotatedTurret.get_rect(center=player.rect.center - cameraOffset))

                    # Health bar
                    pygame.draw.rect(screen, (255, 0, 0), (player.rect.x - cameraOffset[0], player.rect.y - cameraOffset[1] - player.height * 0.25, player.width, 10))
                    pygame.draw.rect(screen, (0, 255, 0), (player.rect.x - cameraOffset[0], player.rect.y - cameraOffset[1] - player.height * 0.25, player.width * player.health / 100, 10))
            
            for projectile in projectiles:
                screen.blit(projectileImage, (projectile.rect.topleft - cameraOffset, (projectile.width, projectile.height)))
                
            for obstacle in obstacles:
                pygame.draw.rect(screen, obstacle.color, (obstacle.rect.topleft - cameraOffset, (obstacle.rect.width, obstacle.rect.height)))
            
            for explosion in explosions:
                pygame.draw.circle(screen, explosion.color, (explosion.x, explosion.y) - cameraOffset, explosion.radius)

            minimap.draw(screen, players, obstacles)
            
            pygame.display.update()
        
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and respawnButton.rect.collidepoint(pygame.mouse.get_pos()):
                    players, projectiles, obstacles = network.send(GameEvent("player-respawn", username), True, (500000))
                    localPlayer = players[username]
                    explosions = []
                    playing = True
                    continue
            
            clock.tick(60)

            # Stop socket from closing
            network.send("keep-alive", False)

            screen.fill((0, 0, 0))
            respawnButton.draw(screen)
            pygame.display.update()

main()