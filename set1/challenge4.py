#!/usr/bin/env python
'''Set 1 Challenge 4'''

from binascii import unhexlify
from challenge3 import find_single_byte_xor_key


def main():
    results = []
    f = open('4.txt')
    for ciphertext in f.readlines():
        possible_keys = find_single_byte_xor_key(unhexlify(ciphertext.strip()))
        for key in possible_keys:
            (plaintext, score) = possible_keys[key]
            results.append((score, ciphertext, plaintext))
    f.close()
    results = sorted(results,
                     cmp=lambda x, y: cmp(x[0], y[0]))
    min_score = results[0][0]
    for (score, ciphertext, plaintext) in results:
        if score == min_score:
            print ciphertext, plaintext
        else:
            break


if __name__ == '__main__':
    main()
