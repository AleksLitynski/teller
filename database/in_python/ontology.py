import networkx as nx
import pickle
import uuid

class node:
    def __init__(self, id, node_type, value):
        self.id = id
        self.type = node_type
        self.value = value

class edge:
    def __init__(self, edge_type):
        self.type = edge_type
        self.weights = {}

    #add support for ranges
    #use: http://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-some-value
    def add_weight(self, time, weight):
        self.weights[time] = weight

class ontology:
    def __init__(self):
        self.graph = nx.Graph()
        pass

    def add_node(self, type, value):
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

    def add_edge(self, type, start, end, time, weight):
        valid = False
        st = start.type
        et = end.type
        if type == "knows_of"  and st == "noun": valid = True
        #elif type == "is_a"      and st == "noun" and et == "noun": valid = True

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
        if valid:
            is_new_edge = True
            new_edge = edge(type)
            for edge_off_start in self.graph.edges([start]): #itterating bad. Fix, fix, fix
                if edge_off_start[0] == start and edge_off_start[1] == end:
                    new_edge = get_edge_val(edge_off_start, self.graph)
                    is_new_edge = False
                    break
            if is_new_edge:
                self.graph.add_edge(start, end, {"edge": new_edge})

            new_edge.add_weight(time, weight)

        return new_edge



    #prints out the whole graph.
    def print_all(self):
        return self.show_locally()

    #save database to disk
    def save(self, file_name="database_dump.tdb"):
        pickle.dump(self.graph, open(file_name, "w"))
    #load db from disk
    def load(self, file_name="database_dump.tdb"):
        self.graph = pickle.load(open(file_name))






    def override_with_sample(self):
        #createes an ontology and adds some fakie nodes.
        self.graph = nx.Graph()
        english = self.add_node("noun", "")
        self.add_relationship(english, english, "named", "english")

        "Chair, Table; Material: Plastic, wood, metal"
        chair = self.new_noun_named("chair", english)
        table = self.new_noun_named("table", english)
        plastic = self.new_noun_named("plastic", english)
        wood = self.new_noun_named("wood", english)
        metal = self.new_noun_named("metal", english)
        self.add_relationship(chair, plastic, "is_made_of", "True")
        self.add_relationship(chair, wood, "is_made_of", "True")
        self.add_relationship(chair, metal, "is_made_of", "True")
        self.add_relationship(table, plastic, "is_made_of", "True")
        self.add_relationship(table, wood, "is_made_of", "True")
        self.add_relationship(table, metal, "is_made_of", "True")



        bed = self.new_noun_named("bed", english)
        bed_frame = self.new_noun_named("bed frame", english)
        blanket = self.new_noun_named("blanket", english)
        self.add_relationship(bed, bed_frame, "has_a", "True")
        self.add_relationship(bed, blanket, "has_a", "True")

        colors = self.new_nouns_named(["burgundy", "violet", "goldenrod",
                        "fuchsia", "lavender", "beige", "azure",
                        "chartreuse", "celadon", "sage", "paisley",
                        "plaid", "tartan", "scarlet"], english)

        for color in colors:
            self.add_relationship(blanket, color, "colored", "True")

        bed_sizes = self.new_nouns_named(["twin", "double", "queen", "king"], english)
        for size in bed_sizes:
            self.add_relationship(bed, size, "size", "True")

        frank = self.new_noun_named("fred", english)












    def show_locally(self):
        for n in self.graph.nodes_iter():
            print n.id + " " + n.type + " " + n.value

        for e in self.graph.edges_iter():
            print str(e[0].id) + " -" + str(get_edge_val(e).weights, self.graph) + "-> " + str(e[1].id)


    def new_nouns_named(self, names, lang):
        return map( lambda x: self.new_noun_named(x, lang) , names)
    def new_noun_named(self, name, lang):
        new_node = self.add_node("noun", "")
        self.add_relationship(new_node, lang, "named", name)
        return new_node


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


ont = ontology()
ont.override_with_sample()
#onr.save()
#ont.load()
#ont.show_locally()

"""




Cup
is on: (bed, chair, table, floor)
Material: Plastic, wood, metal, glass, ceramic
Contains: Water, juice, wine, soda, nothing

Lamp
is on: (bed, chair, table, floor)
On/off

Book
is on: (bed, chair, table, floor)
Title:
(Dreams of Potatoes; Tequila Sunrise; The Kraken; 40 Cakes; Spectral Robot Task Force; The Vengeful Penguin; Ninjas Guide to Ornamental Horticulture; Neko-nomicon; This is Not a Book)

"""