import pygame

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