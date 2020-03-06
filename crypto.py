# Encrypt/Decrypt in CTR mode using PyCrypto playground
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA
from Crypto.Util import Counter
from Crypto import Random
import sys

# Encryption
key = b'Sixteen byte key'
key = SHA.new(key).hexdigest()
key = bytearray(key.encode())
key = list(key)
del key[16:]
key = bytes(key)
print(key)
print(type(key))
print(len(key))

iv = Random.new().read(AES.block_size)
iv = int.from_bytes(iv, byteorder=sys.byteorder)
iv = iv ^ 1
print(type(iv))

plaintext = input('Enter message: ')

ctr = Counter.new(128, initial_value=iv) # 16 bytes = 128 bits
cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
ciphertext = cipher.encrypt(plaintext)
print("Ciphertext: " + str(ciphertext))

mac = HMAC.new(key, ciphertext)
print("MAC: " + mac.hexdigest())