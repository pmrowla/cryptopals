#!/usr/bin/env python
'''Set 1 Challenge 2'''

from binascii import hexlify, unhexlify
from struct import unpack


def xor_buffers(buf1, buf2):
    '''XOR two equal length buffers'''
    if len(buf1) != len(buf2):
        raise ValueError('Buffers must be equal length')
    out = []
    for i in range(len(buf1)):
        (a,) = unpack('B', buf1[i])
        (b,) = unpack('B', buf2[i])
        out.append(chr(a ^ b))
    return ''.join(out)


def main():
    hex_str1 = '1c0111001f010100061a024b53535009181c'
    hex_str2 = '686974207468652062756c6c277320657965'
    result = xor_buffers(unhexlify(hex_str1), unhexlify(hex_str2))
    print hexlify(result)


if __name__ == '__main__':
    main()
