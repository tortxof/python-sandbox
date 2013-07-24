#! /usr/bin/env python3

import sys
import random
numflips = 5
if len(sys.argv) > 1:
    numflips = int(sys.argv[1])
if numflips < 2:
    numflips = 2
flip = 0
goodflips = 0

while goodflips < numflips:
    flip += 1
    flipresult = random.randrange(2)
    if flipresult == 1:
        goodflips += 1
    else:
        goodflips = 0
print("Total flips:", flip)
print(goodflips, "heads in a row.")
