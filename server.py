#!/bin/env python3

import socket

import parser

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
			parser.parse_int_report(data)
		except Exception as e:
			print("Received invalid packet: {}".format(e))

except KeyboardInterrupt:
	print("Interrupt")

finally:
	sock.close()
