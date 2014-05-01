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


"""
#Queries: edges, fork, get, update
#Queries can be found in database/queries
Query Structure:

    {
        "type":"NAME OF A FILE IN QUERIES FOLDER",
        "params": {
                      "depth":"INTIGER DEPTH TO EXPLORE EACH SUBEDGE/TERMINAL"
                  },
        "search": {
                      #STRUCTURE WILL BE PASSED TO SPECIFIED QUERY
                  }

    }


"""

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
    query_string = describe_noun(name, 2)

    noun = get_noun(json.loads(query(query_string)))
    '''
    noun = pipe(query_string, [ 
        query,
        json.loads,
        get_noun
    ])
    '''

    return noun

def get_known_node(name):
    noun = get_node_by_name(name)
    if noun:
        if len(noun.get_all_type("knows_of"))>0:
            return noun
    return None

def print_known():
    node = get_node_by_name("player")

    print(node.get_values("knows_of"))
    
    pass


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


def inspectObject(node, depth=0):

    #we'll want to adjust which attributes are told about at different depths
    s = "A"

    #lengthy string-addition code has been put in print_node()
    #The length of all of these is always either 1 or 0...
    if len(node.get_all_type("colored"))>0:
        
        s+= " " + node.get_value("colored")
        
    if len(node.get_all_type("is_made_of"))>0:

        s+= " " + node.get_value("is_made_of")

    if len(node.get_all_type("floor_mat"))>0:

        s+= " " + node.get_value("floor_mat")
    
    if len(node.get_all_type("bed_size"))>0:
        
        s+= " " + node.get_value("bed_size") + "-sized"
        
    if len(node.get_all_type("named"))>0:
        s+= " " + node.print_noun() #the name/type of the item
    
    if len(node.get_all_type("titled"))>0:

        s+= ". The title reads: " + node.get_value("titled")

    if len(node.get_all_type("contains"))>0:

        s += ". It contains " + node.get_value("contains")
    
    if len(node.get_all_type("power_state")) > 0:

        s+= ". It is " + node.get_value("power_state")

    if len(node.get_all_type("has_a"))>0:
        s+= ". It has a " + node.get_value("has_a")
        #Todo: add to known
        pass
    if len(node.get_all_type("had_by"))>0:
        s+= ". It is had by " + node.get_value("had_by")
        #Todo: add to known
        pass
    
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
    s = re.sub('\\bA ([aeiou])', 'An \\1', s)

    s += "."

    return s

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


dialogs = {             "sit"    : "You sit down cross-legged on the floor.",
            "dance"    : "You dance for a moment, though you are not sure why." 
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

    node = get_node_by_name("room")
    print(node.get_value("in_room"))

def get_from_id(val_id, val_type):
    results = json.dumps({
        "type":"get",
        "params":{"depth":0},
        "search":
        {
            "edges":
            [{
                "type":"has_value",
                "terminal":
                {
                    "type":"relationship",
                    "edges":
                    [
                        {"terminal":{"id": val_id}},
                        {"terminal":{"type": val_type}}
                    ]
                }
            }]
        }
    })

    return results

def get_from_value(val, val_type):
    results = json.dumps({
        "type":"get",
        "params":{"depth":0},
        "search":
        {
            "edges":
            [{
                "terminal":
                {
                    "type":"relationship",
                    "edges":
                    [
                        {"terminal":{"value": val}},
                        {"terminal":{"value": val_type}}
                    ]
                }
            }]
        }
    })

    return results

def json_from_id(value, val_type):
    results = {
    "search":
        {
            "edges":
            [{
                "type":"has_value",
                "terminal":
                {
                    "type":"relationship",
                    "edges":
                    [
                        {"terminal":{"value": value}},
                        {"terminal":{"type": val_type}}
                    ]
                }
            }]
        }
    }
    return results

#function to allow users to create new objects from the console
def createObject():
    #make sure the user did not come here in error
    print("Would you like to make an object? (Y/N)")
    want_new_obj = raw_input().lower()

    #Fork node from another node to create a new node
    #You can give a new name to the new node
    #You can fork noun/verb/etc -- we will assume noun for now
    #To change weight use update and alter the weight (0 to 100)

    if want_new_obj == "yes" or want_new_obj == "y":

        #We will need a way of referring to the database
        queryResult = json.loads(query(describe_noun("room", 2)))
        
        #prompt for name of object
        print("What do you want to create?")
        obj_name = raw_input().lower()

        #Not sure if this will even work -- No. No, it doesn't.
        #ob = new_noun_named(obj_name, "english")
        
        #add attributes to object, if applicable
        print("Would you like to add an attribute to " + obj_name + "? (Y/N)")
        att_permission = raw_input().lower()

        if att_permission == "yes" or att_permission == "y":

            #give attribute a name
            print("Name of attribute:")
            att_name = raw_input().lower()

            #give attribute a list of values
            print("Value of attribute:")
            att_vals = []
            att_vals.append(raw_input().lower())

    #fork from type of node (noun, verb, etc) user wants -- Assume noun
    #fork("noun", obj_name, 1)
            
    #"""
            
    output = query(get_from_value("room", "named"))
    #print(output)
    out_id = json.loads(output)["reply"][0]["id"]

            
    output = query(
        json.dumps({
        "type": "fork",
        "params":{"depth":"0"},
        "search":{"new-value": obj_name,"time":1,"target-node": {"id":out_id}}}))
    #"""

    print(output)
    
    #test new object
    #nd = get_node_by_name(obj_name)
    #inspect_object(nd)

#Pick up an object (remove from room add to inventory)
def pickUp():

    print("Object to pick up?")
    ob = raw_input().lower()

    try:
        node = get_node_by_name(ob)
            
    except:
        node = None
        #see if this is one of the pre-defined player commands
            
    if node:
        #inspect the node to a depth of... (depth doesn't seem to be doing anything right now)
        #print(inspectObject(node,2))

        had = node.get_value("had_by")
        output = query(get_from_value(ob, "named"))
        ob_id = json.loads(output)["reply"][0]["id"]

        output = query(get_from_value(had, "named"))
        had_id = json.loads(output)["reply"][0]["id"]

        query(
        json.dumps({
        "type": "update",
        "params":{"depth":"0"},
        "search":{"time":1,"weight": 0,"left-node": {"id":had_id},"right-node": {"id":ob_id}}}))
        
        #node.set_value()

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

        #Allow the user to call roomPrint() in case they need a reminder.
        elif action == "room" or action == "look":
            #roomPrint()
            print_known()

        elif action == "take" or action == "pickup":
            pickUp()

        #Create new object
        elif action == "create" or action == "make":
            createObject()

        else:
            for word in shlex.split(action):
                #User's query is the action
                resultString = query(describe_noun(word, 1))
                

                #try to get the node
                try:
                    node = get_known_node(word)
                    
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
#roomPrint()

print_known()

#rmcts is room contents
print("\nInside the room, you can see...\n")

rmcts = {"id" : 0, "rel_id" : 1, "value" : 2, "type" : 3, "edges" : 4}

#wait for user input
testLoop()

#GAME END


