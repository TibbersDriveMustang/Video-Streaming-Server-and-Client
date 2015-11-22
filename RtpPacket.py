__author__ = 'Tibbers'
import sys
from time import time
# from VideoStream import VideoStream


import VideoStream
HEADER_SIZE = 12

class RtpPacket:
	header = bytearray(HEADER_SIZE)

	def __init__(self):
		pass

	def encode(self, version, padding, extension, cc, seqnum, marker, pt, ssrc, payload):
		"""Encode the RTP packet with header fields and payload."""

		timestamp = int(time())
		header = bytearray(HEADER_SIZE)
		#--------------
		# TO COMPLETE
		#--------------
		# Fill the header bytearray with RTP header fields
		#VideoS = VideoStream.VideoStream()

		#RTP-version filed(V), must set to 2
		#padding(P),extension(X),number of contributing sources(CC) and marker(M) fields all set to zero in this lab

		#Because we have no other contributing sources(field CC == 0),the CSRC-field does not exist
		#Thus the length of the packet header is therefore 12 bytes


			#Above all done in ServerWorker.py

		# ...
		#header[] =
		header[0] = version + padding + extension + cc + seqnum + marker + pt + ssrc
		print "bytearray: " + header + "hehe"



		# Get the payload from the argument
		# self.payload = ...
		#self.payload =
	def decode(self, byteStream):
		"""Decode the RTP packet."""
		self.header = bytearray(byteStream[:HEADER_SIZE])
		self.payload = byteStream[HEADER_SIZE:]

	def version(self):
		"""Return RTP version."""
		return int(self.header[0] >> 6)

	def seqNum(self):
		"""Return sequence (frame) number."""
		seqNum = self.header[2] << 8 | self.header[3]
		return int(seqNum)

	def timestamp(self):
		"""Return timestamp."""
		timestamp = self.header[4] << 24 | self.header[5] << 16 | self.header[6] << 8 | self.header[7]
		return int(timestamp)

	def payloadType(self):
		"""Return payload type."""
		pt = self.header[1] & 127
		return int(pt)

	def getPayload(self):
		"""Return payload."""
		return self.payload

	def getPacket(self):
		"""Return RTP packet."""
		return self.header + self.payload