import os

class Skippy:
    Sbox = [ 
        0x81, 0x3f, 0xab, 0x3d, 0xa4, 0xb4, 0x31, 0x9e,
        0xba, 0xee, 0x90, 0xec, 0x9f, 0x50, 0x85, 0x62,
        0xb8, 0xde, 0xa2, 0xf4, 0x08, 0x78, 0x0a, 0xc5,
        0xb3, 0x15, 0xa9, 0x27, 0x96, 0xac, 0x33, 0x11,
        0xa0, 0xdc, 0x05, 0x7b, 0xaf, 0xdd, 0xad, 0x7a,
        0x14, 0x9a, 0xb1, 0xaa, 0x29, 0x3b, 0x03, 0x23,
        0x99, 0x82, 0x3c, 0x98, 0x2b, 0x13, 0xa6, 0x21,
        0x2d, 0x63, 0x88, 0x51, 0x10, 0xc7, 0x9d, 0xf5,
        0x4c, 0x58, 0xf3, 0xd5, 0x65, 0x06, 0xc0, 0x91,
        0x5c, 0xd0, 0x76, 0xfa, 0xe6, 0x1a, 0xfc, 0x2a,
        0x5e, 0x6f, 0xd3, 0xf8, 0x6b, 0x97, 0x59, 0x18,
        0xf1, 0x68, 0xc3, 0x6a, 0xe8, 0x2e, 0x4d, 0x1c,
        0xd1, 0x5f, 0x44, 0x47, 0xcc, 0x00, 0xe4, 0xbf,
        0x7e, 0xcf, 0xe9, 0xcd, 0x7f, 0x04, 0x55, 0x89,
        0x7c, 0x40, 0xdb, 0x5a, 0x7d, 0x34, 0x67, 0x2c,
        0xe3, 0x5d, 0x46, 0xe2, 0xfe, 0x02, 0x69, 0x32,
        0x52, 0x87, 0xf7, 0x20, 0x79, 0x1d, 0x4b, 0x1f,
        0x09, 0x8e, 0x39, 0x1b, 0xa8, 0x0e, 0x0f, 0x0c,
        0xae, 0xbe, 0x0b, 0x19, 0x0d, 0x83, 0xb0, 0x26,
        0x48, 0x22, 0xef, 0x12, 0x49, 0x37, 0xf6, 0x92,
        0xb6, 0x94, 0x86, 0x01, 0x25, 0x3e, 0x17, 0x24,
        0xed, 0xb7, 0x60, 0xb5, 0x61, 0x35, 0xc6, 0x2f,
        0xdf, 0x3a, 0x4a, 0x38, 0x53, 0x8a, 0xc4, 0x07,
        0x84, 0xbc, 0x9c, 0x8c, 0xb2, 0x16, 0x80, 0x9b,
        0xbd, 0x71, 0x30, 0x73, 0xca, 0xe1, 0x75, 0x74,
        0xbb, 0xf0, 0x36, 0xea, 0xfd, 0x4e, 0xff, 0x64,
        0x8b, 0x4f, 0x1e, 0xc2, 0x70, 0x56, 0x72, 0x54,
        0xa5, 0xd6, 0xa7, 0xd4, 0x6d, 0xc9, 0x45, 0xf9,
        0xa3, 0xd8, 0xa1, 0xda, 0xd7, 0xeb, 0xe7, 0xd9,
        0x28, 0x41, 0x8d, 0x5b, 0xe0, 0xfb, 0xc8, 0x6e,
        0x95, 0xce, 0x8f, 0x43, 0xd2, 0xcb, 0x77, 0x6c,
        0xb9, 0xf2, 0x93, 0x57, 0xe5, 0xc1, 0x42, 0x66,
    ]

    def __init__(self, key):
        self._key = key + key[:2]

    def _g(self, k, w):
        g1 = w >> 8
        g2 = w & 0xff
        g3 = self.Sbox[g2 ^ self._key[(4 * k + 0) % 10]] ^ g1
        g4 = self.Sbox[g3 ^ self._key[(4 * k + 1) % 10]] ^ g2
        g5 = self.Sbox[g4 ^ self._key[(4 * k + 2) % 10]] ^ g3
        g6 = self.Sbox[g5 ^ self._key[(4 * k + 3) % 10]] ^ g4
        return (g5 << 8) ^ g6

    def _skip(self, b):
        w1 = (b[0] << 8) ^ b[1]
        w2 = (b[2] << 8) ^ b[3]
        w3 = (b[4] << 8) ^ b[5]
        w4 = (b[6] << 8) ^ b[7]
    
        k = 0
        for t in range(2):
            for i in range(8):
                gw1 = self._g(k, w1)
                w1, w2, w3, w4 = gw1 ^ w4 ^ (k + 1), gw1, w2, w3
                k += 1
            for i in range(8):
                gw1 = self._g(k, w1)
                w1, w2, w3, w4 = w4, gw1, w1 ^ w2 ^ (k + 1), w3
                k += 1
         
        return bytes([
            w1 >> 8, w1 & 0xff,
            w2 >> 8, w2 & 0xff,
            w3 >> 8, w3 & 0xff,
            w4 >> 8, w4 & 0xff,
        ])

    def encrypt(self, m):
        if len(m) % 8:
            m += b"\x00" * (8 - len(m) % 8)
        return b"".join(self._skip(m[i:i+8]) for i in range(0, len(m), 8))

k = os.urandom(8)
gourou = Skippy(k)

m = open("skippy.txt", "rb").read()
c = gourou.encrypt(m)
open("skippy.txt.enc", "wb").write(c)

m = open("flag.txt", "rb").read()
c = gourou.encrypt(m)
open("flag.txt.enc", "wb").write(c)
