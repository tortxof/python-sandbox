#! /usr/bin/env python3.2

for i in range(256):
    gray = (i >> 1) ^ i
    print(gray)
