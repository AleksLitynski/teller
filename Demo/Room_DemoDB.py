#needed for user input
import sys
import random
import shlex
import socket
import re
#importing our stuff
import json
from RefCode.Query_Explorer import *
#Nodes have: ID, type, value, & List of Edges
#

#====database talk==============
#This is how we contact the database
def query(query_string):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5005))
    s.send(query_string)            #This fails on a bad query?
    query_response = s.recv(10000) #our replies are VERY long. don't recurse into nodes that already exist?
    s.close()
    return query_response


#Give node a name and a depth; 2 is default, and higher is said to cause issues
def describe_noun(noun_name, depth=2):
    #the only thing that really changes is name, the rest are defaults
    txt = '{"type": "get", "params": {"depth":'+str(depth)+'}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1",' +\
           '"terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "'+noun_name+'"}}]}}]}}'
    return txt

#searches in the database for a node with a certain id
#to a certain depth (todo: describe consequences)
def get_node(node_id, depth=2):
    return '{"type": "get", ' \
           '"params": {"depth":'+str(depth)+'}, ' \
           '"search": {"id":"'+node_id+'"}}'


#uses queries to get the node based on its name
def get_node_by_name(name):
    #get the JSON for the node
    query_string = describe_noun(name, 2)
    #ask the database using it
    noun = get_noun(json.loads(query(query_string)))

    return noun

#gets the node by its name, and then filters it based
#on whether the player would know it exists.
def get_known_node(name):
    noun = get_node_by_name(name)
    if noun:
        if len(noun.get_all_type("knows_of"))>0:
            return noun
    return None


#========database talk end========================
#========print stuff we wanna know about start====
#print everything the player knows about
def print_known():
    s = ""
    for obj in get_known():
        if s == "":
            s+= "a "+obj
        else:
            s+= ", a "+obj
    return a_an(s)


#get everything the player knows about, return string array
def get_known():
    node = get_node_by_name("player")
    return node.get_values("knows_of")

# does a rudimentary a/an fix
def a_an(s):
    s = re.sub('\\bA ([aeiou])', 'An \\1', s)
    return re.sub('\\ba ([aeiou])', 'an \\1', s)

#todo move to node class
def has_attr(node, attr):
    return len(node.get_all_type(attr))>0

#takes a noun node and converts it to a describing sentence
def inspectObject(node, depth=0):

    #we'll want to adjust which attributes are told about at different depths
    s = "A"

    if has_attr(node, "colored"):
        s+= " " + node.get_value("colored")

    if has_attr(node, "is_made_of"):
        s+= " " + node.get_value("is_made_of")

    if has_attr(node, "floor_mat"):
        s+= " " + node.get_value("floor_mat")

    if has_attr(node, "bed_size"):
        s+= " " + node.get_value("bed_size") + "-sized"

    if has_attr(node, "named"):
        s+= " " + node.print_noun() #the name/type of the item

    if has_attr(node, "titled"):
        s+= ". The title reads: " + node.get_value("titled")

    if has_attr(node, "contains"):
        s += ". It contains " + node.get_value("contains")

    if has_attr(node, "power_state"):
        s+= ". It is " + node.get_value("power_state")

    if has_attr(node, "has_a"):
        s+= ". It has a " + node.get_value("has_a")
        #Todo: add to known

    if has_attr(node, "had_by"):
        s+= ". It is had by " + node.get_value("had_by")
        #Todo: add to known


    #'''
    #Test "has_a" code
    #this is a relationship instance it doesn't have get_all_type
    #this was working fine, todo: talk
    if len(node.get_all_type("has_a"))>0:
        for att in node.get_all_type("has_a"):
            if depth==0:#if this is the first layer
                    s += " with " + inspectObject(att, depth+1)
            #else: #only one iteration
                    #s += " with " + items[obj][attr["with"]]
    #'''

    #fix a/an issues
    s = a_an(s)

    s += "."

    return s
#===============print stuff we wanna know about end=================
#===============process actions start===============================
#processes player actions/verbs
#mysteriously missing non-player-targeted verbs?
#todo rename
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
    else:
        print(dialogsNode[verb][1].replace("obj",subject))
    return True

#list of available actions and responses
#todo rename, change to methods

dialogs = { "sit"    : "You sit down cross-legged on the floor.",
            "dance"    : "You dance for a moment, though you are not sure why."
                        + "\nIt is almost as if you are a puppet whose strings are being"
                        + "\npulled by the invisible hands of some unknown God..."
                        + "\nYou quickly dismiss that thought and return to a standing position.",
            "lie" : "You lie down on the floor.",
            "talk" : "You talk to yourself. Sadly, doing so provides you with no new information.",
            "jump" : "You jump up and down. It's good for your buns and thighs."
}
#processes self-targeted actions
def playerNode(action):
    isActionValid = False
    for d in dialogs:
        if d in action:
            isActionValid = True
            print(dialogs[d])
    if(not isActionValid):print("SYSTEM : Action not recognized")
#=======process actions end=================
#=======Queries start=================================
#creates a query that asks for a node of a certain id and type
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

#creates a query that asks for a node of a certain value and type
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

#=============queries end==========================

#=============Ignore Me!! (for now)================
"""

#function to allow users to create new objects from the console
def playerCreateObject():

    #spoon = new_noun()
    #add_property(spoon, "named", "spoon", english())

    #make sure the user did not come here in error
    print("Would you like to make an object? (Y/N)")
    want_new_obj = raw_input().lower()

    #Fork node from another node to create a new node
    #You can give a new name to the new node
    #You can fork noun/verb/etc -- we will assume noun for now
    #To change weight use update and alter the weight (0 to 100)

    if want_new_obj.startswith('y'):

        #Create a new noun
        ob = new_noun()
        
        #prompt for name of object
        print("What do you want to create?")
        obj_name = raw_input().lower()

        #add "named" property to the new noun and give it obj_name as a value
        add_property(ob, "named", obj_name, english())

        #add attributes to object, if applicable
        print("Would you like to add an attribute to " + obj_name + "? (Y/N)")
        att_permission = raw_input().lower()

        if att_permission.startswith('y'):

            #give attribute a name
            print("Name of attribute:")
            att_name = raw_input().lower()

            #add property to the noun and give it a value
            print("Value of attribute:")
            att_val = raw_input().lower()
            add_property(ob, att_name, att_val, english())

    #fork from type of node (noun, verb, etc) user wants -- Assume noun
    #fork("noun", obj_name, 1)



    output = query(get_from_value("room", "named"))
    #print(output)
    out_id = json.loads(output)["reply"][0]["id"]


    output = query(
        json.dumps({
        "type": "fork",
        "params":{"depth":"0"},
        "search":{"new-value": obj_name,"time":1,"target-node": {"id":out_id}}}))


    print(output)

    #test new object
    #nd = get_node_by_name(obj_name)
    #inspect_object(nd)

#add a relationship to an object
def add_rel():
    print("object to add to:")
    add_to = raw_input().lower()

    print("target: ")
    target = raw_input().lower()

    print("Relationship name: ")
    rel_name = raw_input().lower()

    print("Value: ")
    value = raw_input().lower()


    left = node.get_value("had_by")
    output = query(get_from_value(add_to, "named"))
    left_id = json.loads(output)["reply"][0]["id"]

    output = query(get_from_value(target, "named"))
    right_id = json.loads(output)["reply"][0]["id"]

    query(
        json.dumps({
            "type": "update",
            "params":{"depth":"0"},
            "search":{"time":1,"weight": 100,"left-node": {"id":left_id},"right-node": {"id":right_id}}
            }))

"""
#=============Ignore Me!! end======================

#Pick up an object (remove from room add to inventory)
def remove_obj():

    print("Object to pick up?")
    ob = raw_input().lower()

    try:
        node = get_node_by_name(ob)

    except:
        node = None
        #see if this is one of the pre-defined player commands

    if node:
        #inspect the node to a depth of... (depth doesn't seem to be doing anything right now) todo: talk
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
                "search":{"time":1,"weight": 0,"left-node": {"id":had_id},"right-node": {"id":ob_id}}
                }))

        #node.set_value()


#creates a node and gives it a "named" "spoon" property
#returns the ID of the spoon
def create_a_spoon():
    spoon = new_noun()
    add_property(spoon, "named", "spoon", english())
    return spoon

#creates a node with set parameters, takes a name, lists of attributes and values, and whether or not you want it to print
def devCreateSet(name, attList=None, valList=None, displayInfo=None):
    #set up the name
    temp_noun = new_noun()
    add_property(temp_noun, "named", name, english())
    
    #only print things if displayInfo is set to something
    if displayInfo:
        print(name)
    
    #set iterator to 0
    iterator = 0 
    #only add attributes if there is one
    if len(attList) > 0:
        #add a new attribute and corresponding value
        for att in attList:
            add_property(temp_noun, attList[iterator], valList[iterator], english())
            
            if displayInfo:
                print(attList[iterator] + ": " + valList[iterator])     #proves that attList[iterator] and valList[iterator] are working
            
            iterator += 1
            
    #return the new noun
    return temp_noun
    
#Name of value; dictionary of attributes (keys), each of which contains a list of potential values; and whether or not you want it to print
def devCreateRandom(name, attDict=None, displayInfo=None):
    
    temp_noun = new_noun()
    add_property(temp_noun, "named", name, english())
    
    if displayInfo:
        print(name)
    
    #set iterator to 0
    iterator = 0 
    #don't do this if the dictionary is empty
    if len(attDict) > 0:
        #add a new attribute and corresponding value
        for att in attDict:
            
            #get random number from 0 to length of list inside dictionary
            tempRand = random.randrange(0, len(attDict[attDict.keys()[iterator]]))
            #set temporary value to a random value from each list (all of which are keys), in order
            tempVal = attDict[attDict.keys()[iterator]][tempRand]
            
            add_property(temp_noun, attDict.keys()[iterator], tempVal, english())
            
            if displayInfo:
                print(attDict.keys()[iterator] + ": " + tempVal)     #proves that attList[iterator] and valList[iterator] are working
            iterator += 1
            
    #return the new noun
    return temp_noun

    
#returns the ID of the node that connotes the english language
def english():
    query_result = query(json.dumps({
        "type":"get",
        "params": {"depth":-1},
        "search":{"type":"noun",
            "edges":[
                {"terminal":{"type":"relationship",
                    "edges":[
                        {"terminal":{"type":"type", "value":"named"}},
                        {"terminal":{"type":"value","value":"english"}}
        ]}}]}}))

    return json.loads(query_result)["reply"][0]["id"]

#forks a new noun
def new_noun():
    return fork_core_node("noun")

#add a property to a noun (property == type+value+target_noun)
#from_id is your starting noun
#type is the property's type (ie: named or has_a)
#value is it's value (ie: frank or true)
#noun_id is the noun it reguard. For words, it should be a language. See "english()" function
def add_property(from_id, _type, value, noun_id):

    relationship_id = fork_core_node("relationship")
    value_id = fork_core_node("value", value)
    type_id = fork_core_node("type", _type)


    update_edge_between(relationship_id, value_id, "has_value")
    update_edge_between(relationship_id, type_id, "has_type")

    update_edge_between(relationship_id, from_id, "describes")
    update_edge_between(relationship_id, noun_id, "reguarding")


#Two ide's and an optional weight for extending edges. Still debugging this function
def update_edge_between(left_id, right_id, _type, weight=100):
    query_result = query(json.dumps({
        "type": "update",
        "params":{"depth":1},
        "search":{
            "weight":weight,
            "time": 1,
            "type":_type,
            "left-node": { "id":left_id },
            "right-node": {"id":right_id}}}))

#fork's one of the "core" nodes. These nodes will (soon) allow me to remove apriori knowledge of the structure of the ontology
#The type of the node to fork. Should be: "noun", "relationship", "value", "type", "constraint", etc (rest may not be implemented. not really sure...)
#optional value for forked node
def fork_core_node(_type, value=""):
    # { "new-value":"VALUE OF FORKED NODE", "time":"FLOAT TIME OF CREATION", "target-node": { #GET QUERY THAT RETURNS EXACTLY ONE NOUN TYPE NODE } }
    query_result = query(json.dumps({
        "type": "fork",
        "params":{"depth":1},
        "search":{
            "new-value":value,
            "time": 1,
            "target-node": {
                "type": _type,
                "value":"***core-node***"}}}))

    return json.loads(query_result)["reply"][0]["id"]


#Game Loop
def testLoop():


    while(True):
        #create some space between this and last input/output
        print("\n"),
        #raw_input for 2.7
        action = raw_input().lower()
        #convert to lower case (so "SIT on Chair" should work just like "sit on chair")

        #let the user leave the game
        if action == "exit" or action == "quit":
                print("Okay, bye!")
                break

        #Allow the user to look around again in case they have forgotten
        elif action == "room" or action == "look":
            print("You see "+print_known())

        elif action == "take" or action == "pickup":
            remove_obj()

        #Let the player Create new object -- Not really working currently
        elif action == "create" or action == "make":
            #playerCreateObject()
            pass
        
        #Both devCreate methods are working so far. I'm not sure if they are saving the nodes to the database yet, though
        #Literally just making something to test devCreateSet
        elif action == "dog":
            corgi = devCreateSet("corgi", ['personality', 'fur', 'awake?'], ['energetic', 'chocolate', 'sleeping'], True)
            #print(describe_noun(corgi, 1))
        #Ditto with devCreateRandom
        elif action == "cat":
            feline = devCreateRandom("cat", {'Name on collar':['Khoshekh', 'Heathcliff', 'Mr. Bigglesworth'], 
                                            'Mood':['disinterested', 'sleepy', 'hyperactive'],
                                            'Fur':['black', 'orange', 'white', 'tan']}, True)
            #print(describe_noun(feline, 1))

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
                    #inspect the node to a depth of... (depth doesn't seem to be doing anything right now) todo: talk
                    print(inspectObject(node,2))



#==============GAME START========================================
#This code runs as soon as the game starts...

print("You are in a room.")

queryResult = json.loads(query(describe_noun("room", 2)))   #the 2 indicates we go down to a depth of 2

#this is the room
#rm = get_node_by_name("room")

print("\nInside the room, you can see...\n")
print(print_known())

rmcts = {"id" : 0, "rel_id" : 1, "value" : 2, "type" : 3, "edges" : 4}

#create something so we can test if new nodes are added to database - Well, you don't seem to be able to search for it...
bird = devCreateRandom("parrot", {'Answers to':['Paulie', 'Iago', 'Chirpy', 'Clarice'], 
                                            'Mood':['watchful', 'sleepy', 'talkative', 'hungry'],
                                            'Feathers':['red', 'green', 'blue', 'purple']})


#wait for user input
testLoop()

#==============GAME END==========================================


