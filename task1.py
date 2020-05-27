from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def ecb(filename):
    file = open(filename, 'rb')
    img = bytearray(file.read())
    body = img[54:]
    file.close()

    result = open("encrypted_" + filename, "wb")
    result.write(img[:54])

    # TO-DO: set up cipher for encryption without modes of operation
    key = get_random_bytes(16)
    cipher = AES.new(key=key)

    # TO-DO: PKCS #7 padding 
    img_blocks = [img[i*16:(i+1)*16] for i in range(len(body))]

    # TO-DO: encrypt and concat result for each block
    for block in img_blocks:
        pass
    
def cbc(filename):
    pass


def main():
    ecb('cp-logo.bmp')


if __name__ == '__main__':
    main()