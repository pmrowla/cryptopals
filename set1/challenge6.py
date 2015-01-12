#!/usr/bin/env python
'''Set 1 Challenge 6'''


from __future__ import division

from base64 import b64decode
from struct import unpack
from challenge2 import xor_buffers
from challenge3 import find_single_byte_xor_key, score_plaintext
from challenge5 import repeating_xor_encrypt


def edit_distance(a, b):
    '''Compute the Hamming distance between two strings'''
    if len(a) > len(b):
        b = '%s%s' % (b, '\x00' * (len(a) - len(b)))
    elif len(b) > len(a):
        a = '%s%s' % (a, '\x00' * (len(b) - len(a)))
    c = xor_buffers(a, b)
    distance = 0
    for byte in c:
        (x,) = unpack('B', byte)
        x = (x & 0x55) + ((x >> 1) & 0x55)
        x = (x & 0x33) + ((x >> 2) & 0x33)
        x = (x & 0x0f) + ((x >> 4) & 0x0f)
        distance += x
    return distance


def find_keysize(ciphertext):
    max_keysize = 40
    if len(ciphertext) < 40:
        max_keysize = len(ciphertext)
    keysize_distances = []
    for keysize in range(2, max_keysize + 1):
        normalized_distance = 0.0
        for i in range(0, 10, 2):
            a = ciphertext[i * keysize:(i + 1) * keysize]
            b = ciphertext[(i + 1) * keysize:(i + 2) * keysize]
            normalized_distance += edit_distance(a, b) / keysize
        normalized_distance = normalized_distance / 5
        keysize_distances.append((keysize, normalized_distance))
    keysize_distances = sorted(keysize_distances,
                               cmp=lambda x, y: cmp(x[1], y[1]))
    return [keysize_distances[0][0], keysize_distances[1][0]]


def transpose_blocks(ciphertext, keysize):
    ciphertext += '\x00' * (keysize - len(ciphertext) % keysize)
    blocks = []
    for i in range(0, len(ciphertext), keysize):
        block = ciphertext[i:i + keysize]
        blocks.append(block)
    transposed = [''] * keysize
    for i in range(keysize):
        for block in blocks:
            transposed[i] += block[i]
    return transposed


def decrypt_repeating_xor(ciphertext):
    xor_keys = []
    for keysize in find_keysize(ciphertext):
        transposed = transpose_blocks(ciphertext, keysize)
        xor_key = ''
        for i, block in enumerate(transposed):
            possible_keys = find_single_byte_xor_key(block)
            for key in possible_keys:
                xor_key += chr(key)
                break
        xor_keys.append((xor_key, score_plaintext(xor_key)))
        # for XOR encrypt is the same as decrypt
    xor_keys = sorted(xor_keys,
                      cmp=lambda x, y: cmp(x[1], y[1]))
    return repeating_xor_encrypt(ciphertext, xor_key)


def main():
    assert(edit_distance('this is a test', 'wokka wokka!!!') == 37)
    f = open('6.txt')
    ciphertext = f.read()
    f.close()
    ciphertext = b64decode(ciphertext)
    print decrypt_repeating_xor(ciphertext)


if __name__ == '__main__':
    main()
