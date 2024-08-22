# Tracking pickel data

Maybe the app uses this as a web beacon to check if get requests are being done from a browser?

```bash
00000000: 4749 4638 3961 0100 0100 8001 00ff ffff  GIF89a..........
00000010: 0000 0021 f904 010a 0001 002c 0000 0000  ...!.......,....
00000020: 0100 0100 0002 024c 0100 3b              .......L..;
```

# Application

# GET

`page=`

## Result

```Python
Traceback (most recent call last):
  File "./main.py", line 69, in index
    post = json.loads(decryptLink(postCt).decode('utf8'))
  File "./common.py", line 48, in decryptLink
    cipher = AES.new(staticKey, AES.MODE_CBC, iv)
  File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/AES.py", line 95, in new
    return AESCipher(key, *args, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/AES.py", line 59, in __init__
    blockalgo.BlockAlgo.__init__(self, _AES, key, *args, **kwargs)
  File "/usr/local/lib/python2.7/site-packages/Crypto/Cipher/blockalgo.py", line 141, in __init__
    self._cipher = factory.new(key, *args, **kwargs)
ValueError: IV must be 16 bytes long
```

## GET

`post=a`

## Result

```Python
Traceback (most recent call last):
  File "./main.py", line 69, in index
    post = json.loads(decryptLink(postCt).decode('utf8'))
  File "./common.py", line 46, in decryptLink
    data = b64d(data)
  File "./common.py", line 11, in <lambda>
    b64d = lambda x: base64.decodestring(x.replace('~', '=').replace('!', '/').replace('-', '+'))
  File "/usr/local/lib/python2.7/base64.py", line 328, in decodestring
    return binascii.a2b_base64(s)
Error: Incorrect padding
```

## Note

URL safe encoding / decoding logic:

`b64d = lambda x: base64.decodestring(x.replace('~', '=').replace('!', '/').replace('-', '+'))`

# POST

`title=test&body=hello`

## URL

`https://b1d3425ccf7b3cf1628f350d5cf54388.ctf.hacker101.com/?post=zyWe9iyuzkDVAgGBISE2jTEGwqEwmEb0OpAZP7LrCJ9CN6e0LUxYLUF2GU18VAl40GlQ-zEjZa-LdDesR8POVOY2cS1JzM5rsAP7x0rOJCEyOM--8Nm3EWKCoH6UY-lW1IsHbZTJ8tpdJ8TuxVayI4nE0CgOByz7O9IRrpTX0vAQFkwbWAQtlsdhgvZuK-Y-zgrTjS5Xl0Pst5CSByyBYA~~`

## POST

`title=&body=`

## URL

`https://b1d3425ccf7b3cf1628f350d5cf54388.ctf.hacker101.com/?post=aSUGWYkAqGxQ2cNK3Z4cVVL1qZUDZDNsOBGIwC9Zh8KDEybMsnORYRejUJZP0FAljm6sIGInchnQS8KOjXROrXh2E4Ft0658b5N5Wjj-me7aF9ZjYz8T37TaZfvqJUqTyAzCyq4RaRjzZZ8VOgtAaPw4z9-VUjvIeZ9CqOEERtlaBp8Q2qddeuTPP07Lgsk0hm-QNgejR3wYjhWIO2iG1A~~`


## New session, but old cipher:

```
https://11ffc860e7d402e1dc8038ae0d2f0302.ctf.hacker101.com/?post=zyWe9iyuzkDVAgGBISE2jTEGwqEwmEb0OpAZP7LrCJ9CN6e0LUxYLUF2GU18VAl40GlQ-zEjZa-LdDesR8POVOY2cS1JzM5rsAP7x0rOJCEyOM--8Nm3EWKCoH6UY-lW1IsHbZTJ8tpdJ8TuxVayI4nE0CgOByz7O9IRrpTX0vAQFkwbWAQtlsdhgvZuK-Y-zgrTjS5Xl0Pst5CSByyBYA~~
```

```Python
Attempting to decrypt page with title: title
Traceback (most recent call last):
  File "./main.py", line 74, in index
    body = decryptPayload(post['key'], body)
  File "./common.py", line 37, in decryptPayload
    return unpad(cipher.decrypt(data))
  File "./common.py", line 22, in unpad
    raise PaddingException()
PaddingException
```

```
Attempting to decrypt page with title: title
```

The title is not encrypted ??? -> no, the post parameter is kind of a session cookie or something
