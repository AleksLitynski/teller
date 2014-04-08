from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import socket
import json
import SearchInterpreter
#,miserver
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
	print ("   Alert :" + say)
	
def printFunc(say):
	print ("   FunctionCall : " + say)

#I pulled out all the def from class. o_o
#my reasoning was well, python doesn't support || reinforce the notion of object oriented programming.
#Neither do we seem in need for encapsulating style approach since it is more of receive request then process it
#I found no need to have encapsulation to *solve* something. < maybe you find it more reasonable to have encapsulation
#if you do so then maybe feedback?
 
def receiveData():
	#printFunc("RECEIVE DATA")
	#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.connect(("127.0.0.1", 5005))
	#s.send("give me the booty")
	#data = s.recv(1024)
	#s.close()
	return open("dataDummy.txt").read()

def sendJson(handler):
	printFunc("SendJson")
	handler.wfile.write(receiveData())
def sendDummy00(handler):
	handler.wfile.write(open("dataDummy00.txt").read())
def sendDummy01(handler):
	handler.wfile.write(open("dataDummy01.txt").read())
	
def describe_noun(noun_name, depth=2):	
	printFunc("describe_noun, searching for : " + noun_name)
	#broke up the return into 2 lines to make it more readable
	return '{"type": "get", "params": {"depth":'+str(depth)+'}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1",' +    '"terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "'+noun_name+'"}}]}}]}}'

def doSearch(handler):
	printFunc("doSearch")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 5005))
	s.send(describe_noun("room"))
	s.send('{"type":"get", "params":{"depth":2}, "search":{}}')
	raw = s.recv(10000000)
	read = SearchInterpreter.read(raw);
	s.close()
	handler.wfile.write(json.dumps(read))
	return read

def sendSearch(handler,info):
	printFunc("SendSearch")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect(('127.0.0.1', 5005))
	s.send(info)
	raw = s.recv(200000)
	read = SearchInterpreter.read(raw);
	s.close()
	handler.wfile.write(json.dumps(read))
	return read
	
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
def searchByKeyword(data) : return describe_noun(data[1]);
	
def POSTsearch(handler,data):
	printFunc("POSTsearch");
	searchType = {
			'keyword' : searchByKeyword
		}
	try :
		print("POST SEARCH RECEIVED ",data);
		sendSearch(handler,describe_noun(data[1]) );
	except : print "SearchPatternNotFound"

#used by HTTPServer to field all queries.	
class web_handler(BaseHTTPRequestHandler):
#I decided to just leave this one function here
#because it's neither liekly to be used globally nor related to actual logic of the script
	def printClisentInfo(s):
		s.send_response(200)
		s.send_header('Content-type', 'text/html')
		s.end_headers()
	
		
	
	def do_POST(s):
		printFunc("do_POST");
		length = int(s.headers['Content-Length'])
		data = json.loads(s.rfile.read(length));
		print ("Received : " + s.path,data);
		response = {
			'/search' :POSTsearch
		}
		try : response[s.path](s,data)
		except :
			printAlert("do_POST EXCEPTION RAISED");
			sendRequested(s)
		
	def do_GET(self):
		if ".." in self.path : self.send_error(404, "error'd")
		if(isDebug()):self.printClisentInfo();
		print ("RECEIVED REQUEST : " + self.path)
		
		#I am mimicking c style here swtich case statement here
		#http://stackoverflow.com/questions/374239/why-doesnt-python-have-a-switch-statement
		#http://blog.simonwillison.net/post/57956755106/switch
		
		response = {
			'/' :	ERROR_NO_INDEX,
			'' :	ERROR_NO_INDEX,
			'/data.json': sendJson,
			'/dataDummy00' : sendDummy00,
			'/dataDummy01' : sendDummy01,
			'/search' : doSearch
		}
			
		try : response[self.path](self)
		except :
			printAlert("EXCEPTION RAISED");
			sendRequested(self)

#start the web server.

	
web_server = HTTPServer(('', 8080), web_handler)
web_server.serve_forever()