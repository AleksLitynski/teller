#needed for user input
import sys
import random

#Create an array of chairs, tables, and beds
chair=[]
table=[]
bed=[]

#create an array of hard materials
hardMats=["plastic", "wood", "metal"]

#bed sizes
bedSizes=["twin", "double", "queen-sized", "king-sized"]

#create an array of colors
colors=["burgundy", "violet", "goldenrod", "fuchsia", "lavender", "beige", "azure", "chartreuse", "celadon", "sage", "paisley", "plaid", "tartan", "scarlet"]


#Create some strings to act as nodes
chair.append("chair")
table.append("table")
bed.append("bed")

#make potential chairs and tables
for m in hardMats:
	chair.append("a " + m + " chair")
	table.append("a " + m + " table")

#Array to hold a chair, a table, and a bed
roomContents=[chair[0],table[0],bed[0]]

#Note: Don't need to do anything to the first two randoms because they will pick a number from 1-3 in the chair and table arrays, respectively.
#Since chair[0] and table[0] are the basic versions of these objects, we don't need to worry about the range not including them
def inspectObject(obj):
	if obj[0] == "chair":
		roomContents[0] = chair[random.randint(0,3)] #pick a random chair
	elif obj[0] == "table":
		roomContents[1] = table[random.randint(1,3)]
	elif obj[0] == "bed":
		#Frame, then type, then color. Reduce random number by 1 because arrays are 0-indexed
		roomContents[2] = "a " + hardMats[random.randint(0,3) - 1] + " " + bedSizes[random.randint(0,4) - 1] + " bed covered with a " + colors[random.randint(0,14) - 1] + " blanket"
#fill the room with stuff!
def fillRoom():
	#This code isn't working
	#roomContents.append[chair[0]]
	#roomContents.append[table[0]]
	#roomContents.append[bed[0]]
	print("You are in a room. Within the room, you can see: ")
	print("-- a " + chair[0])
	print("-- a " + table[0])
	print("-- a " + bed[0])

#stuffInRoom[chair[0], table[0], bed[0]]
	
def sitOnIt(obj):
	print("You sit on the " + obj);

def UserAction(action):
	
	#object represents something you want to do stuff to
	object = ""
	
	obj[roomContents[0], roomContents[1], roomContents[2]]
	inspected[roomContents[0], roomContents[1], roomContents[2]]
	
	if "chair" in action:
		object = roomContents[0]
	elif "table" in action:
		object = roomContents[1]
	elif "bed" in action:
		object = roomContents[2]
	
	if ("sit on " + object) in action:
		sitOnIt(obj)
		
	if ("look at " + object) in action:
		if inspected[0] == object:
			inspectObject(inspected[0])
			inspectObject = roomContents
		
	
def chairNode(action):
	if "chair" in action: 
		
			if(roomContents[0] == chair[0]):
				inspectObject(chair)
			
			if "sit on chair" in action:
				sitOnIt(chair[0])
			
			else:
				print(roomContents[0])

def tableNode(action):
	if "table" in action:
		
			if(roomContents[1] == table[0]):
				inspectObject(table)
			
			if "sit" in action:
				sitOnIt(table[0])
			
			else:
				print(roomContents[1])
				
def bedNode(action):
	if "bed" in action: 
		
			if(roomContents[2] == bed[0]):
				inspectObject(bed)
			
			if "sit" in action:
				sitOnIt(bed[0])
			
			else:
				print(roomContents[2])	
		
#Game Loop
def testLoop():
	while(True):
		#create some space between this and last input/output
		print ("")
		action = input()
		
		#UserAction(action)
		
		#do stuff with objects
		chairNode(action)
		tableNode(action)
		bedNode(action)
		
		#leave the game
		if action == "exit":
			break 
		
#This code runs as soon as the game starts...	
#Run the game!
fillRoom()
testLoop()