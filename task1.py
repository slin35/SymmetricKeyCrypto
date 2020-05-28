from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def ecb(filename):
    file = open(filename, 'rb')
    img = bytearray(file.read())
    body = img[54:]
    file.close()

    result = open("encrypted_" + filename, "wb")
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


def cbc(filename):
    pass


def main():
    ecb('cp-logo.bmp')


if __name__ == '__main__':
    main()