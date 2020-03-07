# Connects REQ socket to tcp://localhost:5555
import zmq
from Crypto.Cipher import AES
from Crypto.Hash import HMAC
from Crypto.Hash import SHA
from Crypto.Util import Counter
from Crypto import Random

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

  # TODO ask for input instead of key and IV being hardcoded
  key = b'Sixteen byte key' # This is actually 16 bytes
  nonce = b'1111111111111111'
  nonce = int.from_bytes(nonce, byteorder='big')
  counter = 1
  prevAggregateMAC = b''

  # Initialize socket to talk to the server
  context = zmq.Context()
  print("Connecting to server\n")
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://localhost:5555")

  # Send each message to the server
  for message in messages:
    print("Sending message: " + message)

    # Create new counter block
    ctrBlock = Counter.new(128, initial_value=nonce ^ counter) # 16 bytes = 128 bits; XOR nonce with counter

    # Create new block cipher
    ciphertext = AES.new(key, AES.MODE_CTR, counter=ctrBlock).encrypt(message)

    # Generate MAC
    mac = HMAC.new(key, ciphertext).digest()

    # Create Aggregate MAC
    aggregateMac = SHA.new(prevAggregateMAC + mac).digest()

    counter += 1
    del prevAggregateMAC
    prevAggregateMAC = aggregateMac

    # Hash old key using SHA1
    newKey = SHA.new(key).hexdigest()

    # Truncate extra 16 bytes
    newKey = list(bytearray(newKey.encode()))
    del newKey[16:]

    # Set new key as the current key
    del key
    key = bytes(newKey)

    # Send json to server
    socket.send_json({"message": ciphertext.decode('ISO-8859-1'), "auth": aggregateMac.decode('ISO-8859-1')})

    # Cleanup 
    del mac
    del newKey

    # Make sure message was recieved before sending next message
    print('Waiting for response...')
    response = socket.recv().decode()
    print("Received response: " + response + '\n')