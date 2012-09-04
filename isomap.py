#! /usr/bin/env python3.2
import sys

gridsize = 5

if len(sys.argv) > 1:
    gridsize = abs(int(sys.argv[1]))

x = y = 0
for i in range(gridsize):
    for x in range(i + 1):
        y = i - x
        print(x, y)
for i in range(gridsize, (gridsize - 1) * 2):
    for x in range(i - gridsize + 1, gridsize ):
        y = i - x
        print(x, y)
print(gridsize - 1, gridsize - 1)
