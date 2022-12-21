import pygame

class Button():
    hovered = False

    def __init__(self, x, y, width, height, text, font, textColor, buttonColor, rectThickness = 0):
        self.text = font.render(text, True, textColor)
        self.rect = pygame.Rect(x, y, width, height)
        self.rectThickness = rectThickness
        self.buttonColor = buttonColor
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.buttonColor, self.rect, self.rectThickness)
        screen.blit(self.text, self.text.get_rect(center=self.rect.center))