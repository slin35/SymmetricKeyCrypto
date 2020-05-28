from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def ecb(filename):
    file = open(filename, 'rb')
    img = bytearray(file.read())
    body = img[54:]
    file.close()

    result = open("encrypted_ecb_" + filename, "wb")
    result.write(img[:54])

    key = get_random_bytes(16)
    cipher = AES.new(key=key, mode=AES.MODE_ECB)

    img_blocks = [img[i*16:(i+1)*16] for i in range(int(len(body)/16))]
    last_block = body[len(img_blocks) * 16:]
    if (len(last_block) > 0):
        img_blocks.append(PKCS_7_padding(last_block, 16))
    
    for block in img_blocks:
        result.write(cipher.encrypt(block))

    result.close()


def PKCS_7_padding(block, block_size):
    to_pad = block_size - len(block) % block_size
    pad = to_pad.to_bytes(1, 'big')
    return block + pad * to_pad


def xor(str1, str2):
    if (len(str1) != len(str2)):
        print("unequal string lengths")
        exit(1)
    return "".join(chr(ord(x) ^ ord(y)) for (x, y) in zip(str1, str2))


def cbc(filename):
    file = open(filename, 'rb')
    img = bytearray(file.read())
    body = img[54:]
    file.close()

    result = open("encrypted_cbc_" + filename, "wb")
    result.write(img[:54])

    img_blocks = [img[i*16:(i+1)*16] for i in range(int(len(body)/16))]
    last_block = body[len(img_blocks) * 16:]
    if (len(last_block) > 0):
        img_blocks.append(PKCS_7_padding(last_block, 16))

    # xor first block with IV and encrypt with the key
    IV = os.urandom(16)
    key = get_random_bytes(16)
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    encrypted_text = xor(bytearrayToString(img_blocks[0]), bytearrayToString(key))
    encrypted_array = [ord(ch) for ch in encrypted_text]
    encrypted_bytes_array = bytes(encrypted_array)
    cipher_text = cipher.encrypt(encrypted_bytes_array)
    result.write(cipher_text)

    for i in range(1, len(img_blocks)):
        encrypted_text = xor(bytearrayToString(img_blocks[i]), bytearrayToString(cipher_text))
        encrypted_array = [ord(ch) for ch in encrypted_text]
        encrypted_bytes_array = bytes(encrypted_array)
        cipher_text = cipher.encrypt(encrypted_bytes_array)
        result.write(cipher_text)

    result.close()


def bytearrayToString(barray:bytearray) -> str:
    return "".join(chr(b) for b in barray)


def main():
    cbc('mustang.bmp')


if __name__ == '__main__':
    main()