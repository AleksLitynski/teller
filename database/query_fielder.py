import ontology
import json
import random



class query_fielder:



    #node_prop &&
    def __init__(self):
        pass

    #Takes a query in the format below, devises an answer, and returns a string as a reply.
    def field_query(self, query, ontology):


        query_parsed = json.loads(query) #parse the query into a python structure
        target_graph = ontology.graph


        reply = "no data"

        if query_parsed["type"] == "get": #fills takes your search and sends out a list of fully classified responses
            out = self.find_nodes(query_parsed["search"], target_graph)
            out = self.convert_to_valid_json(out, target_graph, query_parsed["params"])
            reply = json.dumps({"type":"get-success","reply": out})

        elif query_parsed["type"] == "pinch": #Takes a node (later, group of nodes, hence "pinch") and create an "is" of it
            out = self.find_nodes(query_parsed["search"], target_graph)
            if len(out) == 1: #if we got only one node from the search, pinch and return the new node
                new_node = [ontology.pinch(out[0], self.get_property_clean("time", query_parsed["params"], 1) )]
                new_node_as_json = self.convert_to_valid_json(new_node, target_graph, query_parsed["params"])
                reply = json.dumps({"type":"pinch-success","reply": new_node_as_json})
            else:
                reply = json.dumps({"type":"pinch-failure","reply": "wrong number of pinch targets"}) #the search returned too many nodes

        elif query_parsed["type"] == "decide": #use is-a/ranges/edge-weights to decide values of a node
            pass
        elif query_parsed["type"] == "create": #adds totally new content to the graph.
            pass
        else:
            reply = "query type: " + query_parsed["type"] + " not implemented yet"
        return reply


    def convert_to_valid_json(self, data_to_jsonify, graph, params): #takes a node and returns a json form of it, recursivinly including edges to a certain depth
        depth = self.get_property_clean("depth", params, 2)

        nodes_to_write = data_to_jsonify

        as_json = []

        for node in nodes_to_write:
            as_json.append(self.print_node_as_json(node, graph, depth))

        return as_json

    def print_node_as_json(self, node, graph, depth): #prints a single node as json.
        as_json = {}
        as_json["id"] = node.id
        as_json["type"] = node.type
        as_json["value"] = node.value
        as_json["edges"] = [] #prints it's values

        if depth > 0: #recursivly print the edges

            for edge in graph.edges_iter([node]):
                edge_obj = ontology.get_edge_val(edge, graph) #The object holding the edge's weight
                edge_json = {}
                edge_json["direction"] = "inbound" if edge[0] == node else "outbound"
                edge_json["type"] = edge_obj.type
                edge_json["weight-at-times"] = edge_obj.weights

                edge_json["terminal"] = self.print_node_as_json(edge[1] if edge[0] is node else edge[0], graph, depth-1)

                as_json["edges"].append(edge_json)

        return as_json





    def find_nodes(self, query, graph): #creates a list of all nodes that fit the query
        valid_nodes = []
        for node in graph.nodes_iter():     #itterate every node in the graph to find the one we seek.
            #Obviously, this has to get better.
            (is_valid, valid_node) = self.is_valid_node(query, node, graph)
            if is_valid:
                valid_nodes.append(valid_node)


        return valid_nodes



    def is_valid_node(self, query, node, graph): #returns a boolean (valid/invalid) and the node itself.


        #check the properties of the node
        all_good =  self.check_property("id", node.id, query) and \
                    self.check_property("type", node.type, query) and \
                    self.check_property("value", node.value, query)

        if all_good: #check if edge matches edges
            query_edges = self.get_property_clean("edges", query, [])
            for query_edge in query_edges:
                all_good = self.is_valid_edge(query_edge, node, graph) #goes into the edge (recursion will happen in here)
                if not all_good:
                    break

        return (all_good, node)


    #checks if an edge is valid
    def is_valid_edge(self, query, node, graph):

        for edge in graph.edges_iter([node]):
            edge_obj = ontology.get_edge_val(edge, graph) #The object holding the edge's weight
            other_end = edge[0]
            if edge[0] == node: other_end = edge[1] #The end of th edge that is not the node
            #checks the properties of the edges
            edge_ok = self.check_property("type", edge_obj.type, query) and \
                        self.check_property("weight-value", self.get_property_clean(
                                                                self.get_property_clean("weight-time", query),
                                                                edge_obj.weights), query) and \
                        (self.check_property("direction", "inbound", query) and node == edge[0])
            if edge_ok:
                terminal_recurse = self.is_valid_node( self.get_property_clean("terminal", query), other_end, graph) #reursivly check the terminal of the edge
                edge_ok = edge_ok and terminal_recurse[0]

            if edge_ok: return True

        return False



    #These two let me look up values in a dict without crashing python.
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



def run():

    #Creates the fielder
    qf = query_fielder()
    #Creates ontology
    ont = ontology.ontology()
    #Fills ontology with simple sample
    #ont.override_with_sample()
    ont.override_with_random_room()

    #A test get and test pinch query
    get_test_query = '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "fred"}}]}}]}}'
    room_test = '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "room"}}]}}]}}'
    pinch_test_query = '{"type": "pinch", "params": {"depth":2, "time":1}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "fred"}}]}}]}}'
    all_nodes = '{"type":"get", "params":{"depth":1}, "search":{}}'
    print(qf.field_query(all_nodes, ont))



if __name__ == '__main__':
	run()



