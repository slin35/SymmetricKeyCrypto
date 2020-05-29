from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import urllib.parse

_pre = 'userid=456;userdata='
_post = ';session-id=31337'

_IV = os.urandom(16)
_key = os.urandom(16)
_str_IV = "".join(chr(c) for c in _IV)
_str_key = "".join(chr(c) for c in _key)

cipher = AES.new(_key, AES.MODE_ECB)


def submit(user_string: str) -> bytearray:
    query = _pre + user_string + _post
    url_encoded = urllib.parse.quote(query)
    print(url_encoded)
    return aes_128_cbc(url_encoded)


def aes_128_cbc(plain_text: str) -> bytearray:
    plain_text = bytes(plain_text, 'utf-8')
    blocks = [plain_text[i*16:(i+1)*16] for i in range(int(len(plain_text)/16))]
    last_block = plain_text[len(blocks) * 16:]
    result = bytearray()

    if len(last_block) > 0:
        blocks.append(PKCS_7_padding_encode(last_block, 16))

    for i in range(len(blocks)):
        if i == 0:
            encrypted_text = xor(blocks[i].decode('utf-8'), _str_IV)
        else:
            encrypted_text = xor(blocks[i].decode('utf-8'),  bytearrayToString(encrypted_text))

        encrypted_text = [ord(c) for c in encrypted_text]
        encrypted_text = cipher.encrypt(bytes(encrypted_text))
        result += encrypted_text

    return result


def verify(encoded_string:bytearray) -> bool:
    result = ""
    blocks = [encoded_string[i*16:(i+1)*16] for i in range(int(len(encoded_string)/16))]
    
    for i in range(len(blocks)):
        decrypted_text = cipher.decrypt(blocks[i])
        decrypted_text = bytearrayToString(decrypted_text)
        if i == 0:
            decrypted_text = xor(decrypted_text, _str_IV)
        else:
            decrypted_text = xor(decrypted_text, bytearrayToString(blocks[i-1]))

        if i == len(blocks) - 1:
            decrypted_text = PKCS_7_padding_decode(decrypted_text)
        
        result += decrypted_text

    return ';admin=true;' in result


def xor(str1:str, str2:str):
    if len(str1) != len(str2):
        print("unequal string lengths")
        exit(1)
    return "".join(chr(ord(x) ^ ord(y)) for (x, y) in zip(str1, str2))


def PKCS_7_padding_encode(block:bytearray, block_size:int) -> bytearray:
    to_pad = block_size - len(block) % block_size
    pad = bytes(chr(to_pad), 'utf-8')
    return block + pad * to_pad

'''
def PKCS_7_padding_decode(bytes:bytearray) -> bytearray:
    pad = ord(bytes.decode('utf-8')[-1])
    return bytes[:-pad]
'''
def PKCS_7_padding_decode(bytes:str) -> str:
    pad = ord(bytes[-1])
    return bytes[:-pad]

def bytearrayToString(barray:bytes) -> str:
    return "".join(chr(b) for b in barray)


def main():
   a = submit("hello;admin=true;")
   print(verify(a))


if __name__ == '__main__':
    main()

