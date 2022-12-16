import pygame
import math
from config import screenWidth, screenHeight
from game import Player, Projectile
from network import Network

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Multiplayer")

font32 = pygame.font.Font("assets/font/font.otf", 32)

def main():
    username = input("Enter username: ")
    net = Network(username)
    
    players, projectiles = net.initialState
    localPlayer = players[username]
    
    clock = pygame.time.Clock()

    while True:
        newProjectile = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                distance = pygame.mouse.get_pos() - pygame.Vector2(localPlayer.rect.center)
                angle = math.atan2(distance.y, distance.x)
                newProjectile = Projectile(localPlayer.rect.centerx, localPlayer.rect.centery, angle)

        # Talking to server
        delta = clock.tick(60) / 1000
        
        localPlayer.move(delta)
        players, projectiles = net.send(localPlayer)
        
        if newProjectile:
            projectiles = net.send(newProjectile)

        screen.fill((255,255,255))
        
        for player in players.values():
            pygame.draw.rect(screen, player.color, player.rect)
            writeText(player.username, font32, player.x, player.y)
        
        for projectile in projectiles:
            pygame.draw.rect(screen, (75, 100, 175), projectile.rect)
        
        pygame.display.update()

def writeText(text, font, x, y):
  renderedText = font.render(text, True, (0, 0, 0))
  screen.blit(renderedText, (x, y))

main()