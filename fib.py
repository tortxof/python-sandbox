#! /usr/bin/env python3

def fib_gen(a=0, b=1):
    while True:
        yield a
        a, b = b, a + b

if __name__ == '__main__':
    for i, x in enumerate(fib_gen(2, 1)):
        if i < 1000:
            print(i, x)
        else:
            break
