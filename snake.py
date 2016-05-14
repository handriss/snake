#!/usr/bin/env python

import curses
import time
import random


def zeroStage(snakeX=[], snakeY=[], direction=""):
    """ Starting stage of the snake """
    snakeX = [20, 19, 18, 17]
    snakeY = [20, 20, 20, 20]
    direction = "right"
    return (snakeX, snakeY, direction)


def amIDeadYet(snakeX, snakeY, maxCols, maxRows):
    """ Checks if the death conditions are true """
    for i in range(len(snakeX) - 1):
        if snakeX[0] == snakeX[i + 1] and snakeY[0] == snakeY[i + 1]:
            return True

    return False


def moveTheSnake(snakeX, snakeY, direction):
    """ Calculates and returns the next X and Y position for each snake part"""
    global foodY
    global foodX

    tempX = snakeX[0]
    tempY = snakeY[0]
    snakeX = shiftRight(snakeX)
    snakeY = shiftRight(snakeY)

    if direction == "down":
        snakeY[0] = tempY + 1
        snakeX[0] = tempX
    elif direction == "up":
        snakeY[0] = tempY - 1
        snakeX[0] = tempX
    elif direction == "right":
        snakeX[0] = tempX + 1
        snakeY[0] = tempY
    elif direction == "left":
        snakeX[0] = tempX - 1
        snakeY[0] = tempY

    if snakeY[0] == foodY and snakeX[0] == foodX:
        foodY = random.randint(2, maxRows - 2)
        foodX = random.randint(2, maxCols - 2)
        snakeX.insert(1, tempX)
        snakeY.insert(1, tempY)

    # right wall
    if snakeX[0] == maxCols - 1:
        snakeX[0] = 1
    # left wall
    elif snakeX[0] == 1:
        snakeX[0] = maxCols - 2
    # upper wall
    elif snakeY[0] == 1:
        snakeY[0] = maxRows - 2
    # bottom wall
    elif snakeY[0] == maxRows - 1:
        snakeY[0] = 1

    for i in range(len(snakeX)):
        if foodX == snakeX[i] and foodY == snakeY[i]:
            foodY = random.randint(2, maxRows - 2)
            foodX = random.randint(2, maxCols - 2)

    return snakeX, snakeY, direction


def drawGameField():
    """ Draws the static parts of the game field and the scoreboard"""
    if (len(snakeX) - 4) // 6 == 0:
        gameSpeed = 200
    elif (len(snakeX) - 4) // 6 == 1:
        gameSpeed = 150
    elif (len(snakeX) - 4) // 6 == 2:
        gameSpeed = 100
    elif (len(snakeX) - 4) // 6 >= 3:
        gameSpeed = 50

    screen.timeout(gameSpeed)
    screen.border(0)
    box1 = curses.newwin(2, 2, 0, 0)
    # Automatically refreshes the box if window size is changed
    box1.immedok(True)
    screen.addstr(1, 1, "SCORE:" + str(len(snakeX) - 4))
    pressq = "Presss 'q' to quit"
    screen.addstr(maxRows - 2, maxCols - 2 - len(pressq), pressq)
    title = "The Ultimate Snake"
    screen.addstr(0, int((maxCols - len(title)) / 2), title)


def drawSnake(snakeY, snakeX):
    """ Draws all segments of the snake at given coordinates and in color"""
    for i in range(len(snakeX)):
        if i == 0:
            screen.addstr(snakeY[i], snakeX[i], "█", curses.color_pair(1))
        else:
            screen.addstr(snakeY[i], snakeX[i], "█", curses.color_pair(2))


def drawFood(y, x):
    """ Draws the food at given coordinates"""
    screen.addstr(y, x, "⦁")


def shiftRight(l):
    """ Takes a list as an input and shifts every element to the right"""
    return l[-1:] + l[:-1]


def gameOver():
    """ Game over text at the end """
    counter = 1
    with open('gameOver.txt') as f:
        for line in f:
            screen.addstr(counter, 17, line)
            counter += 1

    screen.addstr(15, 28, "Press 'SPACE' to try again.")

# -------------------Initialisation starts--------------------

# Curses module initialisation
screen = curses.initscr()
maxRows, maxCols = screen.getmaxyx()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
screen.nodelay(1)
curses.start_color()
stage = "Game"

# Used color pairs initialisation
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Starting position of the food
foodY = random.randint(2, maxRows - 2)
foodX = random.randint(2, maxCols - 2)

# X and Y coordinates of the starting position and direction of the snake
snakeX, snakeY, direction = zeroStage()

# Speed of the game
gameSpeed = 0.1  # the lower the value, the faster the game, but must be > 0
# --------------------Initialisation ends---------------------


# ---------------------Main loop starts-----------------------
while True:
    screen.erase()

    if stage == "Game":
        drawGameField()
        drawFood(foodY, foodX)
        (snakeX, snakeY, direction) = moveTheSnake(snakeX, snakeY, direction)
        drawSnake(snakeY, snakeX)

        if amIDeadYet(snakeX, snakeY, maxCols, maxRows):
            stage = "GameOver"

    elif stage == "GameOver":
        gameOver()
        if event == ord(" "):
            stage = "Game"
            snakeX, snakeY, direction = zeroStage(snakeX, snakeY, direction)
            screen.timeout(1)

    event = screen.getch()

    if event == ord("q"):
        break
    elif event == curses.KEY_UP and direction != "down":
        direction = "up"
    elif event == curses.KEY_DOWN and direction != "up":
        direction = "down"
    elif event == curses.KEY_LEFT and direction != "right":
        direction = "left"
    elif event == curses.KEY_RIGHT and direction != "left":
        direction = "right"


curses.endwin()
# ---------------------Main loop ends-------------------------
