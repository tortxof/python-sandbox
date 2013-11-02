#! /usr/bin/env python3

# alphabet = '2346789BCDFGHJKMPQRTVWXY'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def numduplicates(alphabet):
    count = 0
    for i in alphabet:
        if alphabet.count(i) > 1:
            count += 1
    return(count)

if numduplicates(alphabet) > 0:
    print('Duplicate characters in alphabet.')
    exit(1)

number = int(input('Enter a positive integer:'))

hash = ''

if number == 0:
    hash = alphabet[0]

while number:
    remainder = number % len(alphabet)
    number = number // len(alphabet)
    hash += alphabet[remainder]

hash = hash[::-1]

print(hash)
