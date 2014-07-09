#! /usr/bin/env python3

msft = '2346789BCDFGHJKMPQRTVWXY'
base58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
alphabet = base58


def hasDuplicates(alphabet):
    for i in alphabet:
        if alphabet.count(i) > 1:
            return True
    return False


def basex(number, alphabet):
    myHash = ''
    if number == 0:
        myHash = alphabet[0]
    while number > 0:
        remainder = number % len(alphabet)
        number = number // len(alphabet)
        myHast += alphabet[remainder]
    return myHash[::-1]
