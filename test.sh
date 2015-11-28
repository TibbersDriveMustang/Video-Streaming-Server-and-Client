#!/bin/sh
python Server.py 1025
python ClientLauncher.py 127.0.0.1 1025 5008 video.mjpeg
