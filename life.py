#! /usr/bin/env python3

import random
import time
import sys

class Field:
    def __init__(self, sizex, sizey):
        self.sizex = sizex
        self.sizey = sizey
        self.field = [[[0, 0] for i in range(self.sizey)] for i in range(self.sizex)]
        self.generation = 0

    def draw(self):
        row = ['' for i in range(self.sizey)]
        for y in range(self.sizey):
            for x in range(self.sizex):
                if self.field[x][y][0] == 1:
                    row[y] += '*'
                else:
                    row[y] += '-'
        print("\n\n")
        for i in row:
            print(i)

    def writepbm(self):
        filename = str(self.generation).zfill(8) + '.pbm'
        file = open(filename, 'wt')
        file.write('P1\n')
        file.write('{} {}\n'.format(self.sizex, self.sizey))
        for y in range(self.sizey):
            row = ''
            for x in range(self.sizex):
                if x > 0:
                    row += ' '
                row += str(self.field[x][y][0])
            row += '\n'
            file.write(row)
        file.close()

    def tick(self):
        self.generation += 1
        for x in range(self.sizex):
            for y in range(self.sizey):
                numNeighbors = 0
                for nx in range(x-1, x+2):
                    for ny in range(y-1, y+2):
                        if nx < 0:
                            nx += self.sizex
                        if ny < 0:
                            ny += self.sizey
                        if nx >= self.sizex:
                            nx -= self.sizex
                        if ny >= self.sizey:
                            ny -= self.sizey
                        if not (x == nx and y == ny):
                            numNeighbors += self.field[nx][ny][0]
                if self.field[x][y][0] == 1 and numNeighbors < 2:
                    self.field[x][y][1] = 0
                elif self.field[x][y][0] == 1 and (numNeighbors == 2 or numNeighbors == 3):
                    self.field[x][y][1] = 1
                elif self.field[x][y][0] == 1 and numNeighbors > 3:
                    self.field[x][y][1] = 0
                elif self.field[x][y][0] == 0 and numNeighbors == 3:
                    self.field[x][y][1] = 1
                else:
                    self.field[x][y][1] = 0
        for x in range(self.sizex):
            for y in range(self.sizey):
                self.field[x][y][0] = self.field[x][y][1]

    def randomize(self):
        for x in range(self.sizex):
            for y in range(self.sizey):
                self.field[x][y][0] = random.randrange(2)

maxGenerations = 2000

f1 = Field(1280, 720)
f1.randomize()


while True:
#   f1.draw()
    f1.writepbm()
    print(f1.generation)
    f1.tick()
    if not (maxGenerations > 0 and f1.generation < maxGenerations):
        sys.exit(0)
#   time.sleep(sleeptime)
