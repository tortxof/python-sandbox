#! /usr/bin/env python3

def collatz(n):
    if n == 1:
        return 1
    elif n % 2 == 0:
        return n // 2
    else:
        return 3*n + 1

if __name__ == "__main__":
    import random
    i = random.randrange(1000000)
    while i > 1:
        i = collatz(i)
        print(i)
