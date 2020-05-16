#!/bin/env python3

import socket

UDP_port = 9500
UDP_IP = '0.0.0.0'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_port))

try:
	while True:
		data, addr = sock.recvfrom(1500)
		print('received {} bytes from {}'.format(len(data), addr))
		print("recv: ", data)
		
		try:
			# decode packet and send to DB
			pass
		except:
			pass

except KeyboardInterrupt:
	print("")

finally:
	sock.close()
