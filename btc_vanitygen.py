#! /usr/bin/env python3

import os
from pycoin.key import Key

def vanitygen(s):
    s = '1' + s.lower()
    l = len(s)
    while True:
        r = int.from_bytes(os.urandom(32), 'big')
        k = Key(secret_exponent=r)
        if k.address()[:l] == s:
            print('Address:', k.address())
            print('WIF:'. k.wif())
