import pygame
import math
from config import screenWidth, screenHeight
from game import Player, Projectile, GameEvent
from network import Network

def main():
    username = input("Enter username: ")
    network = Network(username)
    
    players, projectiles, obstacles = network.getState()
    localPlayer = players[username]
    
    pygame.init()

    screen = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Multiplayer")
    
    font16 = pygame.font.Font("assets/font/font.otf", 16)

    tankImage = pygame.image.load("assets/gfx/tank.png").convert_alpha()
    turretImage = pygame.image.load("assets/gfx/turret.png").convert_alpha()
    projectileImage = pygame.image.load("assets/gfx/projectile.png").convert_alpha()
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
            # Firing bullets
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                network.send(Projectile(localPlayer.rect.centerx, localPlayer.rect.centery, math.radians(localPlayer.turretAngle)), False)

        # Logic
        delta = clock.tick(60) / 1000
        
        for projectile in projectiles:
            projectile.update(delta)
        
        localPlayer.update(delta, obstacles)
        
        # Getting changes from server
        players, gameEvents = network.send(localPlayer)
        localPlayer = players[username]
        
        # Event handling
        for event in gameEvents:
            if event.name == "new-projectile":
                projectiles.append(event.data)
            elif event.name == "projectile-destroyed":
                del projectiles[event.data]

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
        
        pygame.display.update()

def writeText(text, font, x, y):
  renderedText = font.render(text, True, (0, 0, 0))
  screen.blit(renderedText, (x, y))

main()