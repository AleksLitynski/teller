import ontology
import json
import random

class query_fielder:

    def __init__(self):
        pass

    #just a stub. Eventually, it could parse a query and do better than a fat dump.
    def field_query(self, query, ontology):

        query_parsed = json.loads(query)
        target_graph = ontology.graph


        reply = "no data"

        if query_parsed["type"] == "get":
            out = self.find_nodes(query_parsed["search"], target_graph)
            out = self.convert_to_json(out, target_graph)
            reply = json.dumps(["reply", out])
        else:
            reply = "query type: " + query_parsed["type"] + " not implimented yet"
        return reply


    def convert_to_json(self, data_to_jsonify, graph):
        return str(data_to_jsonify)





    def find_nodes(self, query, graph):
        valid_nodes = []
        for node in graph.nodes_iter():     #itterate every node in the graph to find the one we seek.
                                            #Obviously, this has to get better.
            (is_valid, valid_node, cause) = self.is_valid_node(query, node, graph)


            if is_valid:

                for e in graph.edges_iter([valid_node]): #edges to noun
                    for rel_edge in graph.edges_iter(e[1]): #relationship
                        print rel_edge[1].type + " " + rel_edge[1].value
                        pass
                valid_nodes.append(valid_node)
            else:
                print "failed because: " + cause
            print "-----------------------------------"

        return valid_nodes



    def check_property(self, prop_name, target_value, query):
        prop_value = None
        try:
            prop_value = query["prop_name"]
        except AttributeError: pass
        except KeyError: pass
        if prop_value == None: #If the value wasn't given, we assume it "could" match.
            return True
        return prop_value == target_value


    #node_prop &&
    def is_valid_node(self, query, node, graph):
        name = ""
        #print node.type + " <" + node.value + ">"
        all_good =  self.check_property("id", node.id, query) and self.check_property("type", node.type, query) and self.check_property("value", node.value, query)

        reason_for_failure = "passed"

        if all_good:
            query_edges = []
            try: query_edges = query["edges"]
            except AttributeError: pass
            except KeyError: pass

            all_edges_ok = True
            for query_edge in query_edges:
                query_edge_ok = True
                for edge in graph.edges_iter([node]):
                    edge_ok = True
                    edge_obj = ontology.get_edge_val(edge, graph)

                    if edge_ok:
                        try:
                            edge_ok = query_edge["type"] == edge_obj.type
                            if not edge_ok: reason_for_failure = "edge type"
                        except AttributeError: pass
                        except KeyError: pass

                    if edge_ok:
                        try:
                            edge_ok = query_edge["weight-value"] == edge_obj.weights[query_edge["weight-time"]]
                            if not edge_ok: reason_for_failure = "edge weight"
                        except AttributeError: pass
                        except KeyError: pass

                    if edge_ok:
                        try:
                            edge_ok = (query_edge["direction"] == "inbound" and node == edge[0])
                            if not edge_ok: reason_for_failure = "edge cardinality"
                        except AttributeError: pass
                        except KeyError: pass

                    if edge_ok:
                        other_end = edge[0]
                        if other_end == node: other_end = edge[1]
                        #print str(edge[0].type) + ", " + str(edge[1].type) + ", " + str(other_end.type)
                        try:
                            (passed, node_checked, cause) = self.is_valid_node(query_edge["terminal"], other_end, graph) #we aren't doing both permutations of edges. IE: If we hit value first, we don't try type next
                            edge_ok = passed
                            if not edge_ok: reason_for_failure = "terminal recursion via: " + cause
                        except AttributeError: pass
                        except KeyError: pass
                    query_edge_ok = query_edge_ok and edge_ok
                    if not edge_ok: break
                all_edges_ok = all_edges_ok and query_edge_ok


            all_good = all_edges_ok


        #if node.id == query.search.id
        return (all_good, node, reason_for_failure)



qf = query_fielder()
ont = ontology.ontology()
ont.override_with_sample()

test_query = '{"type": "get","search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "fred"}}]}}]}}'

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






"""