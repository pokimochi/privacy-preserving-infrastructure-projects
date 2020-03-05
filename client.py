#
# Hello World client in Python
# Connects REQ socket to tcp://localhost:5555
# Sends "Hello" to server, expects "World" back
#

import zmq

def readFile(path):
  messages = []
  
  with open(path) as file:
    for line in file:
      messages.append(line)

  return messages

if __name__== "__main__":
  context = zmq.Context()
  filepath = "./messages.txt"

  # Read nessages text file
  messages = readFile(filepath)

  # Socket to talk to server
  print("Connecting to hello world server\n")
  socket = context.socket(zmq.REQ)
  socket.connect("tcp://localhost:5555")

  # Send each message to the server
  for message in messages:
    print("Sending message: " + message)
    socket.send(message)

    # Get the reply
    reply = socket.recv()
    print("Recieved reply: " + reply + "\n")