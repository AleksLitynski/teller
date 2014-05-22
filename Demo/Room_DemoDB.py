#needed for user input
import sys
import random
import shlex
import socket
import re
import json
#from RefCode.Query_Explorer import *
from roombuilder.helper import *
from database_queries import *

import subprocess
import threading
import time


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
    print node.get_value("knows_of")
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
        pl = get_node_by_name("player")
        update_edge_between(node.get_value("id"), pl.get_value("id"), "knows_of", 100)
        update_edge_between(pl.get_value("id"), node.get_value("id"), "knows_of", 100)
        print(pl.get_value("knows_of"))
        print(node.get_value("knows_of"))
        
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
#=================================================================================

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
        elif action == "make dog":
            corgi = devCreateSet("corgi", ['personality', 'fur', 'awake?'], ['energetic', 'chocolate', 'sleeping'], True, True)
            #print(describe_noun(corgi, 1))
        #Ditto with devCreateRandom
        elif action == "make cat":
            feline = devCreateRandom("cat", {'Name on collar':['Khoshekh', 'Heathcliff', 'Mr. Bigglesworth'], 
                                            'Mood':['disinterested', 'sleepy', 'hyperactive'],
                                            'Fur':['black', 'orange', 'white', 'tan']}, True, True)
            #print(describe_noun(feline, 1))

        else:
            for word in shlex.split(action):
                #User's query is the action
                resultString = query(describe_noun(word, 1))


                #try to get the node
                #try:
                node = get_known_node(word)
                '''
                except:
                    node = None
                    #see if this is one of the pre-defined player commands
                    try:
                        playerNode(action)
                    #If not, the player did something wrong -- or we did.
                    except:
                        #feedback for bad input
                        print("You can't do that.")
                '''
                if node:
                    #inspect the node to a depth of... (depth doesn't seem to be doing anything right now) todo: talk
                    print(inspectObject(node,2))



#==============GAME START========================================
#This code runs as soon as the game starts...

print("You are in a room.")

queryResult = query(describe_noun("room", 2))   #the 2 indicates we go down to a depth of 2

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


