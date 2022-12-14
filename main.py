import pygame
import math
from game.config import screenWidth, screenHeight
from game.player import Player
from game.bullet import Bullet
from game.network import Network

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Multiplayer")

font32 = pygame.font.Font("assets/font/font.otf", 32)

def main():
    net = Network()
    
    gamestate = net.initialState
    
    name = input("Enter username: ")
    localPlayer = Player(100, 100, name)
    
    clock = pygame.time.Clock()

    while True:
        newBullets = []
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                distance = pygame.mouse.get_pos() - pygame.Vector2(localPlayer.rect.center)
                angle = math.atan2(distance.y, distance.x)
                newBullets.append(Bullet(localPlayer.x, localPlayer.y, angle))

        # Logic
        delta = clock.tick(60) / 1000
        
        # Local player logic
        localPlayer.move(delta)
        
        payload = {}
        payload["player"] = localPlayer
        payload["bullets"] = newBullets
        
        gamestate = net.send(payload)
        players = gamestate["players"]
        bullets = gamestate["bullets"]

        screen.fill((255,255,255))
        
        for player in players.values():
            pygame.draw.rect(screen, player.color, player.rect)
            writeText(player.name, font32, player.x, player.y)
        
        for bullet in bullets:
            pygame.draw.rect(screen, (75, 100, 175), bullet.rect)
        
        pygame.display.update()

def writeText(text, font, x, y):
  renderedText = font.render(text, True, (0, 0, 0))
  screen.blit(renderedText, (x, y))

main()