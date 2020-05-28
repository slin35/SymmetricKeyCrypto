from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import urllib.parse

_pre = 'userid=456;userdata='
_post = ';session-id=31337'

_IV = os.urandom(16)
_key = os.urandom(16)


def submit(user_string: str) -> bytearray:
    query = _pre + user_string + _post
    url_encoded = urllib.parse.quote(query)
    return aes_128_cbc(url_encoded, _IV, _key)


def aes_128_cbc(plain_text: str, IV:str, key:str) -> bytearray:
    blocks = [plain_text[i*16:(i+1)*16] for i in range(int(len(plain_text)/16))]
    last_block = plain_text[len(blocks) * 16:]

    if len(last_block) > 0:
        blocks.append(PKCS_7_padding(last_block, 16))

    # encrypt the first block
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    cipher_text = xor(blocks[0], bytearrayToString(_IV))
    cipher_array = [ord(ch) for ch in cipher_text]
    cipher_text = cipher.encrypt(bytes(cipher_array))
    result = cipher_text

    for i in range(1, len(blocks)):
        cipher_text = xor(blocks[i], bytearrayToString(cipher_text))
        cipher_array = [ord(ch) for ch in cipher_text]
        cipher_text = cipher.encrypt(bytes(cipher_array))
        result += cipher_text

    return result


def xor(str1:str, str2:str) -> str:
    if len(str1) != len(str2):
        print("unequal string lengths")
        exit(1)
    return "".join(chr(ord(x) ^ ord(y)) for (x, y) in zip(str1, str2))


def PKCS_7_padding(block:str, block_size:int) -> str:
    to_pad = block_size - len(block) % block_size
    pad = chr(to_pad)
    return block + pad * to_pad


def bytearrayToString(barray:bytearray) -> str:
    return "".join(chr(b) for b in barray)


def main():
    print(submit("hello"))


if __name__ == '__main__':
    main()

