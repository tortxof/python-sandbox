#! /usr/bin/env python3.2

import random

cycles = 1000000
passes = 0

def large_random(base=1000, exponent=100):
    return random.randrange(1,base) ** random.randrange(1,exponent)

while True:
    for i in range(cycles):
        z = float(large_random()) / float(large_random())
    passes += 1
    print(passes, "passes.")
