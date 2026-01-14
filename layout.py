import pygame

class Layout:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screenWidth = screen.get_width()
        self.screenHeight = screen.get_height()
        self.fieldHeight = self.screenHeight / 3
        self.fieldWidth = self.screenWidth / 3
        self.xFieldCenter = self.fieldWidth / 2
        self.yFieldCenter = self.fieldHeight / 2