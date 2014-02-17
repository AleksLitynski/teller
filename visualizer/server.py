from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket

#used by HTTPServer to field all queries.
class web_handler(BaseHTTPRequestHandler):

	def do_GET(self):
		#stupid (maybe effective) way to keep people from crawling all over my file system.
		if ".." in self.path : self.send_error(404, "error'd")

		#set the header.
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

		#send the index if they forgot to ask for something else.
		if self.path == "/" or self.path == "":
			self.path = "/index.html"

		#if they want data.json, send that.
		if self.path == "/data.json":
			global ontology_info
			print ontology_info
			self.wfile.write(ontology_info)
		else:
			try:
				#otherwise, send them whatever file they asked for.
				fh = open("static_files" + self.path, "r")
				file_read = fh.read()
				self.wfile.write(file_read)
				fh.close()
			except:
				self.send_error(404, "big whoopsie on somebodies part")





ontology_info = ""
def run():
	#tell python ontology_info is THE ontology_info.
	global ontology_info
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(("127.0.0.1", 5005))
	#ask for the json data. ANY message will do.
	s.send("give me the booty")
	data = s.recv(1024)
	s.close()
	print data
	#store the sta from python
	ontology_info = data


	#start the web server.
	web_server = HTTPServer(('', 8080), web_handler)
	web_server.serve_forever()








run()