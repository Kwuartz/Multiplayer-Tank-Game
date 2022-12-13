import pygame
from game.config import screenWidth, screenHeight
from game.player import Player
from game.network import Network

pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Multiplayer")

font32 = pygame.font.Font("assets/font/font.otf", 32)

def main():
    net = Network()
    
    players = net.initialState
    name = input("Enter username: ")
    
    localPlayer = Player(100, 100, 100, 100, (0, 255, 0), name)
    
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Logic
        delta = clock.tick(60) / 1000
        
        # Local player logic
        localPlayer.move(delta)
        players = net.send(localPlayer)
        
        for player in players.values():
            player.update()

        screen.fill((255,255,255))
        
        for player in players.values():
            pygame.draw.rect(screen, player.color, player.rect)
            writeText(player.name, font32, player.x, player.y)
        
        pygame.display.update()

def writeText(text, font, x, y):
  renderedText = font.render(text, True, (0, 0, 0))
  screen.blit(renderedText, (x, y))

main()