import ontology
import json
class query_fielder:

	def __init__(self):
		pass
	#just a stub. Eventually, it could parse a query and do better than a fat dump.
	def field_query(self, query, ontology):
		query = json.loads(query)
		target_graph = ontology.graph

		reply = "no data"
		if query.type == "get":
			reply = json.dumps(["reply", find_nodes(query, target_graph)])
		else:
			reply = "query type: " + query.type + " not implimented yet"
		return reply


	def find_nodes(self, query, graph):
		valid_nodes = []
		for node in graph.nodes():  #itterate every node in the graph to find the one we seek. 
									#Obviously, this has to get better.
			(is_valid, valid_node) = is_valid_node(query, node)
			if is_valid:
				valid_nodes.append(valid_node)

		return valid_nodes


	def is_valid_node(self, query, node):
		#if node.id == query.search.id

		return (False, "")




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

"""

