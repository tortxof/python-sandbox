#! /usr/bin/env python3

for i in range(256):
    gray = (i >> 1) ^ i
    print(gray)
