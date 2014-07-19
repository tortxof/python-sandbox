#! /usr/bin/env python3

def binToGray(i):
    return (i >> 1) ^ i

if __name__ == '__main__':
    for i in range(256):
        print('{0:08b}'.format(binToGray(i)))
