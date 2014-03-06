import networkx as nx
import pickle
import uuid
from random import choice

#A node has an uuid, a type, and a value. Types may be used by the DB, values never will be.
class node:
	def __init__(self, id, node_type, value):
		self.id = id
		self.type = node_type
		self.value = value

#Edge src and dest are stored by networkX. I store edge weights here.
#Weights vary over time. Only part of the graph that varies over time.
#Weights are a % chances that the edge "really exists" at a given time.
#This will be optimized into a list of ranges later.
#By making edges exist over time, the graph doesn't NEED to be mutable (although I bet some people would like it if it were)
class edge:
	def __init__(self, edge_type):
		self.type = edge_type
		self.weights = {}

	#add support for ranges
	#use: http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-some-value
	def add_weight(self, time, weight):
		self.weights[time] = weight

#An ontology has:
#Add node
#Add edge
#Graph
#save
#load
#debug helper functions
class ontology:
	def __init__(self):
		self.graph = nx.Graph()
		pass

	#confirms the node if of a valid type and adds it to the graph with a UUID
	def add_node(self, type, value):
		#print type + " " + value + "<----"
		valid_nodes = [ "noun",
						"relationship",
						"value",
						"type",
						"verb",
						"change",
						"constraint"]

		new_node = node( str(uuid.uuid1()), type, value )

		if type in valid_nodes:
			self.graph.add_node( new_node )
		else:
			new_node = type + " is invalid node type"
		return new_node

	#confirms edge type and adds it to the graph.
	def add_edge(self, type, start, end, time, weight):
		valid = False
		st = start.type
		et = end.type
		#confirms the edge is a valid type with valid start and end points
		if type == "knows_of"  and st == "noun": valid = True
		elif type == "is_a"    and st == "noun" and et == "noun": valid = True

		elif type == "describes" and st == "relationship": valid = True
		elif type == "has_value" and st == "relationship" and et == "value": valid = True
		elif type == "has_type"  and st == "relationship" and et == "type": valid = True
		elif type == "regarding" and st == "relationship" and et == "noun": valid = True

		elif type == "is_constrained_by" and st == "relationship" and et == "constraint": valid = True
		elif type == "leads_to"  and st == "verb" and et == "verb": valid = True
		elif type == "causes"    and st == "verb" and end == "change": valid = True


		#find existing edge else, add new edge
		#add weight to edge
		new_edge = "not a valid edge"
		if valid: #look and see if the edge already exists
			is_new_edge = True
			new_edge = edge(type)
			for edge_off_start in self.graph.edges_iter([start]): #itterating bad. Fix, fix, fix
				if edge_off_start[0] == start and edge_off_start[1] == end:
					new_edge = get_edge_val(edge_off_start, self.graph)
					is_new_edge = False
					break
			if is_new_edge: #If it doesn't exist, add the edge
				self.graph.add_edge(start, end, {"edge": new_edge})

			new_edge.add_weight(time, weight) # update the edge's weight with this new weight

		return new_edge



	#prints out the whole graph as text
	def print_all(self):
		return self.show_locally()

	#save database to disk
	def save(self, file_name="database_dump.tdb"):
		pickle.dump(self.graph, open(file_name, "w"))
	#load db from disk
	def load(self, file_name="database_dump.tdb"):
		self.graph = pickle.load(open(file_name))





	#fills the graph with a simple sampling
	def override_with_sample(self):
		#createes an ontology and adds some fakie nodes.
		self.graph = nx.Graph()
		english = self.add_node("noun", "")
		self.add_relationship(english, english, "named", "english")
		frank = self.new_noun_named("fred", english)

	def override_with_random_room(self):
		self.graph = nx.Graph()
		english = self.add_node("noun", "")
		self.add_relationship(english, english, "named", "english")

		room = self.new_noun_named("room", english)
		objects_in_room = []

		chair = self.new_noun_named("chair", english) #lots of helper functions for more sprawling graph structures
		objects_in_room.append(chair)

		table = self.new_noun_named("table", english)
		objects_in_room.append(table)


		materials = self.new_nouns_named(["plastic", "wood", "aluminum", "duct tape"], english) #make a node for each material

		self.add_relationship(chair, choice(materials), "is_made_of", "True") #declare we are made of ONE material
		self.add_relationship(table, choice(materials), "is_made_of", "True")



		bed = self.new_noun_named("bed", english)
		objects_in_room.append(bed)
		blanket = self.new_noun_named("blanket", english)
		self.add_relationship(bed, blanket, "has_a", "True")

		#Adds a noun for each color
		#THESE SHOULD BE VALUES, NOT NOUNS@!!!!@!@!@!
		colors = self.new_nouns_named(["burgundy", "violet", "goldenrod", "fuchsia", "lavender", "beige", "azure", "chartreuse", "celadon", "sage", "paisley", "plaid", "tartan", "scarlet"], english) 
		self.add_relationship(blanket, choice(colors), "colored", "True")

		bed_sizes = self.new_nouns_named(["twin", "double", "queen", "king"], english)
		self.add_relationship(bed, choice(bed_sizes), "size", "True")

		floor = self.new_noun_named("floor", english)
		objects_in_room.append(floor)



		cup = self.new_noun_named("cup", english)
		self.add_relationship(choice(objects_in_room), cup, "has_a", "True")
		self.add_relationship(cup, choice(materials), "is_made_of", "True")

		liquids = self.new_nouns_named(["water", "juice", "wine", "soda", "nothing"], english)
		self.add_relationship(cup, choice(liquids), "contains", "True")


		lamp = self.new_noun_named("lamp", english)
		self.add_relationship(choice(objects_in_room), lamp, "has_a", "True")
		power_state = self.new_nouns_named(["on", "off"], english)
		self.add_relationship(lamp, choice(power_state), "is_currently_turned", "True")


		book = self.new_noun_named("book", english)
		self.add_relationship(choice(objects_in_room), book, "has_a", "True")
		book_titles = self.new_nouns_named(["Dreams of Potatoes", "Tequila Sunrise", "The Kraken", "40 Cakes", "Spectral Robot Task Force", "The Vengeful Penguin", "Ninja's Guide to Ornamental Horticulture",
                                                    "Neko-nomicon", "This is Not a Book"], english)
		self.add_relationship(book, choice(book_titles), "titled", "True")




		for object_in_room in objects_in_room:
			self.add_relationship(room, object_in_room,"has_a", "True")















	def show_locally(self):
		for n in self.graph.nodes_iter():
			print(n.id + " " + n.type + " " + n.value)

		for e in self.graph.edges_iter():
			print(str(e[0].id) + " -" + str(get_edge_val(e, self.graph).weights) + "-> " + str(e[1].id))


	def new_nouns_named(self, names, lang):
		nouns = []
		for noun in map( lambda x: self.new_noun_named(x, lang) , names):
			nouns.append(noun)
		return nouns

	def new_noun_named(self, name, lang):
		new_node = self.add_node("noun", "")
		self.add_relationship(new_node, lang, "named", name)
		return new_node

	def pinch(self, pinch_from, time):
		new_noun = self.add_node("noun", "")
		self.add_edge("is_a", new_noun, pinch_from, time, 100)
		return new_noun

	#wraps the process of adding a relationship. Nice.
	def add_relationship(self, src, target, type, value, weight=100, time=1):

		re = self.add_node("relationship", "")
		ty = self.add_node("type", type)
		va = self.add_node("value", value)
		self.add_edge("has_type", re, ty, time, 100)
		self.add_edge("has_value", re, va, time, 100)
		self.add_edge("describes", re, src, time, weight)
		self.add_edge("regarding", re, target, time, 100)
		return re

def get_edge_val(edge_tuple, graph):
	return graph[edge_tuple[0]][edge_tuple[1]]["edge"]

def run():
	ont = ontology()
	ont.override_with_sample()
	#nx.draw(ont.graph)
	#onr.save()
	#ont.load()
	#ont.show_locally()

if __name__ == '__main__':
	run()


