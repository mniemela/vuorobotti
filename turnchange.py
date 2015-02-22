import socket
import sys
import settings

def main():
    if len(sys.argv) != 2:
        print "Virheelliset argumentit!"
    else:
        socketti = socket.socket()
		
        socketti.connect(('localhost', 6666))
        socketti.send(sys.argv[1]) 
        socketti.close()

    
if __name__ == '__main__': main()
