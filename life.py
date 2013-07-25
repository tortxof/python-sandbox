#! /usr/bin/env python3

import random
import time

updaterate = 24
sizex = 120
sizey = 50
field = [[[0, 0] for i in range(sizey)] for i in range(sizex)]
sleeptime = 1 / updaterate
generation = 0

def drawField():
    global field
    row = ['' for i in range(sizey)]
    for y in range(sizey):
        for x in range(sizex):
            if field[x][y][0] == 1:
                row[y] += '*'
            else:
                row[y] += '-'
    print("\n\n")
    for i in row:
        print(i)

def tickField():
    global field
    global generation
    generation += 1
    for x in range(sizex):
        for y in range(sizey):
            numNeighbors = 0
            for nx in range(x-1, x+2):
                for ny in range(y-1, y+2):
                    if nx < 0:
                        nx += sizex
                    if ny < 0:
                        ny += sizey
                    if nx >= sizex:
                        nx -= sizex
                    if ny >= sizey:
                        ny -= sizey
                    if not (x == nx and y == ny):
                        numNeighbors += field[nx][ny][0]
            if field[x][y][0] == 1 and numNeighbors < 2:
                field[x][y][1] = 0
            elif field[x][y][0] == 1 and (numNeighbors == 2 or numNeighbors == 3):
                field[x][y][1] = 1
            elif field[x][y][0] == 1 and numNeighbors > 3:
                field[x][y][1] = 0
            elif field[x][y][0] == 0 and numNeighbors == 3:
                field[x][y][1] = 1
            else:
                field[x][y][1] = 0
    for x in range(sizex):
        for y in range(sizey):
            field[x][y][0] = field[x][y][1]

def randomField():
    global field
    for x in range(sizex):
        for y in range(sizey):
            field[x][y][0] = random.randrange(2)

randomField()

while True:
    drawField()
    print(generation)
    tickField()
    time.sleep(sleeptime)
