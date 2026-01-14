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
isCircleTurn = False

screen.fill("beige")
borderThickness = 5

clock = pygame.time.Clock()
running = True

def calculate_center_fields():
    centerPoints: list[list[Field]] = []

    for col in range(3):
        y = yFieldCenter + ((col) * fieldHeight)
        rowList: list[Field] = []
        for row in range(3):
            x = xFieldCenter + ((row) * fieldWidth)
            field = Field(int(x), int(y), False, False)
            rowList.append(field)
        centerPoints.append(rowList)
        x = xFieldCenter
        y = yFieldCenter

    return centerPoints

fields = calculate_center_fields()

def render_playing_field():
    for i in range(2):
        border = pygame.Rect(0, (fieldHeight) * (i + 1) - borderThickness, screenWidth, borderThickness)
        pygame.draw.rect(screen, "white", border)
        
        border = pygame.Rect(fieldHeight * (i + 1) - borderThickness, 0, borderThickness, screenHeight)
        pygame.draw.rect(screen, "white", border)

    pygame.display.flip()

def render_circle(field: Field):
    pygame.draw.circle(screen, "blue", (int(field.xCenterPoint), int(field.yCenterPoint)), int(fieldWidth / 4), 5)
    pygame.display.flip()

def render_cross(field: Field):
    pygame.draw.line(screen, "red", (int(field.xCenterPoint - xFieldCenter / 2), int(field.yCenterPoint - yFieldCenter / 2)),
                        (int(field.xCenterPoint + xFieldCenter / 2), int(field.yCenterPoint + yFieldCenter / 2)), 5)
    pygame.draw.line(screen, "red", (int(field.xCenterPoint + xFieldCenter / 2), int(field.yCenterPoint - yFieldCenter / 2)),
                        (int(field.xCenterPoint - xFieldCenter / 2), int(field.yCenterPoint + yFieldCenter / 2)), 5)
    pygame.display.flip()

def calculate_nearest_field():
    mousePos = pygame.mouse.get_pos()
    smallestDistance = float("inf")
    nearestField = Field()

    for list in fields:
        for point in list:
            currentDistance = np.square(point.xCenterPoint - mousePos[0]) + np.square(point.yCenterPoint - mousePos[1])
            if currentDistance < smallestDistance:
                nearestField = point
                smallestDistance = currentDistance

    return nearestField

def check_win_condition():
    # rows
    lines = list(fields)

    # cols
    lines += [[fields[r][c] for r in range(3)] for c in range(3)]

    # diagonals
    lines += [
        [fields[i][i] for i in range(3)],
        [fields[i][2 - i] for i in range(3)],
    ]

    if is_symbol_winning(lines, "Cross"):
        print("Cross Wins")
        return True
    if is_symbol_winning(lines, "Circle"):
        print("Circle Wins")
        return True
    
    return False

def is_symbol_winning(lines, symbol):
    if "Circle" in symbol:
        if any(all(cell.isCircle for cell in line) for line in lines):
            return True
    if "Cross" in symbol:
        if any(all(cell.isCross for cell in line) for line in lines):
            return True

def click_selected_field():
    nearestField = calculate_nearest_field()
    
    if not nearestField.filled:
        global isCircleTurn
        if isCircleTurn:
            render_circle(nearestField)
            nearestField.isCircle = True
        else:
            render_cross(nearestField)
            nearestField.isCross = True

        nearestField.filled = True
        isCircleTurn = not isCircleTurn
    
    check_win_condition()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_selected_field()

    render_playing_field()

    clock.tick(60)

pygame.quit()