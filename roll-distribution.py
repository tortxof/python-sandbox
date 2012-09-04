#! /usr/bin/env python3.2
import random

for n in range(10):
    heads = tails = 0
    for i in range(1000000):
        if random.randrange(2):
            heads += 1
        else:
            tails += 1
    print(heads, tails)
