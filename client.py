#!/usr/bin/python

from socket import *
import sys, string

# reqRandPortTCP(sAddress, nPort, rCode):
# This function creates tcp socket and initiatese tcp connection through given server address and negotiation port.
# When tcp connection is successfully made, it sends a request code to the listening server and receives back the port that will be used for actual request.
# It then returns the port number in integer.
# If socket exception occurs while initiating tcp connection (e.g. negotiation port is unavailable/invalid), exits the client file.
# Also, if the request code sent does not match with the server's request code, closes tcp connection and exits the client file. 
def reqRandPortTCP(sAddress, nPort, rCode):
	try:
		clientSocketTCP = socket(AF_INET, SOCK_STREAM)
		clientSocketTCP.connect((sAddress, int(nPort)))
	except error:
		print "Error: Failed to connect. Invalid server address or invalid negotiation port number."
		sys.exit(1)
	else:
		clientSocketTCP.send(rCode)
		rPort = clientSocketTCP.recv(1024)
		if rPort == '':
			print "Error: Invalid request code was sent."
			sys.exit(1)

		clientSocketTCP.close()
		return int(rPort)

# sendMessageUDP(sAddress, rPort, msg):
# This function creates udp socket and sends the string message with the given server address and port to the server.
# It then receives the reversed message back from the server through the udp socket and returns it.
def sendMessageUDP(sAddress, rPort, msg):
	clientSocketUDP = socket(AF_INET, SOCK_DGRAM)
	clientSocketUDP.sendto(msg, (sAddress, rPort))
	rMsg, serverAddress = clientSocketUDP.recvfrom(1024)
	clientSocketUDP.close()
	return rMsg

# signalingClient():
# This is the main signaling function for client to execute and checks if the correct number of command line arguments are received.
# It also prints the reversed message returned from the server.
def signalingClient():
	if len(sys.argv) == 5:
		serverAddress = sys.argv[1]
		negoPort = sys.argv[2]
		reqCode = sys.argv[3]
		message = sys.argv[4]
		randPort = reqRandPortTCP(serverAddress, negoPort, reqCode)
		reversedMessage = sendMessageUDP(serverAddress, randPort, message)
		print "The message received from the server: " + reversedMessage
	else:
		print "Error: Incorrect number of command line arguments."
		sys.exit(1)

	return

signalingClient()