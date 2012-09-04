#! /usr/bin/env python3.2
blocksize = abs(int(input("Block size: ")))
x = y = 0
while x <= 1024 * 8:
    y += blocksize
    x = (y / 9) * 16
    if x % blocksize == 0:
        print(int(x), y)
