#! /usr/bin/env python3
import sys
import random
numdice = 5
numsides = 6
if len(sys.argv) > 1:
    numdice = int(sys.argv[1])
if len(sys.argv) > 2:
    numsides = int(sys.argv[2])
if numdice < 2:
    numdice = 2
if numsides < 2:
    numsides = 2
roll = 0
yahtzee = 0

while yahtzee == 0:
    roll += 1
    rollresult = []
    for i in range(numdice):
        rollresult.append(random.randrange(numsides))
    for side in range(numsides):
        numequal = 0
        for die in range(numdice):
            if rollresult[die] == side:
                numequal += 1
        if numequal == numdice:
            yahtzee += 1
            print("Roll:", roll)
            for i in rollresult:
                print(i + 1, end=' ')
            print()
