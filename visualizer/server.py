from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket


#Hey you cannot have global variable. unless you do,
#global nameOfVariableHere
#Python doesn't like global variables but if we must I think we can have global "variable" without having to declare global everytime.
#More I look into python I get an impression that it doesn't like object oriented style.
#It likes to show everything in a plain sight.

#Global variables I guess 
def isDebug(): return False

#helper functions for printing particular message
#Man... I wish we could have different colored messages so that way we can have better impression without having to actually read
def printAlert(say):
	print "   Alert :" + say
def printFunc(say):
	print "   FunctionCall : " + say

#I pulled out all the def from class. o_o
#my reasoning was well, python doesn't support || reinforce the notion of object oriented programming.
#Neither do we seem in need for encapsulating style approach since it is more of receive request then process it
#I found no need to have encapsulation to *solve* something. < maybe you find it more reasonable to have encapsulation
#if you do so then maybe feedback?
 
def receiveData():
	printFunc("RECEIVE DATA")
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.connect(("127.0.0.1", 5005))
	#s.send("give me the booty")
	#data = s.recv(1024)
	#s.close()
	return open("dataDummy.txt").read()

def sendJson(handler):
	printFunc("SendJson")
	handler.wfile.write(receiveData())

#send them whatever file they asked for.
def sendRequested(handler):
	printFunc("SendingRequested")
	try:
		fh = open("static_files" + handler.path, "r")
		file_read = fh.read()
		handler.wfile.write(file_read)
		fh.close()
	except:
		handler.send_error(404, "big whoopsie on somebodies part")
		
def ERROR_NO_INDEX(handler):
	printFunc("ERROR_NO_INDEX")
	handler.path = "/index.html"
	sendRequested(handler);
	
#used by HTTPServer to field all queries.	
class web_handler(BaseHTTPRequestHandler):
#I decided to just leave this one function here
#because it's neither liekly to be used globally nor related to actual logic of the script
	def printClisentInfo(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	
	def do_GET(self):
		if ".." in self.path : self.send_error(404, "error'd")
		if(isDebug()):self.printClisentInfo();
		print "RECEIVED REQUEST : " + self.path
		
		#I am mimicking c style here swtich case statement here
		#http://stackoverflow.com/questions/374239/why-doesnt-python-have-a-switch-statement
		#http://blog.simonwillison.net/post/57956755106/switch
		response = {
			'/' :	ERROR_NO_INDEX,
			'' :	ERROR_NO_INDEX,
			'/data.json': sendJson
		}
		try : response[self.path](self)
		except :
			printAlert("EXCEPTION RAISED");
			sendRequested(self)

#start the web server.
web_server = HTTPServer(('', 8080), web_handler)
web_server.serve_forever()