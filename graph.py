import matplotlib.pyplot as plt
import numpy as np

'''
_rsa_key_size = [512, 1024, 2048, 4096]
_rsa_private_throughput = [1364351.2, 2211102.4, 313204.8, 47409.6]
_rsa_public_throughput = [25466651.2, 51004102.4, 10904204.8, 2921409.6]

plt.plot(_rsa_key_size, _rsa_private_throughput, 'r-o', label="private-rsa")
plt.plot(_rsa_key_size, _rsa_public_throughput, 'b-o', label="public-rsa")

plt.xlabel('RSA Key Size (bits)')
plt.ylabel('RSA Throughput (1e7bits/second')
plt.title('RSA Key Size vs. Throughput for Each RSA operation')

plt.legend()
plt.show()
'''

_aes_block_size = [16, 64, 256, 1024, 8192]
_aes_128_cbc_throughput = [22992269/3, 6214987/3, 1511894/3, 390916/3, 49424/3]
_aes_128_ige_throughput = [22046865/3, 5938100/3, 1515681/3, 373569/3, 4719/3]

plt.plot(_aes_block_size, _aes_128_cbc_throughput, 'r-o', label="aes-128-cbc")
plt.plot(_aes_block_size, _aes_128_ige_throughput, 'b-o', label="aes-128-ige")
plt.xlabel('AES-128 Block Size (bits)')
plt.ylabel('Throughput for Various Modes of Operations (bits/seconds)')
plt.title('AES-128 Block Size vs. Throughput for Various Modes of Operations')
plt.legend()
plt.show()