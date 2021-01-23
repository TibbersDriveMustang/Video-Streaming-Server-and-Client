__author__ = 'Tibbers'
import sys, socket

from ServerWorker import ServerWorker

class Server:

	def main(self):
		try:
			SERVER_PORT = int(sys.argv[1])
		except:
			print ("[Usage: Server.py Server_port]\n")
		rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		rtspSocket.bind(('', SERVER_PORT))
		print ("RTSP Listing incoming request...")
		rtspSocket.listen(5)

		# Receive client info (address,port) through RTSP/TCP session
		while True:
			clientInfo = {}
			clientInfo['rtspSocket'] = rtspSocket.accept()   # this accept {SockID,tuple object},tuple object = {clinet_addr,intNum}!!!

			ServerWorker(clientInfo).run()


# Program Start Point
if __name__ == "__main__":
	(Server()).main()


