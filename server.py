# Binds REP socket to tcp://*:5555
import zmq
import time

if __name__== "__main__":
  context = zmq.Context()
  socket = context.socket(zmq.REP)
  socket.bind("tcp://*:5555")

  while True:
    # Wait for ciphertext
    message = socket.recv_json()
    print("Recieved message: %s" % message)

    # Verify Aggregate MAC
    # Decrypt Ciphertext if Calculated Aggregate MAC == Recieved Aggregate MAC
    time.sleep(0.5)

     #  Send reply back to client
    socket.send(b"Message recieved!")