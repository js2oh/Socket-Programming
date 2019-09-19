
#!/usr/bin/python

from socket import *
import sys, string

# sendRandPortTCP(rcode):
# This function receives the request for the random available port for the UDP from the client through tcp connection,
# and it sends the available port number back to the client if the client's request code matches the server's code.
# It also prints the negotiation port to make sure tcp connection can be made correctly.
# Then, it returns the upd socket created and bound to the port sent.
def sendRandPortTCP(rCode):
	serverSocketTCP = socket(AF_INET,SOCK_STREAM)
	serverSocketTCP.bind(('', 0))
	serverSocketTCP.listen(1)
	print "SERVER_PORT=" + (str)(serverSocketTCP.getsockname()[1])
	inProc = 1
	while inProc:
		connectionSocket, addr = serverSocketTCP.accept()
		rCodeClient = connectionSocket.recv(1024)
		if rCodeClient == rCode:
			serverSocketUDP = socket(AF_INET,SOCK_DGRAM)
			serverSocketUDP.bind(('', 0))
			connectionSocket.send((str)(serverSocketUDP.getsockname()[1]))
			inProc = 0
		else:
			print "Error: Invalid request code was received. Unable to send the port."
		
		connectionSocket.close()
	
	return serverSocketUDP

# reverseMessageUDP(ssUDP):
# This function receives the the string delivered from the client via the udp sockets, reverse the string, and return it back to the client.
def reverseMessageUDP(ssUDP):
	message, clientAddress = ssUDP.recvfrom(1024)
	reversedMessage = message[::-1]
	ssUDP.sendto(reversedMessage, clientAddress)
	ssUDP.close()
	return

# signalingServer():
# This is the main signaling function for server to execute and checks if it took the request code through command line arugment or not.
def signalingServer():
	if len(sys.argv) == 2:
		reqCode = sys.argv[1]
		serverSocketUDP = sendRandPortTCP(reqCode)
		reverseMessageUDP(serverSocketUDP)
	else:
		print "Error: Incorrect number of command line arguments."
		sys.exit(1)

	return

signalingServer()