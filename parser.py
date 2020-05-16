#!/bin/env python3

import struct

def get_header_data(data, offset, size):
	if (offset + size > len(data)):
		raise Exception('Too short packet')
	return data[offset:offset+size]

def split_int_report(data):
	# data format in report is as follow:
	# IP (20 B), options ignored
	# TCP (20 B)/ UDP (8 B), options ignored
	# INT Shim (4 B)
	# INT (8 B)
	# INT metadata

	offset = 0

	# IP
	header_size = 20
	ip_header = get_header_data(data, offset, header_size)
	offset += header_size

	next_protocol = struct.unpack('!B', get_header_data(ip_header, 9, 1))[0]
	
	# TCP/UDP
	transport_header = b''
	if next_protocol == 6:
		# TCP
		header_size = 20
		transport_header = get_header_data(data, offset, header_size)
		offset += header_size
	elif next_protocol == 17:
		# UDP
		header_size = 8
		transport_header = get_header_data(data, offset, header_size)
		offset += header_size
	else:
		raise Exception('Unknown transport layer protocol')

	# INT shim
	header_size = 4
	int_shim_header = get_header_data(data, offset, header_size)
	offset += header_size

	# INT
	header_size = 8
	int_header = get_header_data(data, offset, header_size)
	offset += header_size

	# Metadata
	header_size = 4 * (get_header_data(int_shim_header, 3, 1)[0] - 3)
	if header_size < 0:
		raise Exception('Invalid INT length')
	int_metadata = get_header_data(data, offset, header_size)

	return int_shim_header, int_header, int_metadata, ip_header, transport_header

def parse_int_report(data):
	int_shim_header, int_header, int_metadata, ip_header, transport_header = split_int_report(data)
