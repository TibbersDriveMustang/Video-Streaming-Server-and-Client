{\rtf1\ansi\ansicpg1252\cocoartf1348\cocoasubrtf170
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural

\f0\fs24 \cf0 First\
	Start the server with the command line\
	\
		python Server.py server_port\
	\
	Where server_port is the port your server listens to for incoming RTSP connections\
		# Standard RTSP port is 554 \
		# But need to choose a #port > 1024\
	\
Then \
	Start the client with the command line\
		\
		python ClientLauncher.py server_host server_port RTP_port video_file\
\
	Where \
		# server_host : the name of the machine where server is running\
		# server_port : port the server is listening on\
		# RTP_port : port where the RTP packets are received\
		# video_file : name of video file you want to request\
	\
		@ file format\
			Lab`s proprietary MJPEG(Motion JPEG) format\
				# The server streams a video which has been encoded into a proprietary MJPEG file format\
				# This format stores the video as concatenated JPEG-encoded images\
				# Each image being preceded by a 5-Byte header which indicates the bit size of the image\
				# Server parses the bitstream of MJPEG file to extract the JPEG images\
				# Server sends the images to client at periodic intervals\
				# Client then displays the individual JPEG images sent from server			}