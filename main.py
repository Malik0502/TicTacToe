import pygame
import numpy as np
from field import Field
import constants
from layout import Layout
from renderer import Renderer

pygame.init()
pygame.font.init()



screen = pygame.display.set_mode((512, 512))
layout = Layout(screen=screen)
renderer = Renderer(layout=layout)
isCircleTurn = False
isGameOver = False

screen.fill("beige")


clock = pygame.time.Clock()
running = True

def calculate_center_fields():
    centerPoints: list[list[Field]] = []

    for col in range(3):
        y = layout.yFieldCenter + ((col) * layout.fieldHeight)
        rowList: list[Field] = []
        for row in range(3):
            x = layout.xFieldCenter + ((row) * layout.fieldWidth)
            field = Field(int(x), int(y), False, False)
            rowList.append(field)
        centerPoints.append(rowList)
        x = layout.xFieldCenter
        y = layout.yFieldCenter

    return centerPoints

fields = calculate_center_fields()

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
    global isGameOver
    global winningText
    # rows
    lines = list(fields)

    # cols
    lines += [[fields[r][c] for r in range(3)] for c in range(3)]

    # diagonals
    lines += [
        [fields[i][i] for i in range(3)],
        [fields[i][2 - i] for i in range(3)],
    ]

    if is_symbol_winning(lines, constants.CROSS):
        renderer.winningText = "Cross Wins"
        isGameOver = True
        return True
    if is_symbol_winning(lines, constants.CIRCLE):
        renderer.winningText = "Circle Wins"
        isGameOver = True
        return True
    if is_draw():
        renderer.winningText = "Draw"
        isGameOver = True
        return True
    
    return False

def is_symbol_winning(lines, symbol):
    if constants.CIRCLE in symbol:
        if any(all(cell.isCircle for cell in line) for line in lines):
            return True
    if constants.CROSS in symbol:
        if any(all(cell.isCross for cell in line) for line in lines):
            return True
         
    
def is_draw():
    if all(cell.isFilled for row in fields for cell in row):
        return True

def click_selected_field():
    nearestField = calculate_nearest_field()
    
    if not nearestField.isFilled:
        global isCircleTurn
        if isCircleTurn:
            renderer.render_circle(nearestField)
            nearestField.isCircle = True
        else:
            renderer.render_cross(nearestField)
            nearestField.isCross = True

        nearestField.isFilled = True
        isCircleTurn = not isCircleTurn
    
    check_win_condition()

def reset_game():
    global fields, isCircleTurn, isGameOver, winningText
    fields = calculate_center_fields()
    isCircleTurn = False
    isGameOver = False
    winningText = ""
    screen.fill("beige")

def get_events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not isGameOver:
                click_selected_field()
        if event.type == pygame.KEYDOWN:
            if isGameOver and event.key == pygame.K_SPACE:
                reset_game()

while running:
    get_events()

    if isGameOver and renderer.winningText:
        renderer.render_win_title()

    if not isGameOver:
        renderer.render_playing_field()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()