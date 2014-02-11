from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket

class web_handler(BaseHTTPRequestHandler):

	def do_GET(self):

		if ".." in self.path : self.send_error(404, "error'd")
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		if self.path == "/" or self.path == "":
			self.path = "/index.html"

		if self.path == "/data.json":
			global ontology_info
			print ontology_info
			self.wfile.write(ontology_info)
		else:
			try:
				fh = open("static_files" + self.path, "r")
				file_read = fh.read()
				self.wfile.write(file_read)
				fh.close()
			except:
				self.send_error(404, "big whoopsie on somebodies part")





ontology_info = ""
def run():
	global ontology_info
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 5005))
	s.send("give me the booty")
	data = s.recv(1024)
	s.close()
	print data
	ontology_info = data



	web_server = HTTPServer(('', 8080), web_handler)
	web_server.serve_forever()








run()