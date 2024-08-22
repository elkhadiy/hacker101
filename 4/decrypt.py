from concurrent.futures import ThreadPoolExecutor, as_completed

import base64
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import requests as rq

import time


def unpkcs7(plain):
    if 1 <= plain[-1] <= 16 and plain[-plain[-1]:] == bytes([plain[-1]]) * plain[-1]:
        return plain[:-plain[-1]]
    else:
        raise ValueError("Bad padding")

B = lambda s: [s[i:i+16] for i in range(0, len(s), 16)]

def change_byte(b, pos, B):
    pos = pos % len(B)
    return B[:pos] + b + B[pos+1:]



def break_P2(C0, C1, C2, padding_oracle):

    P2 = b''
    C1_blkp = C1

    for i in range(256):
        C1_prime = change_byte(bytes([i]), -1, C1)
        if padding_oracle(C0, C1_prime + C2):
            C1_second = change_byte(bytes([(C1_prime[-2] >> 1) ^ C1_prime[-2]]), -2, C1_prime)
            if padding_oracle(C0, C1_second + C2):
                pad_byte = bytes([C1_prime[-1] ^ 0x01 ^ C1[-1]])
                break

    P2 = pad_byte + P2

    for i in range(1, 16):

        C1 = C1_blkp

        for j in range(1, i+1):
            C1 = change_byte(bytes([P2[-j] ^ C1[-j] ^ (i+1)]), -j, C1)

        for k in range(256):
            C1_prime = change_byte(bytes([k]), -(i+1), C1)
            if padding_oracle(C0, C1_prime + C2):
                pad_byte = bytes([C1_prime[-(i+1)] ^ (i+1) ^ C1[-(i+1)]])
                break

        P2 = pad_byte + P2

        print(f"\rDecrypting block: {P2}", end="")
    
    print("")
    
    return P2


def padding_oracle_attack(iv, ciphertxt, padding_oracle):
    blks = [b'\x00' * 16, iv] + B(ciphertxt)
    return unpkcs7(b''.join([break_P2(blks[i], blks[i+1], blks[i+2], padding_oracle) for i in range(len(blks) - 3 + 1)]))


b64d = lambda x: base64.b64decode(x.replace(b'~', b'=').replace(b'!', b'/').replace(b'-', b'+'))
b64e = lambda x: base64.b64encode(x).replace(b'=', b'~').replace(b'/', b'!').replace(b'+', b'-')

def decryption_oracle(data):
    url = 'https://11ffc860e7d402e1dc8038ae0d2f0302.ctf.hacker101.com/'
    response = rq.get(url, params={'post': b64e(data)}).content.decode('utf-8')
    time.sleep(0.1)
    return response

def padding_oracle(iv, ciphertxt):
    response = decryption_oracle(iv + ciphertxt)
    while '502 Bad Gateway' in response:
        response = decryption_oracle(iv + ciphertxt)
    padding_exception = 'PaddingException' in response
    if not padding_exception and 'UnicodeDecodeError:' not in response:
        print(f"\n{response}\n")
    return not padding_exception




if __name__ == '__main__':

    cipher = b64d(b'z6Fs5eGxe5JhCHrodvFYrTzae87ym0Rca!8xEFYXHyngLfaHCyMBDd3!GRsKXu-BWazdQgzI6aj4ORJBUt0ORkH3rq9uG9EpQAXAP1xyYCnjZLhfYvigCj22TVA01s8!dKUleFpjL!4wUTKrRLV7qRKRjtsHZxhCih4tsu8NPAXuUQBiUldxsOasxaVBHRWTkI4VysZpC7!L2NImqZw!AA~~')
    iv, ciphertxt = cipher[:16], cipher[16:]
    plaintxt = padding_oracle_attack(iv, ciphertxt, padding_oracle)
    print(plaintxt)
