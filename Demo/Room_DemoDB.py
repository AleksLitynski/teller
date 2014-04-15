#needed for user input
import sys
import random
import shlex
import socket
import re
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

class noun:

    def __init__(self, id):
        self.id = id
        self.relationships = []

    def get_value(self, relationship_type, default="Something"):
        value = default
        for noun_relationship in self.relationships:
            if noun_relationship.type == relationship_type:
                value = noun_relationship.value
        return value
    
    def get_all(self, relationship_type):
        relationships = []
        for noun_relationship in self.relationships:
            if noun_relationship.type == relationship_type:
                relationships.append(noun_relationship)
        return relationships

    def get_relationship_types(self):
        relationship_types = set()
        for relationships in self.relationships:
            relationship_types.add(relationships.type)
        return relationship_types

    def print_noun(self):
        #Testing self.get_value() -- it works
        #print(self.get_value("named"))
        return self.get_value("named")

    def get_relationship(query):
        type = get_edge_named(query.get("edges"), "has_type").get("value")

        value = get_edge_named(query.get("edges"), "has_value").get("value")

        target = get_edge_named(query.get("edges"), "regarding").get("id")

        return relationship(type, value, target)
		
class relationship:
    def __init__(self, type, value, reguarding):
        self.type = type
        self.value = value
        self.reguarding = reguarding


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
    txt = '{"type": "get", "params": {"depth":'+str(depth)+'}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1",' +\
           '"terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "'+noun_name+'"}}]}}]}}'
    return txt
    

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

def show_locally(self):
		for n in self.graph.nodes_iter():
			print(n.id + " " + n.type + " " + n.value)

		for e in self.graph.edges_iter():
			print(str(e[0].id) + " -" + str(get_edge_val(e, self.graph).weights) + "-> " + str(e[1].id))

def new_noun_named(self, name, lang):
		new_node = self.add_node("noun", "")
		self.add_relationship(new_node, lang, "named", name)
		return new_node

def new_nouns_named(self, names, lang):
		nouns = []
		for noun in map( lambda x: self.new_noun_named(x, lang) , names):
			nouns.append(noun)
		return nouns

def fork(self, fork_from, name, time):
		new_noun = self.add_node(fork_from.type, name)
		self.add_edge("is_a", new_noun, fork_from, time, 100)
		return new_noun

#These are our lists of stuff
colors = ["burgundy", "violet", "goldenrod", "fuchsia", "lavender", "beige", "azure", "chartreuse", "celadon", "sage", "paisley", "plaid", "tartan", "scarlet"]
materials = ["plastic", "wood", "aluminum", "duct tape"]
bed_sizes = ["twin", "double", "queen-sized", "king-sized"]
book_titles = ["Dreams of Potatoes", "Tequila Sunrise", "The Kraken", "40 Cakes", "Spectral Robot Task Force",
             "The Vengeful Penguin", "Ninja's Guide to Ornamental Horticulture", "Neko-nomicon", "This is Not a Book"]
power_state = ["on", "off"]
liquids = ["water", "juice", "wine", "soda", "nothing"]

#Room will hold saved values -- [room_number][object_in_room][attribute_type][attribute_value]
room_dict = {}

#print objects, whose values we have already found/made -- It works!
def inspectOldObject(obj):
    s = "a"

    if "colored" in obj:
        s += " " + obj["colored"]

    if "is_made_of" in obj:
        s += " " + obj["is_made_of"]

    if "size" in obj:
        s += " " + obj["size"]

    s += " " + obj["named"] + ". "

    if "titled" in obj:
        s+= "The title reads: " + obj["titled"] + ". "

    if "power_state" in obj:
        s+= "It is " + obj["power_state"] + ". "
    
    return s

def inspectObject(node, depth=0):
    #Although I don't typically like making decisions that unilaterally effect a project...no one is here
    #So, I'm going to try to make this work, regardless of whether or not it technically fully utilizes our database

    #this is an old object
    is_old = False
    
    for obj in room_dict:
        #run inspectOldObject if we've already assigned values to it --this isn't being hit
        if node.get_value("named") in obj:
            is_old = True

    if is_old == True:
        return inspectOldObject(room_dict[node.get_value("named")])
        
    #otherwise, we will put the object and its attributes into our dictionary
        #This allows us to assume that the code below is always being used for new objects, rather than old ones
    else:
        #rm_obj is a dictionary meant to hold the new object -- Also creates the "named" key.
        rm_obj = {"named":node.get_value("named") }
        
        #we'll want to adjust which attributes are told about at different depths
        s = "a"

        #The length of all of these is always either 1 or 0...
        #I will use colors for testing things and update other parts accordingly
        if len(node.get_all_type("colored"))>0:
            
            color_rand = random.randint(0, len(colors) - 1)     #select a random color
            rm_obj["colored"] = colors[color_rand]              #give rm_obj a "colored" attribute, and set it to the random color

            #print rm_obj's "colored" attribute -- prints properly
            s+= " " + rm_obj["colored"]
            
            #s+= " " + node.get_value("colored")[0].value
            #if there isn't a material, go ahead and say the color -- it actually already does that
            #if depth==0 or items[obj][attr["material"]] == "!=":
                #s += " "  + items[obj][attr["color"]]
        if len(node.get_all_type("is_made_of"))>0:
            #s+= " made_of " + node.get_all_type("is_made_of")[0].value  # returns true
            #s+= " " + node.get_relationship_types()
            mat_rand = random.randint(0, len(materials) - 1)
            rm_obj["is_made_of"] = materials[mat_rand]

            s+= " " + rm_obj["is_made_of"] #also returns true

        if len(node.get_all_type("size"))>0:

            bed_rand = random.randint(0, len(bed_sizes) - 1)
            rm_obj["size"] = bed_sizes[bed_rand]
            
            s+= " " + rm_obj["size"]
            
        if len(node.get_all_type("has_a"))>0:
            #s+= " " + node.get_value("has_a")      #true -- this is making things look weird without really adding anything
            pass
            
        if len(node.get_all_type("named"))>0:
            #This doesn't need to set anything because we have already created a key for "named"
            s+= " " + node.get_value("named") #the name/type of the item
            
        if len(node.get_all_type("titled"))>0:

            title_rand = random.randint(0, len(book_titles) - 1)
            rm_obj["titled"] = book_titles[title_rand]

            s+= ". The title reads: " + rm_obj["titled"] #the name/type of the item
            
        if len(node.get_all_type("power_state")) > 0:

            power_rand = random.randint(0, len(power_state) - 1)
            rm_obj["power_state"] = power_state[power_rand]
            
            s+= ". It is " + rm_obj["power_state"]
        
        #'''
        #Test "has_a" code
        #this is a relationship instance it doesn't have get_all_type
        if len(node.get_all_type("has_a"))>0:       
            for att in node.get_all_type("has_a"):
                if depth==0:#if this is the first layer
                        s += " with " + inspectObject(att, depth+1) #This could theoretically run forever...
                #else: #only one iteration
                        #s += " with " + items[obj][attr["with"]]
        #'''
                        
        #fix a/an issues 
        s = re.sub('\\ba ([aeiou])', 'an \\1', s)

        s += "."

        #add rm_obj to room_dict
        room_dict[rm_obj["named"]] = rm_obj
        
        return s

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
	isActionValid = False
	for d in dialogs:
		if d in action:
			isActionValid = True
			print(dialogs[d])
	if(not isActionValid):print("SYSTEM : Action not recognized")
				
    		
def Get_All_Edges(node):
    li = []
    for edge in node.get("edges"):
        terminal = edge.get("terminal")
        if terminal:
            li += [terminal]
    return li
            
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

        else:
            for word in shlex.split(action):
                #User's query is the action
                queryResult = json.loads(query(describe_noun(word, 2)))

                #try to get the node
                try:
                    node = get_node_by_name(word)
                except:
                    node = None
                    #see if this is one of the pre-defined player commands
                    try:
                        playerNode(action)
                    #If not, the player did something wrong -- or we did.
                    except:
                        #feedback for bad input
                        print("You can't do that.")
                    
                if node:
                    #inspect the node to a depth of... (depth doesn't seem to be doing anything right now)
                    print(inspectObject(node,2))
                    

#create a version of recSearch that is designed to list things
def listSearch(queryResult, searchFor, searchIn):
    ls = []

    if queryResult.get("type") == "get-success":
        roomConts[queryResult.get("id")] = []
        
        for response_node in queryResult.get("reply"):

            #looks for evbery node in the edges of that node, and finds our target
            #IMPORTANT!!! -- Need to make new versions of Check_Edge and Check_Terminal that return lists
            tmp = listEdge(response_node, searchFor, searchIn, ls)
            if tmp:
                #print (tmp)
                ls+=[tmp]
                
        return ls

def listEdge (node, searchFor, searchIn, DictToStore):
    
    for edge in node.get("edges"):
        if (edge.get(searchIn) == searchFor):
            #add to roomConts
            roomConts[edge.get("id")] = [edge.get("id"), edge.get("value"), edge.get("type"), edge.get("edges")]
            return edge

        else:
            tmp = listTerminal(edge, searchFor, searchIn, DictToStore)
            
            if tmp:
                DictToStore += tmp
                return edge

def listTerminal(edge, searchFor, searchIn, DictToStore):

    terminal = edge.get("terminal")
    if(terminal.get(searchIn) == searchFor):
        roomConts[terminal.get("id")] = [terminal.get("id"), terminal.get("value"), terminal.get("type"), terminal.get("edges")]
        return DictToStore
    else:
        #see if you got anything
        tmp = listEdge(terminal, searchFor, searchIn, DictToStore)

        #if tmp exists, add it to the list we want to store things in and return the list
        if tmp:
            DictToStore += tmp
            return terminal

#Working on a function to list room contents at game start
def listRoomConts(queryResult):
    
    returnDict = listSearch(queryResult, "noun", "type")
    #print ("1")
    i = 1
    for n in returnDict:
        print (str(i) + ": ")
        print (n)
        i += 1
        
    #pass
    return returnDict
    
#Class with ID and list of properties
    #fill up from initial query
    #take room object and use toString function to print things
    #player types something in
        #if any of those words are named properties of an object, find that object
        #loop forever

class room:
    def __init__(self, contents):
        self.contents = roomConts

    def rm_print(self):
        print (roomConts)


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
#rm = get_node_by_name("room")

#We have a set of functions that do the obnoxious node traversal!
qrNode = listSearch(queryResult, "room", "value")

#test to see if we are getting things in roomConts, as we are supposed to
roomPrint()

#rmcts is room contents
print("\nInside the room, you can see...\n")
#rmcts = recSearch(queryResult, "noun", "type")
#print(rmcts)

#print(rm.print_noun)
#print(rm.get_relationship_types)

#rmcts = str(get_node_by_name("chair"))
#rmcts += "\n" + str(get_node_by_name("table"))
#rmcts += "\n" + str(get_node_by_name("bed"))

#print (rmcts)


#This is...another way to make a room
#testRoom = room(get_node_by_name("room"))
#print("\n")
#testRoom.rm_print()

#get relationships in room
#room_rel = rm.get_relationship_types()
#print results
#print("\nRoom relations: " + str(room_rel))

rmcts = {"id" : 0, "rel_id" : 1, "value" : 2, "type" : 3, "edges" : 4}

#listRoomConts(qrNode)

#print (rmcts)

#wait for user input
testLoop()

#GAME END


