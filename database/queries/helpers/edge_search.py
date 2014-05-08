import itertools
import pprint
#import matplotlib.pyplot as plt

class edge_search:
    def find_edges(self, lefts, rights, props, graph):
        valid_edges = []

        node_pairs = []
        if props.get("cardinality") == None:
            node_pairs = list(itertools.product(lefts, rights))
        elif props.get("cardinality") == "inbound":
            node_pairs = [(x, y) for x in lefts for y in rights]
        elif props.get("cardinality") == "outbound":
            node_pairs = [(y, x) for x in lefts for y in rights]

        for (left, right) in node_pairs: #itterate each valid pair of nodes
            local_properties = self.edge_properties (left, right, props, graph) #go in and check edge weight up each inherit chain. I'm not liking the look of this.
            if local_properties["weight-value"] != 0:
                valid_edges.append( {"left-node":left,"right-node":right, "properties":local_properties} )

        return valid_edges

    def edge_properties(self, left, right, properties, graph):
        properties["weight-time"] = properties.get("weight-time", 1)
        properties["cardinality"] = "outbound"

        for (left, right) in [(x, y) for x in self.node_and_parents(left, graph) for y in self.node_and_parents(right, graph)]:

            for edge in graph.edges_iter([right]):

                if (edge[0] == left) or (edge[1] == left):

                    edge_obj = graph[edge[0]][edge[1]]["edge"]

                    if self.check_property("type", edge_obj.type, properties) and self.check_property("weight-value", edge_obj.weights.get(properties.get("weight-time"), None), properties): #condition so "if not defiened" will return true as well.

                        properties["type"] = edge_obj.type  #set rest of properties and return properties object
                        properties["weight-value"] = edge_obj.weights.get(properties.get("weight-time"))
                        return properties  #break on first match. We are counting up

        properties["type"] = "none"
        properties["weight-value"] = 0
        return properties


    def node_and_parents(self, node, graph, rest=[]):
        np_list = [node] if rest == [] else rest

        for edge in graph.edges_iter([node]):
            edge_obj = graph[edge[0]][edge[1]]["edge"]
            if edge_obj.type == "is_a" and edge[0].value != "***core-node***": #simple way to keep if from flipping over the top.
                np_list = np_list + (self.node_and_parents(edge[1], graph, np_list))

        return np_list


    #Check if a value is valid. "Valid" means it matches, or wasn't specified
    def check_property(self, prop_name, target_value, query):
        prop_value = query.get(prop_name, None)
        if prop_value is None: #If the value wasn't given, we assume it "could" match.
            return True
        return prop_value == target_value



"""
{"weight-time":search.get("weight-time"),
 "cardinality":search.get("cardinality"),
 "weight-value":search.get("weight-value"),
 "type":search.get("type")}


for edge in graph.edges_iter([node]):

#The object holding the edge's weight
edge_obj = graph[edge[0]][edge[1]]["edge"]
"""
