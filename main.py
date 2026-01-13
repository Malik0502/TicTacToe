import pygame
import numpy as np
from field import Field

pygame.init()

screen = pygame.display.set_mode((512, 512))
screenWidth = screen.get_width()
screenHeight = screenWidth = screen.get_height()

fieldHeight = screenHeight / 3
fieldWidth = screenWidth / 3
xFieldCenter = fieldWidth / 2
yFieldCenter = fieldHeight / 2

screen.fill("beige")
borderThickness = 5

clock = pygame.time.Clock()
running = True

def calculate_field_center():
    centerPoints: list[Field] = []

    for col in range(3):
        y = yFieldCenter + ((col) * fieldHeight)
        for row in range(3):
            x = xFieldCenter + ((row) * fieldWidth)
            field = Field(int(x), int(y), False, False)
            centerPoints.append(field)
        x = xFieldCenter
        y = yFieldCenter

    return centerPoints

centerPoints = calculate_field_center()

def render_playing_field():
    for i in range(2):
        border = pygame.Rect(0, (fieldHeight) * (i + 1) - borderThickness, screenWidth, borderThickness)
        pygame.draw.rect(screen, "white", border)
        
        border = pygame.Rect(fieldHeight * (i + 1) - borderThickness, 0, borderThickness, screenHeight)
        pygame.draw.rect(screen, "white", border)

    pygame.display.flip()

def render_rect(field: Field):
    rect = pygame.Rect(0, 0, fieldWidth, fieldHeight)
    rect.center = (int(field.xCenterPoint), int(field.yCenterPoint))
    pygame.draw.rect(screen, "red", rect)
    pygame.display.flip()

def click_selected_field():
    mousePos = pygame.mouse.get_pos()
    smallestDistance = float("inf")
    nearestField = Field()


    for point in centerPoints:
        currentDistance = np.square(point.xCenterPoint - mousePos[0]) + np.square(point.yCenterPoint - mousePos[1])
        print(currentDistance)
        if currentDistance < smallestDistance:
            nearestField = point
            smallestDistance = currentDistance
    render_rect(nearestField)
    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_selected_field()

    render_playing_field()

    clock.tick(60)

pygame.quit()