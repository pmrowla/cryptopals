#!/usr/bin/env python
'''Set 1 Challenge 3'''


from __future__ import division

from binascii import unhexlify
from collections import defaultdict
from challenge2 import xor_buffers


# according to http://en.wikipedia.org/wiki/Letter_frequency
ENGLISH_LETTER_FREQUENCY = {
    'a': 0.08167,
    'b': 0.01492,
    'c': 0.02782,
    'd': 0.04253,
    'e': 0.12702,
    'f': 0.02228,
    'g': 0.02015,
    'h': 0.06094,
    'i': 0.06966,
    'j': 0.00153,
    'k': 0.00772,
    'l': 0.04025,
    'm': 0.02406,
    'n': 0.06749,
    'o': 0.07507,
    'p': 0.01929,
    'q': 0.00095,
    'r': 0.05987,
    's': 0.06327,
    't': 0.09056,
    'u': 0.02758,
    'v': 0.00978,
    'w': 0.02360,
    'x': 0.00150,
    'y': 0.01974,
    'z': 0.00074,
}


def single_byte_xor_decrypt(ciphertext, key):
    '''Decrypt a ciphertext using single-byte XOR'''
    extended_key = key * len(ciphertext)
    return xor_buffers(ciphertext, extended_key)


def score_plaintext(plaintext):
    '''Score a plaintext based on English character frequency'''
    char_counts = defaultdict(int)
    plaintext_chars = 0
    for c in plaintext.lower():
        # ignore punction and non-printable characters
        if c in ENGLISH_LETTER_FREQUENCY:
            char_counts[c] += 1
            plaintext_chars += 1
    score = 0.0
    for c, expected_freq in ENGLISH_LETTER_FREQUENCY.items():
        if c in char_counts:
            observed_freq = char_counts[c] / plaintext_chars
        else:
            observed_freq = 0.0
        score += abs(expected_freq - observed_freq)
    return score


def find_single_byte_xor_key(ciphertext):
    '''Test all possible single-byte XOR keys for the given ciphertext'''
    plaintext_scores = []
    for i in range(1, 256):
        key = i
        plaintext = single_byte_xor_decrypt(ciphertext, chr(i))
        score = score_plaintext(plaintext)
        plaintext_scores.append((key, score, plaintext))
    plaintext_scores = sorted(plaintext_scores,
                              cmp=lambda x, y: cmp(x[1], y[1]))
    possible_keys = {}
    min_score = plaintext_scores[0][1]
    for key, score, plaintext in plaintext_scores:
        if score == min_score:
            possible_keys[key] = (plaintext, score)
        else:
            break
    return possible_keys


def main():
    ciphertext = \
        '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    possible_keys = find_single_byte_xor_key(unhexlify(ciphertext))
    print '[ Key ] | Plaintext'
    print '--------+----------'
    for key in possible_keys:
        (plaintext, score) = possible_keys[key]
        if '\x00' in plaintext:
            continue
        print '[ %3d ] | %s' % (key, possible_keys[key])


if __name__ == '__main__':
    main()
