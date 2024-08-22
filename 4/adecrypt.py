"""Hacker101: challenge 4"""

import base64
import asyncio
from aiohttp import ClientSession
from cryptography.hazmat.primitives import padding
from rich import print
import wat


class Decryptor:

    def __init__(self, url, session):
        self.session = session
        self.url = url
    
    async def padding_oracle(self, iv, ciphertxt):
        """Returns true if padding is correct, false otherwise"""
        async with self.session.get(self.url, params={'post': self.b64urlenc(iv + ciphertxt)}) as response:
            content = await response.text(encoding='utf-8')
            return (
                    'PaddingException' not in content
                and 'ValueError: IV must be 16 bytes long' not in content
                and 'ValueError: Input strings must be a multiple of 16 in length' not in content
                and '502 Bad Gateway' not in content
            )
    
    async def probe_padding_oracle(self, iv, ciphertxt, i):
        return i, await self.padding_oracle(iv, ciphertxt)
    
    async def find_pad_byte(self, C0, C1, C2):
        C1_prime = [self.change_byte(bytes([i]), -1, C1) for i in range(256)]
        C1_second = [self.change_byte(bytes([(C1_prime[i][-2] >> 1) ^ C1_prime[i][-2]]), -2, C1_prime[i]) for i in range(256)]
        
        tasks = [self.probe_padding_oracle(C0, C1_prime[i] + C2, i) for i in range(256)]
        task_pool = asyncio.as_completed(tasks)
        for task in task_pool:
            i, result = await task
            if result:
                padding_found = await self.padding_oracle(C0, C1_second[i] + C2)
                if padding_found:
                    task_pool.close()
                    return bytes([C1_prime[i][-1] ^ 0x01 ^ C1[-1]])
    
    async def decrypt_block(self, C0, C1, C2):
        P2 = pad_byte = await self.find_pad_byte(C0, C1, C2)

        C1_init = C1
    
        for i in range(1, 16):
            C1 = C1_init

            for j in range(1, i+1):
                C1 = self.change_byte(bytes([P2[-j] ^ C1[-j] ^ (i+1)]), -j, C1)

            C1_prime = [self.change_byte(bytes([k]), -(i+1), C1) for k in range(256)]
            tasks = [self.probe_padding_oracle(C0, C1_prime[k] + C2, k) for k in range(256)]
            task_pool = asyncio.as_completed(tasks)
            for task in task_pool:
                idx, result = await task
                if result:
                    pad_byte = bytes([C1_prime[idx][-(i+1)] ^ (i+1) ^ C1[-(i+1)]])
                    task_pool.close()
                    break
            
            P2 = pad_byte + P2

        return P2
    

    async def padding_oracle_attack(self, iv, ciphertxt):
        blks = [b'\x00' * 16, iv] + self.B(ciphertxt)
        tasks = [self.decrypt_block(blks[i], blks[i+1], blks[i+2]) for i in range(len(blks) - 3 + 1)]
        return self.unpad(b''.join(await asyncio.gather(*tasks)))


    @staticmethod
    def b64urldec(data):
        return base64.b64decode(data.replace(b'~', b'=').replace(b'!', b'/').replace(b'-', b'+'))
    
    @staticmethod
    def b64urlenc(data):
        return base64.b64encode(data).replace(b'=', b'~').replace(b'/', b'!').replace(b'+', b'-').decode('utf-8')

    @staticmethod
    def unpad(plain):
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(plain) + unpadder.finalize()

    @staticmethod
    def B(s):
        return [s[i:i+16] for i in range(0, len(s), 16)]
    
    @staticmethod
    def change_byte(b, pos, B):
        pos = pos % len(B)
        return B[:pos] + b + B[pos+1:]


async def main(url, cipher):
    async with ClientSession() as session:
        d = Decryptor(url, session)
        iv, ciphertxt = cipher[:16], cipher[16:]
        result = await d.padding_oracle_attack(iv, ciphertxt)
        result = result.decode('utf-8')
        print(result)

        cipher_blocks = Decryptor.B(ciphertxt)
        plain_blocks = Decryptor.B(result)

        for c, p in zip(cipher_blocks, plain_blocks):
            print(c, ' -> ', p)

if __name__ == '__main__':
    url = 'https://c1174c62dad6f53bad389a2b5a576532.ctf.hacker101.com/'
    cipher = Decryptor.b64urldec(b'pkiXK9!o8SuB765yS3demEaA3XAZhhCjs-zc1!LcV!7VyoWSRUXbKIhQ4HmpgO74CTYJx!eJRPgExwbiDMYCCxZilxXqV6xj2cV0bWWDqLbBopYnA2y56o1Cwhx1Lb38k787UlHmMYTMtGSQGhQ0ejpMQGsxhaz7P2KIHbfiP5PRtjadc-dRtSPHMohHmyWyIcTdhMS3EbI2gItyUCSF4A~~')
    cipher = Decryptor.b64urldec(b'ec6j!KjXvSypWLumZZfOBvPcTPVFJjXRaQ7mqz4oEOcummIZL-hp!9s8iVPwd7YUKljGYnsrd1t0e0h-St3so0PliJ0q4L!X1GUsYdjIxjI6U4L2U!hfleSIg8!qbYlapWwkgD3DI5sDnIocJVBTbR8NDWpGlR8yGHmIR2oT4m2C4Mu-KWGIBROR-6zU95Jg!S3iTFaFLQjPPSBrs1!t-w~~')
    asyncio.run(main(url, cipher))