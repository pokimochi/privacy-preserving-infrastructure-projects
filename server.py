# Binds REP socket to tcp://*:5555
import zmq
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA
from Crypto.Util import Counter
from Crypto import Random

if __name__== "__main__":
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")

  # Shared key and IV
  key = b'Sixteen byte key' # This is actually 16 bytes
  nonce = b'1111111111111111'
  nonce = int.from_bytes(nonce, byteorder='big')
  counter = 1
  prevAggregateMAC = b''

  while True:
    file1 = open("Result.txt", "a")
    # Wait for ciphertext
    print('Waiting for message...')
    data = socket.recv_json()
    print('Message recieved...')
    ciphertext = data["message"].encode('ISO-8859-1')
    receivedMac = data["auth"].encode('ISO-8859-1')

    # Verify Aggregate MAC
    print('Verifying message...')
    mac = HMAC.new(key, ciphertext).digest()
    aggregateMac = SHA.new(prevAggregateMAC + mac).digest()

    # Decrypt Ciphertext if Calculated Aggregate MAC == Recieved Aggregate MAC
    if(aggregateMac == receivedMac):
      print('Message is valid...')

      # Create new counter block
      ctrBlock = Counter.new(128, initial_value=nonce ^ counter) # 16 bytes = 128 bits; XOR nonce with counter

      plaintext = AES.new(key, AES.MODE_CTR, counter=ctrBlock).decrypt(ciphertext)
      del prevAggregateMAC
      prevAggregateMAC = aggregateMac
      counter += 1

      # Hash old key using SHA1
      newKey = SHA.new(key).hexdigest()

      # Truncate extra 16 bytes
      newKey = list(bytearray(newKey.encode()))
      del newKey[16:]

      # Set new key as the current key
      key = bytes(newKey)

      # Cleanup 
      del mac
      del newKey

      #print('Message recieved: %s' % plaintext)
      print('Message recieved: ' + str(plaintext, 'utf-8'))
      file1.write(str(plaintext, 'utf-8'))
    else:
      print('Message is invalid...')

    print('\n')
    file1.close()
    #  Send reply back to client
    socket.send(b"Message recieved!")
