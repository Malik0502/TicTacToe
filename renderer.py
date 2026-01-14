import pygame
from layout import Layout
from field import Field
import constants

class Renderer:
    def __init__(self, layout: Layout):
        self.layout = layout
        self.winningTextFont = pygame.font.SysFont(name="",size=90, bold=True)
        self.restartTextFont = pygame.font.SysFont(name="", size=30)
        self.winningText = ""


    def render_playing_field(self):
        for i in range(2):
            border = pygame.Rect(0, 
                                 (self.layout.fieldHeight) * (i + 1) - constants.BORDERTHICKNESS, 
                                 self.layout.screenWidth, constants.BORDERTHICKNESS)
            pygame.draw.rect(self.layout.screen, "white", border)
        
            border = pygame.Rect(self.layout.fieldHeight * (i + 1) - constants.BORDERTHICKNESS, 0,
                                 constants.BORDERTHICKNESS, self.layout.screenHeight)
            pygame.draw.rect(self.layout.screen, "white", border)

    def render_circle(self, field: Field):
        pygame.draw.circle(self.layout.screen, "blue", 
                         (int(field.xCenterPoint), int(field.yCenterPoint)), 
                         int(self.layout.fieldWidth / 4), 5)
        pygame.display.flip()

    def render_cross(self, field: Field):
        pygame.draw.line(self.layout.screen, "red", 
                         (int(field.xCenterPoint - self.layout.xFieldCenter / 2), 
                         int(field.yCenterPoint - self.layout.yFieldCenter / 2)),
                         (int(field.xCenterPoint + self.layout.xFieldCenter / 2), 
                         int(field.yCenterPoint + self.layout.yFieldCenter / 2)), 5)
        pygame.draw.line(self.layout.screen, "red", 
                         (int(field.xCenterPoint + self.layout.xFieldCenter / 2), 
                         int(field.yCenterPoint - self.layout.yFieldCenter / 2)), 
                         (int(field.xCenterPoint - self.layout.xFieldCenter / 2), 
                         int(field.yCenterPoint + self.layout.yFieldCenter / 2)), 5)
        pygame.display.flip()

    def render_win_title(self):
        restartText = "Press Space to restart the Game"
        winTitleSurface = self.winningTextFont.render(self.winningText, False, (0, 0, 0))
        restartTitleSurface = self.restartTextFont.render(restartText, False, (0, 0, 0))
        winTitleRect = winTitleSurface.get_rect(center=(self.layout.screenWidth / 2, self.layout.screenHeight / 2))
        restartTitleRect = restartTitleSurface.get_rect(center=(self.layout.screenWidth / 2, self.layout.screenHeight / 2 + self.restartTextFont.size(restartText)[1] * 3))
        self.layout.screen.blit(winTitleSurface, winTitleRect)
        self.layout.screen.blit(restartTitleSurface, restartTitleRect)