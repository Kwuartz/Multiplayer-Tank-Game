import pygame
from config import mapWidth, mapHeight

class Button:
    hovered = False

    def __init__(self, x, y, width, height, text, font, textColor, bgColor, rectThickness = 0):
        self.text = font.render(text, True, textColor)
        self.rect = pygame.Rect(x, y, width, height)
        self.rectThickness = rectThickness
        self.bgColor = bgColor
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.bgColor, self.rect, self.rectThickness)
        screen.blit(self.text, self.text.get_rect(center=self.rect.center))

class TextInputBox:
    text = ""

    def __init__(self, x, y, width, height, font, textColor, bgColor, rectThickness = 0):
        self.font = font
        self.textColor = textColor
        self.textRendered = self.font.render(self.text, True, self.textColor)
        self.rect = pygame.Rect(x, y, width, height)
        self.rectThickness = rectThickness
        self.bgColor = bgColor

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgColor, self.rect, self.rectThickness)
        screen.blit(self.textRendered, self.textRendered.get_rect(center=self.rect.center))

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            elif event.unicode.isalnum() or event.key== pygame.K_SPACE:
                self.text += event.unicode

            self.textRendered = self.font.render(self.text, True, self.textColor)

class Minimap:
    bgColor = (200, 200, 200)
    playerColor = (255, 0, 0)
    localPlayerColor = (255, 255, 0)
    dotSize = 3

    def __init__(self, x, y, width, height, localPlayerName):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = pygame.Surface((width, height))

        self.xScale = mapWidth / width
        self.yScale = mapHeight / height

        self.localPlayerName = localPlayerName

    def draw(self, screen, players, obstacles):
        self.surface.fill(self.bgColor)

        for player in players.values():
            if not player.dead:
                if player.username == self.localPlayerName:
                    pygame.draw.circle(self.surface, self.localPlayerColor, (player.x / self.xScale, player.y / self.yScale), self.dotSize)
                else:
                    pygame.draw.circle(self.surface, self.playerColor, (player.x / self.xScale, player.y / self.yScale), self.dotSize)

        for obstacle in obstacles:
            pygame.draw.rect(self.surface, obstacle.color, (obstacle.rect.x / self.xScale, obstacle.rect.y / self.yScale, obstacle.rect.width / self.xScale, obstacle.rect.height / self.yScale))
        
        screen.blit(self.surface, self.rect)



