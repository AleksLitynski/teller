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
			out = self.convert_to_json(out)
			reply = json.dumps(["reply", out])
		else:
			reply = "query type: " + query_parsed["type"] + " not implimented yet"
		return reply


	def convert_to_json(self, data_to_jsonify):
		return str(data_to_jsonify)





	def find_nodes(self, query, graph):
		valid_nodes = []
		for node in graph.nodes_iter():     #itterate every node in the graph to find the one we seek.
											#Obviously, this has to get better.
			(is_valid, valid_node) = self.is_valid_node(query, node, graph)
			if is_valid:
				valid_nodes.append(valid_node)

		return valid_nodes


	def is_valid_node(self, query, node, graph):
		all_good = True
		if all_good:
			try: all_good = query["id"] == node.id
			except AttributeError: pass
			except KeyError: pass
		if all_good:
			try:  all_good = query["type"] == node.type
			except AttributeError: pass
			except KeyError: pass
		if all_good:
			try: all_good = query["value"] == node.value
			except AttributeError: pass
			except KeyError: pass
		"""
		if all_good:
			for edge in graph.edges_iter([node]):

			   edge_obj = ontology.get_edge_val(edge, graph)

			   if all_good:
				   try:  all_good = query["type"] == edge_obj.type
				   except AttributeError: pass
				   except KeyError: pass
			   if all_good:
				   try:
					   time = query["weight-time"]
					   all_good = query["weight-value"] == edge_obj.weights[time]
				   except AttributeError: pass
				   except KeyError: pass
			   if all_good:
				   try: all_good = (query["direction"] == "inbound" and node == edge[0])
				   except AttributeError: pass
				   except KeyError: pass
			   if all_good:
				   try:
					   other_end = edge[0]
					   if other_end == node: other_end = edge_obj[1]
					   all_good = self.is_valid_node(query["terminal"], other_end, graph)
				   except AttributeError: pass
				   except KeyError: pass

			   if not all_good: break
		"""
		#if node.id == query.search.id
		return (True, node)



qf = query_fielder()
ont = ontology.ontology()
ont.override_with_sample()

test_query = '{"type": "get","search": {"edges": [{"direction": "inbound","type": "described_by","weight-time": "1","terminal": {"type": "adjective","edges": [{"terminal": {"type": "type","value": "name"}},{"terminal": {"type": "value","value": "fred"}}]}}]}}'

print qf.field_query(test_query, ont)







"""
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
				"type": "described_by",
				"weight-time": "1",
				"terminal": {
					"type": "adjective",
					"edges": [
						{
							"terminal": {
								"type": "type",
								"value": "name"
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