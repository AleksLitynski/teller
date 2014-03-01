import ontology
import json
import random

class query_fielder:



    #node_prop &&
    def __init__(self):
        pass

    #just a stub. Eventually, it could parse a query and do better than a fat dump.
    def field_query(self, query, ontology):

        query_parsed = json.loads(query)
        target_graph = ontology.graph


        reply = "no data"

        if query_parsed["type"] == "get": #fills takes your search and sends out a list of fully classified responses
            out = self.find_nodes(query_parsed["search"], target_graph)
            out = self.convert_to_valid_json(out, target_graph, query_parsed["params"])

            reply = json.dumps({"type":"get-reply","reply": out})
        elif query_parsed["type"] == "pinch": #Takes a node (later, group of nodes, hence "pinch") and create an "is" of it
            pass
        elif query_parsed["type"] == "decide": #given a certain part of the graph, refine the relationships on it. Possably same of different from other types of updates
            pass
        elif query_parsed["type"] == "create": #given a certain part of the graph, refine the relationships on it. Possably same of different from other types of updates
            pass
        else:
            reply = "query type: " + query_parsed["type"] + " not implemented yet"
        return reply


    def convert_to_valid_json(self, data_to_jsonify, graph, params):
        depth = self.get_property_clean("depth", params, 2)

        nodes_to_write = data_to_jsonify

        as_json = []

        for node in nodes_to_write:
            as_json.append(self.print_node_as_json(node, graph, depth))

        return as_json

    def print_node_as_json(self, node, graph, depth):
        as_json = {}
        as_json["id"] = node.id
        as_json["type"] = node.type
        as_json["value"] = node.value
        as_json["edges"] = []

        if depth > 0:

            for edge in graph.edges_iter([node]):
                edge_obj = ontology.get_edge_val(edge, graph) #The object holding the edge's weight
                edge_json = {}
                edge_json["direction"] = "inbound" if edge[0] == node else "outbound"
                edge_json["type"] = edge_obj.type
                edge_json["weight-at-times"] = edge_obj.weights

                edge_json["terminal"] = self.print_node_as_json(edge[1] if edge[0] is node else edge[0], graph, depth-1)

                as_json["edges"].append(edge_json)

        return as_json





    def find_nodes(self, query, graph):
        valid_nodes = []
        for node in graph.nodes_iter():     #itterate every node in the graph to find the one we seek.
            #Obviously, this has to get better.
            (is_valid, valid_node) = self.is_valid_node(query, node, graph)
            if is_valid:
                valid_nodes.append(valid_node)


        return valid_nodes



    def is_valid_node(self, query, node, graph):


        all_good =  self.check_property("id", node.id, query) and \
                    self.check_property("type", node.type, query) and \
                    self.check_property("value", node.value, query)

        if all_good: #check edges
            query_edges = self.get_property_clean("edges", query, [])
            for query_edge in query_edges:
                all_good = self.is_valid_edge(query_edge, node, graph) #This tells us if the edge is good enough
                if not all_good:
                    break

        return (all_good, node)


    def is_valid_edge(self, query, node, graph):

        for edge in graph.edges_iter([node]):
            edge_obj = ontology.get_edge_val(edge, graph) #The object holding the edge's weight
            other_end = edge[0]
            if edge[0] == node: other_end = edge[1] #The end of th edge that is not the node

            edge_ok = self.check_property("type", edge_obj.type, query) and \
                        self.check_property("weight-value", self.get_property_clean(
                                                                self.get_property_clean("weight-time", query),
                                                                edge_obj.weights), query) and \
                        (self.check_property("direction", "inbound", query) and node == edge[0])
            if edge_ok:
                terminal_recurse = self.is_valid_node( self.get_property_clean("terminal", query), other_end, graph)
                edge_ok = edge_ok and terminal_recurse[0]

            #print str(self.get_property_clean("terminal", query)) + " -> " + str(edge_ok)

            if edge_ok: return True

        return False



    def check_property(self, prop_name, target_value, query):
        prop_value = self.get_property_clean(prop_name, query)
        if prop_value == None: #If the value wasn't given, we assume it "could" match.
            return True
        #print str(prop_value) + " == " + str(target_value) + " ==>" + str(prop_value == target_value)
        return prop_value == target_value
    def get_property_clean(self, prop_name, query, on_fail = None):
        prop_value = on_fail
        try:
            prop_value = query[prop_name]
        except AttributeError: pass
        except KeyError: pass
        return prop_value




qf = query_fielder()
ont = ontology.ontology()
ont.override_with_sample()

test_query = '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "fred"}}]}}]}}'

print qf.field_query(test_query, ont)







"""
{"type":"get, "search":{}}
{
    type: "get", #get will return a filled out version of the form.
    edge_depth: 0, #if you want all neighbor info, set to 1, nh of nh, 2, etc
    search: {

        id: "", #uuid of node
        type: "",
        value: "",

        edges: [
            {
                direction: "inbound/outbound",
                type: "",
                weight-time: "",
                weight-value: "",
                terminal: same node description structure. Recursive, edge_depth - 1.
            },
            ...
        ]
    }
}

{
    "type": "get",
    "params": {
        "depth": 2
    },
    "search": {
        "edges": [
            {
                "direction": "inbound",
                "type": "describes",
                "weight-time": "1",
                "terminal": {
                    "type": "relationship",
                    "edges": [
                        {
                            "terminal": {
                                "type": "type",
                                "value": "named"
                            }
                        },
                        {
                            "terminal": {
                                "type": "value",
                                "value": "fred"
                            }
                        }
                    ]
                }
            }
        ]
    }
}





#prints perfectly formatted json. The X, Y, Size should be removed soon.
def to_string(self):
    return "{ " \
    "\"id\": \"n" + str(self.id) + "\"," \
    "\"label\": \"" + str(self.value) + "\"," \
    "\"x\": " + str(random.uniform(0,10)) + "," \
    "\"y\": " + str(random.uniform(0,10)) + "," \
    "\"size\": " + str(3) + "},"


def to_string(self):
    return "{ " \
    "\"id\": \"e" + str(self.id) + "\"," \
    "\"source\": \"n" + str(self.start) + "\"," \
    "\"target\": \"n" + str(self.end) + "\"},"


#prints out the whole graph.
def print_all(self):
    printed = "{ \"nodes\":["
    for node in self.nodes:
        printed = printed + node.to_string()
    printed = printed[:-1] + "], \"edges\": ["
    for edge in self.edges:
        printed = printed + "\n" + edge.to_string()
    printed = printed[:-1] + "]}"
    return printed


for e in graph.edges_iter([valid_node]): #edges to noun
                    for rel_edge in graph.edges_iter(e[1]): #relationship
                        print rel_edge[1].type + " " + rel_edge[1].value
                        pass



"""