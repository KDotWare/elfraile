#!/usr/bin/python3
#############################
#       Code by Mec505      #
#############################	
import socket
import threading
import sys
import mimetypes
sys.path.insert(0, "../config/")
import website

class webserver:
	def __init__(self, host="", port=80):
		self.web_socket()
		self.web_bind(host, port)
		self.web_listen(50)
		while True:
			conn, addr = self.web_accept()
			self.web_thread(conn, addr)

	def web_socket(self):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		except socket.error as error:
			print("ERROR"+ str(error))

	#start binding to the target port that user give
	def web_bind(self, host, port):
		try:
			self.s.bind((host, port))
			print("bind at port {}".format(port))

		except socket.error as error:
			print("ERROR:"+ str(error) +"Retrying...")
			self.web_bind()
		
	def web_listen(self, queue):
		self.s.listen(queue)

	def web_accept(self, timeout=5):
		conn, addr = self.s.accept()
		if timeout > 0:
			conn.settimeout(timeout)
			return conn, addr

		else:
			return conn, addr
		f.close()

	def web_thread(self, conn, addr):
		thread = threading.Thread(target=self.web_clients, args=(conn, addr))
		thread.start()
		self.active = str(threading.active_count() - 1)

	def web_clients(self, conn, addr):
		self.conn = conn
		self.addr = addr

		while True:
			try:
				data = self.conn.recv(65535).decode("utf-8")
				header2 = self.web_process(data)
				self.conn.send(header2.encode())
			except socket.timeout:
				self.conn.close()
				break

	def web_process(self, data):
		request = []
		headers = []
		data = data.splitlines()
		for i in data:
			request = data[0].split()

		for i in range(1, len(data)):
			headers.append(data[i])
		
		if request[0] == "GET":
			print("active(s): "+ self.active + " || {0} || {1} {2}".format(self.addr[0], request[0], request[1]))
			header1 = self.web_get(request[1])
			return header1

		elif request[0] == "POST":
			pass

	def web_get(self, path):
		header = website.get(path)
		return header

if __name__ == "__main__":
	try:
		webserver()
	except KeyboardInterrupt as msg:
		print(" !!Shutting down the server...")



