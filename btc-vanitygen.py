#! /usr/bin/env python3

import os
from pycoin.key import Key

def vanitygen(s):
    s = s.lower()
    while True:
        r = int.from_bytes(os.urandom(32), 'big')
        k = Key(secret_exponent=r)
        if k.address()[:len(s)+1].lower() == '1' + s:
            print('Address:', k.address())
            print('WIF:'. k.wif())
