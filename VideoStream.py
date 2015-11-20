__author__ = 'Tibbers'
class VideoStream:
	def __init__(self, filename):
		self.filename = filename
		try:
			self.file = open(filename, 'rb')
			print filename + " read in VideoStream.py"
		except:
			print "read " + filename + " error"
			raise IOError
		self.frameNum = 0

	def nextFrame(self):
		"""Get next frame."""
		data = self.file.read(5) # Get the framelength from the first 5 bits
		print "framelength is " + data
		if data:

			framelength = 15 #int(data,16)
			# Read the current frame
			data = self.file.read(framelength)
			self.frameNum += 1
		return data

	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum

