import socket
import sys


if len(sys.argv) != 2:
    print "Virheelliset argumentit!"
else:
    socketti = socket.socket()
    socketti.connect(('localhost', 666))
    socketti.send(sys.argv[1])
    socketti.close()
