#! /usr/bin/env python3

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
