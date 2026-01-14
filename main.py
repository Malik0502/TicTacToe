import pygame
import numpy as np
from field import Field

pygame.init()
pygame.font.init()

winningTextFont = pygame.font.SysFont(name="",size=90, bold=True)
restartTextFont = pygame.font.SysFont(name="", size=30)

screen = pygame.display.set_mode((512, 512))
SCREENWIDTH = screen.get_width()
SCREENHEIGHT = screen.get_height()
FIELDHEIGHT = SCREENHEIGHT / 3
FIELDWIDTH = SCREENWIDTH / 3
XFIELDCENTER = FIELDWIDTH / 2
YFIELDCENTER = FIELDHEIGHT / 2
isCircleTurn = False
isGameOver = False
winningText = ""

CROSS = "Cross"
CIRCLE = "Circle"

screen.fill("beige")
BORDERTHICKNESS = 5

clock = pygame.time.Clock()
running = True

def calculate_center_fields():
    centerPoints: list[list[Field]] = []

    for col in range(3):
        y = YFIELDCENTER + ((col) * FIELDHEIGHT)
        rowList: list[Field] = []
        for row in range(3):
            x = XFIELDCENTER + ((row) * FIELDWIDTH)
            field = Field(int(x), int(y), False, False)
            rowList.append(field)
        centerPoints.append(rowList)
        x = XFIELDCENTER
        y = YFIELDCENTER

    return centerPoints

fields = calculate_center_fields()

def render_playing_field():
    for i in range(2):
        border = pygame.Rect(0, (FIELDHEIGHT) * (i + 1) - BORDERTHICKNESS, SCREENWIDTH, BORDERTHICKNESS)
        pygame.draw.rect(screen, "white", border)
        
        border = pygame.Rect(FIELDHEIGHT * (i + 1) - BORDERTHICKNESS, 0, BORDERTHICKNESS, SCREENHEIGHT)
        pygame.draw.rect(screen, "white", border)

def render_circle(field: Field):
    pygame.draw.circle(screen, "blue", (int(field.xCenterPoint), int(field.yCenterPoint)), int(FIELDWIDTH / 4), 5)
    pygame.display.flip()

def render_cross(field: Field):
    pygame.draw.line(screen, "red", (int(field.xCenterPoint - XFIELDCENTER / 2), int(field.yCenterPoint - YFIELDCENTER / 2)),
                        (int(field.xCenterPoint + XFIELDCENTER / 2), int(field.yCenterPoint + YFIELDCENTER / 2)), 5)
    pygame.draw.line(screen, "red", (int(field.xCenterPoint + XFIELDCENTER / 2), int(field.yCenterPoint - YFIELDCENTER / 2)),
                        (int(field.xCenterPoint - XFIELDCENTER / 2), int(field.yCenterPoint + YFIELDCENTER / 2)), 5)
    pygame.display.flip()

def render_win_title():
    restartText = "Press Space to restart the Game"
    winTitleSurface = winningTextFont.render(winningText, False, (0, 0, 0))
    restartTitleSurface = restartTextFont.render(restartText, False, (0, 0, 0))
    winTitleRect = winTitleSurface.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2))
    restartTitleRect = restartTitleSurface.get_rect(center=(SCREENWIDTH / 2, SCREENHEIGHT / 2 + restartTextFont.size(restartText)[1] * 3))
    screen.blit(winTitleSurface, winTitleRect)
    screen.blit(restartTitleSurface, restartTitleRect)


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

    if is_symbol_winning(lines, CROSS):
        winningText = "Cross Wins"
        isGameOver = True
        return True
    if is_symbol_winning(lines, CIRCLE):
        winningText = "Circle Wins"
        isGameOver = True
        return True
    
    return False

def is_symbol_winning(lines, symbol):
    if CIRCLE in symbol:
        if any(all(cell.isCircle for cell in line) for line in lines):
            return True
    if CROSS in symbol:
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

def reset_game():
    global fields, isCircleTurn, isGameOver, winningText
    fields = calculate_center_fields()
    isCircleTurn = False
    isGameOver = False
    winningText = ""
    screen.fill("beige")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not isGameOver:
                click_selected_field()
        if event.type == pygame.KEYDOWN:
            if isGameOver and event.key == pygame.K_SPACE:
                reset_game()

    if isGameOver and winningText:
        render_win_title()

    if not isGameOver:
        render_playing_field()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()