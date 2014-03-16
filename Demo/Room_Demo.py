#needed for user input
import sys
import random
import shlex
import re
#Create an array of items (chairs, tables, beds, etc.)
items={}
attr = {'actions' : 0, 'material' : 1, 'size' : 2, 'color' : 3, 'with' : 4}


#create an dictionary of materials
materials ={"furniture" : ["plastic", "wood", "metal"],
			"fabric":["linen", "muslin", "tarp", "velvet"],
			"dishware" : ["plastic", "metal", "glass", "ceramic"]}
#bed sizes
bedSizes=["twin", "double", "queen-sized", "king-sized"]
#create an array of colors
colors=["burgundy", "violet", "goldenrod", "fuchsia", "lavender", "beige", "azure", "chartreuse", "celadon", "sage", "paisley", "plaid", "tartan", "scarlet"]

items["chair"] = [["sit", "jump", "under", "lift", "stand"], \
				random.choice(materials["furniture"]),
				"!=", random.choice(colors), "!="]

items["table"] = [["under", "lift", "search", "lean", "lie"], \
				random.choice(materials["furniture"]),
				"!=", random.choice(colors), "teapot"]

items["bed"] = [["sit", "jump", "search", "lean", "stand", "lie"], \
				random.choice(materials["furniture"]),
				random.choice(bedSizes), "!=", "cover"]

items["cover"] = [["sit", "jump", "search", "lean", "stand", "lie"], \
				random.choice(materials["fabric"]),
				"!=", random.choice(colors), "!="]

items["wall"] = [["search", "lean"], \
                "!=", "!=", random.choice(colors), "!="]

items["teapot"] = [["search", "lift"], \
                random.choice(materials["dishware"]),
				"!=", random.choice(colors), "liquid"]

items["liquid"] = [["search"], \
                "!=", "!=", random.choice(colors), "!="]

#Array to hold a chair, a table, a wall, and a bed
roomContents=["chair","table","bed", "wall"]

def inspectObject(obj, depth=0):
	#we'll want to adjust which attributes are told about at different depths
	if obj in items:
		s = "a"
		if not items[obj][attr["color"]] == "!=":
			#if there isn't a material, go ahead and say the color
			if depth==0 or items[obj][attr["material"]] == "!=":
				s += " "  + items[obj][attr["color"]]
		if not items[obj][attr["material"]] == "!=":
			s += " " + items[obj][attr["material"]]
		if not items[obj][attr["size"]] == "!=":
			s += " " + items[obj][attr["size"]]

		s+= " " + obj #the name/type of the item

		if not items[obj][attr["with"]] == "!=":
			if depth==0:#if this is the first layer
				s += " with " + inspectObject(items[obj][attr["with"]], depth+1)
			#else: #only one iteration
				#s += " with " + items[obj][attr["with"]]

		#fix a/an issues
		s = re.sub('\\ba ([aeiou])', 'an \\1', s)
		return s


#fill the room with stuff!
#Idea for fililng the room: only do this with stuff at a certain depth. Deeper stuff can be found by searching/inspecting objects (hidden panels, cupcakes, etc) ~Joe
def fillRoom():
	print("You are in a room with " + items["wall"][attr["color"]] + " walls. Within the room, you can see: ")
	for thing in roomContents:
		print("-- a " + thing)

#wherever the name of the object should be, we put 'obj'
#(we will search and replace it when we use it)
verbs = {         "sit" : ["You sit on the obj.","You can't sit on the obj."],
			"jump" : ["You jump on the obj.","You can't jump on the obj."],
			"under" : ["You crawl under the obj.", "You can't crawl under the obj"],
			"lift" : ["You lift the obj off of the ground.","You can't lift the obj"],
			"search" : ["You search the obj, finding nothing of interest.","You can't search the obj."],
			"lean" : ["You lean on the obj.","You cannot lean on the obj."],
			"stand" : ["You stand on the obj, taking great care not to fall.","You cannot stand on the obj."],
			"lie" : ["You lie down on the obj.","You cannot lie down on that obj."],
			"talk" : ["You try to talk to the obj.","Your only reply is the faint echo of your own voice."]

}
response_index = {"can" : 0, "can't" : 1}#removes hard-coding of indexes

def node(action):
	verb = ""
	subject = ""
	for word in shlex.split(action):#divides the action by spaces
		if word in items:
			subject = word
		if word in verbs:
			verb = word

	if subject == "": #if there is no subject, get out and check player
		return False
	if verb == "":#if there is subject but no action
		print(inspectObject(subject))#talk about the subject
	#there is a verb, and it can be applied to the subject
	elif(verb in items[subject][attr["actions"]] ):
		print(verbs[verb][response_index["can"]].replace("obj",subject))
	else: #you can't do that to this subject
		print(verbs[verb][response_index["can't"]].replace("obj",subject))
	return True

self_verbs = { "sit"	: "You sit down cross-legged on the floor.",
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
	for d in self_verbs: #go through self-targeted verbs
		if d in action: #if the verb is in the statement anywhere
			isActionValid = True
			print(self_verbs[d]) #get its sentence and print it
	return isActionValid

#Game Loop
def testLoop():
	while(True):
		#create some space between this and last input/output
		print("\n"),

		#since we have decided on python 2, just using raw_input
		#convert to lower case to prevent problems where there are none
		#(i.e. "SIT on Chair" should work just like "sit on chair")
		action = raw_input().lower()

		#if exit then quit
		if "exit" in action or "quit" in action or "bye" in action:
			print("okay, bye")
			break

		#do stuff with objects
		if not node(action):
			#Only access player node if you don't refer to any of the objects
			if not playerNode(action):
				print ("Sorry, please try something else.")



#This code runs as soon as the game starts...
#Run the game!
fillRoom()
testLoop()

