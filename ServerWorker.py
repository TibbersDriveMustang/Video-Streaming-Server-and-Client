__author__ = 'Tibbers'

import random, math
import time
from random import randint
import sys, traceback, threading, socket

from VideoStream import VideoStream
from RtpPacket import RtpPacket

class ServerWorker:
	SETUP = 'SETUP'
	PLAY = 'PLAY'
	PAUSE = 'PAUSE'
	TEARDOWN = 'TEARDOWN'

	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT

	OK_200 = 0
	FILE_NOT_FOUND_404 = 1
	CON_ERR_500 = 2

	clientInfo = {}

	def __init__(self, clientInfo):
		self.clientInfo = clientInfo

	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()

	def recvRtspRequest(self):
		"""Receive RTSP request from the client."""
		connSocket = self.clientInfo['rtspSocket'][0]
		while True:
			data = connSocket.recv(256)  ###
			if data:
				print '-'*60 + "\nData received:\n" + '-'*60
				self.processRtspRequest(data)

	def processRtspRequest(self, data):
		"""Process RTSP request sent from the client."""
		# Get the request type
		request = data.split('\n')
		line1 = request[0].split(' ')
		requestType = line1[0]
		# Get the media file name
		filename = line1[1]
		# Get the RTSP sequence number
		seq = request[1].split(' ')

		# Process SETUP request
		if requestType == self.SETUP:
			if self.state == self.INIT:
				# Update state
				print "SETUP Request received\n"

				try:

					self.clientInfo['videoStream'] = VideoStream(filename)
					self.state = self.READY

				except IOError:
					self.replyRtsp(self.FILE_NOT_FOUND_404, seq[1])

				# Generate a randomized RTSP session ID
				self.clientInfo['session'] = randint(100000, 999999)

				# Send RTSP reply
				self.replyRtsp(self.OK_200, seq[0])  #seq[0] the sequenceNum received from Client.py
				print "sequenceNum is " + seq[0]
				# Get the RTP/UDP port from the last line
				self.clientInfo['rtpPort'] = request[2].split(' ')[3]
				print '-'*60 + "\nrtpPort is :" + self.clientInfo['rtpPort'] + "\n" + '-'*60
				print "filename is " + filename

		# Process PLAY request
		elif requestType == self.PLAY:
			if self.state == self.READY:
				print '-'*60 + "\nPLAY Request Received\n" + '-'*60
				self.state = self.PLAYING

				# Create a new socket for RTP/UDP
				self.clientInfo["rtpSocket"] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

				self.replyRtsp(self.OK_200, seq[0])
				print '-'*60 + "\nSequence Number ("+ seq[0] + ")\nReplied to client\n" + '-'*60

				# Create a new thread and start sending RTP packets
				self.clientInfo['event'] = threading.Event()
				self.clientInfo['worker']= threading.Thread(target=self.sendRtp)
				self.clientInfo['worker'].start()
		# Process RESUME request
			elif self.state == self.PAUSE:
				print '-'*60 + "\nRESUME Request Received\n" + '-'*60
				self.state = self.PLAYING

		# Process PAUSE request
		elif requestType == self.PAUSE:
			if self.state == self.PLAYING:
				print '-'*60 + "\nPAUSE Request Received\n" + '-'*60
				self.state = self.READY

				self.clientInfo['event'].set()

				self.replyRtsp(self.OK_200, seq[0])

		# Process TEARDOWN request
		elif requestType == self.TEARDOWN:
			print '-'*60 + "\nTEARDOWN Request Received\n" + '-'*60

			self.clientInfo['event'].set()

			self.replyRtsp(self.OK_200, seq[0])

			# Close the RTP socket
			self.clientInfo['rtpSocket'].close()

	def sendRtp(self):
		"""Send RTP packets over UDP."""

		counter = 0
		threshold = 10
		while True:
			jit = math.floor(random.uniform(-13,5.99))
			jit = jit / 1000

			self.clientInfo['event'].wait(0.05 + jit)
			jit = jit + 0.020

			# Stop sending if request is PAUSE or TEARDOWN
			if self.clientInfo['event'].isSet():
				break

			data = self.clientInfo['videoStream'].nextFrame()
			#print '-'*60 + "\ndata from nextFrame():\n" + data + "\n"
			if data:
				frameNumber = self.clientInfo['videoStream'].frameNbr()
				try:
					#address = 127.0.0.1 #self.clientInfo['rtspSocket'][0][0]
					#port = '25000' #int(self.clientInfo['rtpPort'])

					#print '-'*60 + "\nmakeRtp:\n" + self.makeRtp(data,frameNumber)
					#print '-'*60

					#address = self.clientInfo['rtspSocket'][1]   #!!!! this is a tuple object ("address" , "")

					port = int(self.clientInfo['rtpPort'])

					prb = math.floor(random.uniform(1,100))
					if prb > 5.0:
						self.clientInfo['rtpSocket'].sendto(self.makeRtp(data, frameNumber),(self.clientInfo['rtspSocket'][1][0],port))
						counter += 1
						time.sleep(jit)
				except:
					print "Connection Error"
					print '-'*60
					traceback.print_exc(file=sys.stdout)
					print '-'*60

	def makeRtp(self, payload, frameNbr):
		"""RTP-packetize the video data."""
		version = 2
		padding = 0
		extension = 0
		cc = 0
		marker = 0
		pt = 26 # MJPEG type
		seqnum = frameNbr
		ssrc = 0

		rtpPacket = RtpPacket()

		rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)

		return rtpPacket.getPacket()

	def replyRtsp(self, code, seq):
		"""Send RTSP reply to the client."""
		if code == self.OK_200:
			#print "200 OK"
			reply = 'RTSP/1.0 200 OK\nCSeq: ' + seq + '\nSession: ' + str(self.clientInfo['session'])
			connSocket = self.clientInfo['rtspSocket'][0]
			connSocket.send(reply)

		# Error messages
		elif code == self.FILE_NOT_FOUND_404:
			print "404 NOT FOUND"
		elif code == self.CON_ERR_500:
			print "500 CONNECTION ERROR"
