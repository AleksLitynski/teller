#needed for user input
import sys
import random
import shlex

#Create an array of chairs, tables, and beds
items={}
attr = {'actions' : 0, 'material' : 1, 'size' : 2, 'cover_color' : 3}


#create an array of hard materials
hardmats=["plastic", "wood", "metal"]

#bed sizes
bedSizes=["twin", "double", "queen-sized", "king-sized"]

#create an array of colors
colors=["burgundy", "violet", "goldenrod", "fuchsia", "lavender", "beige", "azure", "chartreuse", "celadon", "sage", "paisley", "plaid", "tartan", "scarlet"]

items["chair"] = [["sit", "jump", "under", "lift"], \
				random.choice(hardmats), "!=", "!="]

items["table"] = [["under", "lift", "search"], \
				random.choice(hardmats), "!=", "!="]

items["bed"] = [["sit", "jump", "search"], \
				random.choice(hardmats), random.choice(bedSizes), random.choice(colors)]

#Array to hold a chair, a table, and a bed
roomContents=["chair","table","bed"]

def inspectObject(obj):
	if obj == "chair" or obj == "table":
		return "a " + items[obj][attr["material"]] + " " + obj
		
	elif obj == "bed":
		#Frame, then type, then color
		return "a " + items["bed"][attr["material"]] + " " + items["bed"][attr["size"]] + " bed covered with a " + items["bed"][attr["cover_color"]] + " blanket"
	
	
#fill the room with stuff!
def fillRoom():
	print("You are in a room. Within the room, you can see: ")
	for thing in roomContents:
		print("-- a " + thing)

	
def node(action):
	verb = "!="
	subject = "!="
	for word in shlex.split(action):#divides the action by spaces
		if word in roomContents:
			subject = word
		elif word in methods:
			verb = word
	#verb methods are defined at the bottom of the file
	

	if subject == "!=" and not "exit" in action:
		print("I don't know what you're talking about.")
	else:
		if verb == "!=":
			print(inspectObject(subject))
		else:
			methods[verb](subject, (verb in items[subject][attr["actions"]]))
			#arg 2 evaluates to a boolean: can you verb this subject
			#the method uses this to determine what happens

	
def sitOnIt(obj, can):
	if can:
		print("You sit on the " + obj + ".")
	else:
		print("You can't sit on the " + obj + ".")

def jumpOnIt(obj, can):
	if can:
		print("You jump on the " + obj + ".")
	else:
		print("You can't jump on the " + obj + ".")

def duckAndCover(obj, can):
	if can:
		print("You crawl under the " + obj + ".")
	else:
		print("You can't crawl under the " + obj + ".")
	
def lift(obj, can):
	if can:
		print("You lift the " + obj + " off of the ground.")
	else:
		print("You can't lift the " + obj + ".")
	
def search(obj, can):
	if can:
		print("You search the " + obj + ", finding nothing of interest.")
	else:
		print("You can't search the " + obj + ".")
	
methods = {"sit" : sitOnIt, "jump" : jumpOnIt, "under" : duckAndCover, \
	   "lift" : lift, "search" : search}
	

#Game Loop
def testLoop():
	while(True):
		#create some space between this and last input/output
		print ("")
		action = input()
		
		#do stuff with objects
		node(action)
		
		#leave the game
		if action == "exit":
			break 
		
#This code runs as soon as the game starts...	
#Run the game!
fillRoom()
testLoop()

