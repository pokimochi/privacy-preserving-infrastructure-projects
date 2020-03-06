# Binds REP socket to tcp://*:5555
import zmq
import time

if __name__== "__main__":
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")

  while True:
    #  Wait for next request from client
    message = socket.recv()
    print("Received message: %s" % message)

    time.sleep(1)

    #  Send reply back to client
    socket.send(b"Message successfully recieved")