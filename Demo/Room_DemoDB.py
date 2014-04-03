#needed for user input
import sys
import random
import shlex
import socket
#importing our stuff
import json
from RefCode.Query_Explorer import *

#must have foobar
#can have arbitrary number of arguments and/or keyword arguments
#def func(foobar, *args, **kwargs)

#Nodes have: ID, type, value, & List of Edges
#

##Workflow

#Ask for Room
#Tell about Room -- comes back with relationships
#Keep list of all objects in the room
#Search input for one of those objects
#Query about objects
#Repeat

#This is how we contact the database
def query(query_string):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5005))
    #print (type(s))                 #What is the type of s... -- It's a socket!
    s.send(query_string)            #It doesn't seem to like this line...
    query_response = s.recv(10000) #our replies are VERY long. GOTTA fix that. At least, don't recurse into nodes that already exist
    s.close()
    #print("query_response: ")
    #print (query_response)
    return query_response


#Give node a name and a depth; 2 is default, but you could do 10 or something, if needed.
def describe_noun(noun_name, depth=2):
	#broke up the return into 2 lines to make it more readable
    return '{"type": "get", "params": {"depth":'+str(depth)+'}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1",' +\
           '"terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "'+noun_name+'"}}]}}]}}'


def get_node(node_id, depth=2):
    return '{"type": "get", ' \
           '"params": {"depth":'+str(depth)+'}, ' \
                                            '"search": {"id":"'+node_id+'"}}'


def translate_type(type):
    return type


def get_node_by_name(name):

    #exp = Query_Explorer()
    query_string = describe_noun(name, 2)

    noun = get_noun(json.loads(query(query_string)))
    noun = pipe(query_string, [
        query,
        json.loads,
        get_noun
    ])


    return noun

#This will contain all the dictionaries returned from our JSON code
encyclopedia = []

#List of room contents
roomConts = {"id" : 0, "rel_id" : 1, "value" : 2, "type" : 3, "edges" : 4}

#want to create a list of nodes.
nodes = {"info":[]}
edges = {"info":[]}

def addEdge(edge):
        edges["info"].append(edge)

def edgeInfo(edge_type, weight):
        edge = {}
        edge["type"] = edge_type
        edge["weight"] = weight
        addEdge(edge)

def addNode(node):
        nodes["info"].append(node)

def nodeInfo(node_id, node_type, value, edges):
        node = {}
        node["id"]= node_id
        node["type"]= node_type
        node["value"]= value
        node["edges"]= edges
        addNode(node)

        

#ideal length of method 5-15 
#http://programmers.stackexchange.com/questions/133404/what-is-the-ideal-length-of-a-method
def node(action):
	verb = ""; subject = ""
	for word in shlex.split(action):#divides the action by spaces
		if word in roomContents: subject = word; continue;
		if word in dialogsNode: verb = word; continue;
	if subject == "": return False
	if verb == "":
		print(inspectObject(subject))
	elif(verb in items[subject][attr["actions"]] ):
		print(dialogsNode[verb][0].replace("obj",subject))
	else : 
		print(dialogsNode[verb][1].replace("obj",subject))
	return True


dialogs = {             "sit"	: "You sit down cross-legged on the floor.",
			"dance"	: "You dance for a moment, though you are not sure why." 
						+ "\nIt is almost as if you are a puppet whose strings are being"
						+ "\npulled by the invisible hands of some unknown God..."
						+ "\nYou quickly dismiss that thought and return to a standing position.",
                        "lie" : "You lie down on the floor.",
                        "talk" : "You talk to yourself. Sadly, doing so provides you with no new information.",
                        "jump" : "You jump up and down. It's good for your buns and thighs."
}
def playerNode(action):
#Modification reasoning, function wraps a concept. hard coding if statemetns when it is
#likely subjected to expand(since we want to have more than two actions) is not a good practice. -- An excellent point.
	isActionValid = False
	for d in dialogs:
		if d in action:
			isActionValid = True
			print(dialogs[d])
	if(not isActionValid):print("SYSTEM : Action not recognized")
				
    		
def Check_Edge(node, searchFor, searchIn):
    for edge in node.get("edges"):
        if (edge.get(searchIn) == searchFor):
            #add to roomConts
            roomConts[edge.get("id")] = [edge.get("id"), edge.get("value"), edge.get("type"), edge.get("edges")]
            return edge
        else:
            tmp = Check_Terminal(edge, searchFor, searchIn)
            if tmp:
                return tmp

def Check_Terminal(edge, searchFor, searchIn):
    terminal = edge.get("terminal")
    if(terminal.get(searchIn) == searchFor):
        roomConts[terminal.get("id")] = [terminal.get("id"), terminal.get("value"), terminal.get("type"), terminal.get("edges")]
        return terminal
    else:
        tmp = Check_Edge(terminal, searchFor, searchIn)
        if tmp:
            return tmp



#Recursive Search -- look through all nodes until you find searchFor
#searchIn is the attribute to look for searchFor in.
def recSearch(queryResult, searchFor, searchIn):
    if queryResult.get("type") == "get-success":
        roomConts[queryResult.get("id")] = []
        
        for response_node in queryResult.get("reply"):

            #looks for evbery node in the edges of that node, and finds our target
            tmp = Check_Edge(response_node, searchFor, searchIn)
            if tmp:
                return tmp


def qrPrint(qrNode):
    #print("This is where more information would be... \nIF I HAD ANY!")
    pNode = qrNode.get("type")
    pNode += "; "
    pNode += qrNode.get("value")
    pNode += "; "
    pNode += qrNode.get("id")
    print(pNode)

    #nodeCheck = json.loads(query(get_node(qrNode.get("id"), 2)))
    #print(nodeCheck.get("type"))

def roomPrint():
    print("\nRoomContents: ")
    print(roomConts)

#Game Loop
def testLoop():
    while(True):
        #create some space between this and last input/output
        print("\n"),
        #input() does not work on my system, don't know why, so if it doesn't work, just try raw_input instead
        action = raw_input().lower()    #convert to lower case to prevent problems where there are none (i.e. "SIT on Chair" should work just like "sit on chair")

        #leave the game if the user wants to -- Moving it here prevents the game from yelling at the user when he/she exits ~Joe
        if action == "exit" or action == "quit":
                print("Okay, bye!")
                break 


        
        success = False
        for word in shlex.split(action):
            #User's query is the action
            queryResult = json.loads(query(describe_noun(word, 2)))

            
            #check for action in value, type, id, terminal
            node = recSearch(queryResult, word, "value")
            if not node:
                node = recSearch(queryResult, word, "type")
            if not node:
                node = recSearch(queryResult, word, "id")
            if not node:
                node = recSearch(queryResult, word, "terminal")
            if node:
                success = True
                print(roomConts[node.get("id")])
                
        if success:
            pass
        #do stuff with objects
        elif not playerNode(action):
            #Only access player node if you don't refer to any of the objects
            #node(action)
            pass


#create a version of recSearch that is designed to list things
def listSearch(queryResult, searchFor, searchIn):
    ls = []

    if queryResult.get("type") == "get-success":
        roomConts[queryResult.get("id")] = []
        
        for response_node in queryResult.get("reply"):

            #looks for evbery node in the edges of that node, and finds our target
            #IMPORTANT!!! -- Need to make new versions of Check_Edge and Check_Terminal that return lists
            tmp = Check_Edge(response_node, searchFor, searchIn)
            if tmp:
                print (tmp)
                ls+=[tmp]
        return ls

#Working on a function to list room contents at game start
def listRoomConts():
    node = listSearch(queryResult, "noun", "type")
    #print ("1")
    for n in node:
        print (n.get("id"))
    #pass
    


#GAME START
#This code runs as soon as the game starts...	
#Run the game!

print("Creating Room...")
#create room
edgeInfo("contains", 1)
nodeInfo(0, "noun", "A Room", "contains")

print("You are in a room.")

queryResult = json.loads(query(describe_noun("room", 2)))   #the 2 indicates we go down to a depth of 2

#this is the room
rm = get_node_by_name("room")

#We have a set of functions that do the obnoxious node traversal!
qrNode = recSearch(queryResult, "room", "value")

#test to see if we are getting things in roomConts, as we are supposed to
roomPrint()

#rmcts = room contents
print("\nInside the room, you can see...\n")
#rmcts = recSearch(queryResult, "noun", "type")
#print(rmcts)

listRoomConts()

#wait for user input
testLoop()

#GAME END


