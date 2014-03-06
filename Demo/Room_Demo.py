#needed for user input
import sys
import random
import shlex
#importing our stuff
import json
from Query_Explorer import *

#Create an array of items (chairs, tables, beds, etc.)
items={}
attr = {'actions' : 0, 'material' : 1, 'size' : 2, 'cover_color' : 3}


#create an array of hard materials
hardmats=["plastic", "wood", "metal"]

#bed sizes
bedSizes=["twin", "double", "queen-sized", "king-sized"]

#create an array of colors
colors=["burgundy", "violet", "goldenrod", "fuchsia", "lavender", "beige", "azure", "chartreuse", "celadon", "sage", "paisley", "plaid", "tartan", "scarlet"]

items["chair"] = [["sit", "jump", "under", "lift", "stand"], \
				random.choice(hardmats), "!=", "!="]

items["table"] = [["under", "lift", "search", "lean", "lie"], \
				random.choice(hardmats), "!=", "!="]

items["bed"] = [["sit", "jump", "search", "lean", "stand", "lie"], \
				random.choice(hardmats), random.choice(bedSizes), random.choice(colors)]

items["wall"] = [["search", "lean"], \
                                "!=", "!=", random.choice(colors)]

items["teapot"] = [["search", "lift"], \
                               random.choice(hardmats), "!=", "!="]

#Array to hold a chair, a table, a wall, and a bed
roomContents=["chair","table","bed", "wall", "teapot"]

def inspectObject(obj):
	if obj == "chair" or obj == "table" or obj == "teapot":
		return "a " + items[obj][attr["material"]] + " " + obj
	elif obj == "wall":
                return ("You see a " + items[obj][attr["cover_color"]] + " " + obj + " on the other side of the room."
                        + "\nA large painting hangs crookedly above an old-fasioned fireplace.") 
	elif obj == "bed":
		#Frame, then type, then color
		return "a " + items["bed"][attr["material"]] + " " + items["bed"][attr["size"]] + " bed covered with a " + items["bed"][attr["cover_color"]] + " blanket"
	
	
#fill the room with stuff!
#Idea for fililng the room: only do this with stuff at a certain depth. Deeper stuff can be found by searching/inspecting objects (hidden panels, cupcakes, etc) ~Joe
def fillRoom():
	print("You are in a room with " + items["wall"][attr["cover_color"]] + " walls. Within the room, you can see: ")
	for thing in roomContents:
		print("-- a " + thing)

#reasoning : they all shared the same pattern which can be factored out
#			And though they convey little importance than different outcome, they occupied much space
#			Combining them this way it is more readable
#			readable because you are interested only in the different output message. -- I think this is a huge improvement. Great job! ~Joe
dialogsNode = {         "sit" : ["You sit on the obj.","You can't sit on the obj."], 
			"jump" : ["You jump on the obj.","You can't jump on the obj."], 
			"under" : ["You crawl under the obj.", "You can't crawl under the obj"],
			"lift" : ["You lift the obj off of the ground.","You can't lift the obj"], 
			"search" : ["You search the obj, finding nothing of interest.","You can't search the obj."],
                        "lean" : ["You lean on the obj.","You cannot lean on the obj."],
                        "stand" : ["You stand on the obj, taking great care not to fall.","You cannot stand on the obj."],
                        "lie" : ["You lie down on the obj.","You cannot lie down on that obj."],
                        "talk" : ["You try to talk to obj.","Your only reply is the faint echo of your own voice."]
                        
}
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
				
#Game Loop
def testLoop():
	while(True):
		#create some space between this and last input/output
		print("\n"),
		#input() does not work on my system, don't know why, so if it doesn't work, just try raw_input instead
		try:
                        action = input().lower()    #convert to lower case to prevent problems where there are none (i.e. "SIT on Chair" should work just like "sit on chair")

                        #leave the game if the user wants to -- Moving it here prevents the game from yelling at the user when he/she exits ~Joe
                        if action == "exit":
                                break 

		except :
			#Failed with function input. Attempting to use function raw_input instead
			print("Sorry the game made a mistake, could you type it one more time?\n   "),
			try: action = raw_input().lower()
			except :
				print("SYSTEM : Cannot process user input")
				break;
		
		#do stuff with objects
		if not node(action):
			#Only access player node if you don't refer to any of the objects
			playerNode(action)
		
		
		
#This code runs as soon as the game starts...	
#Run the game!
fillRoom()
testLoop()

