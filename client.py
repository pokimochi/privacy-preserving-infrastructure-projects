# Connects REQ socket to tcp://localhost:5555
import zmq
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA
from Crypto.Util import Counter
from Crypto import Random
import sys

# Reads a file per line
def readFile(path):
  lineArr = []
  
  with open(path) as file:
    for line in file:
      lineArr.append(line)

  return lineArr

# MAIN FUNCTION
if __name__== "__main__":
  # Read messages text file
  filepath = "./messages.txt"
  messages = readFile(filepath)

  # TODO ask for input instead of hardcoded
  key = b'Sixteen byte key' # This is actually 16 bytes
  nonce = Random.new().read(AES.block_size) # 16 byte IV
  nonce = int.from_bytes(nonce, byteorder=sys.byteorder)
  counter = 1
  initialEncMsg = ''

  # Initialize socket to talk to the server
  context = zmq.Context()
  print("Connecting to server\n")
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://localhost:5555")

  # Send each message to the server
  for message in messages:
    print("Sending message: " + message)

    encryptedMsg = ''

    # Create new counter block
    ctrBlock = Counter.new(128, initial_value=nonce ^ counter) # 16 bytes = 128 bits; XOR nonce with counter

    # Create new block cipher
    cipher = AES.new(key, AES.MODE_CTR, counter=ctrBlock)
    ciphertext = cipher.encrypt(message)

    if(counter == 1):
      encryptedMsg = HMAC.new(key, ciphertext).digest()
      initialEncMsg = encryptedMsg
    else:
      encryptedMsg = HMAC.new(key, initialEncMsg + ciphertext).digest()

    counter += 1

    # Hash old key using SHA1
    newKey = SHA.new(key).hexdigest()

    # Truncate extra 16 bytes
    newKey = list(bytearray(newKey.encode()))
    del newKey[16:]

    # Set current key as the new key
    key = bytes(newKey)

    # Send the message
    socket.send(encryptedMsg)
    
    #  Get the reply from server
    response = socket.recv().decode()
    print("Received reply: " + response)