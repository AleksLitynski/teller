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
        greg = self.new_noun_named("greg", english)
        self.add_edge("knows_of", frank, greg, 1, 100)




    def override_with_random_room(self):
        self.graph = nx.Graph()
        english = self.add_node("noun", "")
        self.add_relationship(english, english, "named", "english")

        room = self.new_noun_named("room", english)
        #create string for everything in the room (to be stored in "in_room")
        room_str = "Objects in Room:"

        player = self.new_noun_named("player", english)

        chair = self.new_noun_named("chair", english) #lots of helper functions for more sprawling graph structures
        self.add_relationship(player, chair, "knows_of", "chair")
        #add to string
        room_str += "\n-- chair"

        table = self.new_noun_named("table", english)
        self.add_relationship(player, table, "knows_of", "table")
        room_str += "\n-- table"


        materials = ["plastic", "wood", "aluminum", "duct tape"] #make an attribute for each material
        mat = self.new_noun_named("material", english)
        self.add_relationship(chair, mat, "is_made_of", choice(materials)) #declare we are made of ONE material
        self.add_relationship(table, mat, "is_made_of", choice(materials))

        bed = self.new_noun_named("bed", english)
        self.add_relationship(player, bed, "knows_of", "bed")
        room_str += "\n-- bed"
                

        blanket = self.new_noun_named("blanket", english)
        self.add_relationship(bed, blanket, "has_a", "blanket")
        self.add_relationship(blanket, bed, "had_by", "bed")
        room_str += "\n-- blanket"

        #Values for each color
        colors = ["burgundy", "violet", "goldenrod", "fuchsia", "lavender", "beige", "azure", "chartreuse", "celadon", "sage", "paisley", "plaid", "tartan", "scarlet"]
        rgb_color = self.new_noun_named("rgb color", english)
        self.add_relationship(blanket, rgb_color, "colored", choice(colors))

        bed_sizes = ["twin", "double", "queen", "king"]
        bed_size = self.new_noun_named("bed_size", english)
        self.add_relationship(bed, bed_size, "bed_size", choice(bed_sizes))


        floor = self.new_noun_named("floor", english)
        self.add_relationship(player, floor, "knows_of", "floor")
        #objects_in_room.append(floor)
        room_str += "\n-- floor"

        floor_mats = ["hardwood", "linoleum", "concrete", "marble", "carpeted"]
        floor_mat = self.new_noun_named("floor_mat", english)
        self.add_relationship(floor, floor_mat, "floor_mat", choice(floor_mats))

        cup = self.new_noun_named("cup", english)
        self.add_relationship(cup, mat, "is_made_of", choice(materials))
        self.add_relationship(table, cup, "has_a", "cup")
        self.add_relationship(cup, table, "had_by", "table")
        room_str += "\n-- cup"


        liquids = ["water", "juice", "wine", "soda", "nothing"]
        contents = self.new_noun_named("contents", english)
        self.add_relationship(cup, contents, "contains", choice(liquids))


        lamp = self.new_noun_named("lamp", english)
        self.add_relationship(table, lamp, "has_a", "lamp")
        self.add_relationship(lamp, table, "had_by", "table")
        power_state = ["on", "off"]
        p_state = self.new_noun_named("on/off", english)
        self.add_relationship(lamp, p_state, "power_state", choice(power_state))
        room_str += "\n-- lamp"

        book = self.new_noun_named("book", english)
        self.add_relationship(table, book, "has_a", "book")
        self.add_relationship(book, table, "had_by", "table")
        book_titles = ["Dreams of Potatoes", "Tequila Sunrise", "The Kraken", "40 Cakes", "Spectral Robot Task Force", "The Vengeful Penguin", "Ninja's Guide to Ornamental Horticulture",
                "Neko-nomicon", "This is Not a Book"]
        title = self.new_noun_named("title", english)
        self.add_relationship(book, title, "titled", choice(book_titles))
        room_str += "\n-- book"

        #Does it work with one big string? -- it does
        in_room = self.new_noun_named("in_room", english)
        self.add_relationship(room, in_room, "in_room", room_str)


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

    def fork(self, fork_from, name, time):
        new_noun = self.add_node(fork_from.type, name)
        self.add_edge("is_a", new_noun, fork_from, time, 100)
        return new_noun

    #def discover(self, on, ):

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


