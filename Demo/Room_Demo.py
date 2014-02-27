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
chair.append("a chair")
table.append("a table")
bed.append("a bed")

#make potential chairs and tables
for m in hardMats:
	chair.append("a " + m + " chair")
	table.append("a " + m + " table")

#Array to hold a chair, a table, and a bed
roomContents=[chair[0],table[0],bed[0]]

#Note: Don't need to do anything to the first two randoms because they will pick a number from 1-3 in the chair and table arrays, respectively.
#Since chair[0] and table[0] are the basic versions of these objects, we don't need to worry about the range not including them
def inspectObject(obj):
	if obj[0] == "a chair":
		roomContents[0] = chair[random.randint(0,3)] #pick a random chair
	elif obj[0] == "a table":
		roomContents[1] = table[random.randint(0,3)]
	elif obj[0] == "a bed":
		#Frame, then type, then color. Reduce random number by 1 because arrays are 0-indexed
		roomContents[2] = "a " + hardMats[random.randint(0,3) - 1] + " " + bedSizes[random.randint(0,4) - 1] + " bed covered with a " + colors[random.randint(0,14) - 1] + " blanket"
#fill the room with stuff!
def fillRoom():
	#This code isn't working
	#roomContents.append[chair[0]]
	#roomContents.append[table[0]]
	#roomContents.append[bed[0]]
	print("You are in a room. Within the room, you can see: ")
	print("-- " + chair[0])
	print("-- " + table[0])
	print("-- " + bed[0])

#Game Loop
def testLoop():
	while(True):
		#create some space between this and last input/output
		print ("")
		action = input()
		
		#inspect objects
		if "chair" in action: 
		
			if(roomContents[0] == chair[0]):
				inspectObject(chair)
		
			print(roomContents[0])
		
		if "table" in action:
		
			if(roomContents[1] == table[0]):
				inspectObject(table)
		
			print(roomContents[1])
		
		if "bed" in action: 
		
			if(roomContents[2] == bed[0]):
				inspectObject(bed)
				
			print(roomContents[2])
		
		#leave the game
		if action == "exit":
			break 
		
#Run the game!
fillRoom()
testLoop()