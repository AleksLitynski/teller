class graph_writer:

	#takes a node and returns a json form of it, recursivinly including edges to a certain depth
	def to_json(self, data_to_jsonify, graph, params):
		depth = params.get("depth", 2)

		nodes_to_write = data_to_jsonify
		as_json = []
		for node in nodes_to_write:
			as_json.append(self.node_to_json(node, graph, depth))

		return as_json

	def node_to_json(self, node, graph, depth): #prints a single node as json.
		as_json = {}
		as_json["id"] = node.id
		as_json["type"] = node.type
		as_json["value"] = node.value
		as_json["edges"] = [] #prints it's values

		if depth > 0: #recursivly print the edges

			for edge in graph.edges_iter([node]):
				edge_obj = graph[edge[0]][edge[1]]["edge"] #The object holding the edge's weight
				edge_json = {}
				edge_json["direction"] = "inbound"
				if edge[0] != node:
					print("hey")
					edge_json["direction"] = "outbound"

				edge_json["type"] = edge_obj.type
				edge_json["weight-at-times"] = edge_obj.weights

				edge_json["terminal"] = self.node_to_json(edge[1] if edge[0] is node else edge[0], graph, depth-1)

				as_json["edges"].append(edge_json)




		return as_json
