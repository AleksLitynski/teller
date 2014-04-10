class node_search:

	#creates a list of nodes from the given graph that match the pattern structure (query)
	def find_nodes(self, query, graph): #creates a list of all nodes that fit the query
		valid_nodes = []
		for node in graph.nodes_iter():     #itterate every node in the graph to find the one we seek.
											#Obviously, this has to get better.
			(is_valid, valid_node) = self.is_valid_node(query, node, graph)
			if is_valid:
				valid_nodes.append(valid_node)

		return valid_nodes


	#returns a boolean (valid/invalid) and the node itself.
	def is_valid_node(self, query, node, graph):
		#check the properties of the node
		all_good =  self.check_property("id", node.id, query) and \
					self.check_property("type", node.type, query) and \
					self.check_property("value", node.value, query)

		#check if edge matches edges
		if all_good:
			query_edges = query.get("edges", [])

			#goes into the edge (recursion will happen in there)
			for query_edge in query_edges:
				all_good = self.is_valid_edge(query_edge, node, graph)
				if not all_good:
					break

		return (all_good, node)


	#checks if an edge is valid
	def is_valid_edge(self, query, node, graph):
		for edge in graph.edges_iter([node]):

			#The object holding the edge's weight
			edge_obj = graph[edge[0]][edge[1]]["edge"]

			#get the object on the other end of the edge
			other_end = edge[0]
			if edge[0] == node: other_end = edge[1]

			#checks the properties of the edges
			edge_ok = self.check_property("type", edge_obj.type, query) and \
						self.check_property("weight-value", edge_obj.weights.get(query.get("weight-time")), query) and \
						(self.check_property("direction", "inbound", query) and node == edge[0])

			#reursivly check the other end of the edge
			if edge_ok:
				terminal_recurse = self.is_valid_node( query.get("terminal"), other_end, graph)
				edge_ok = edge_ok and terminal_recurse[0]

			if edge_ok: return True

		return False



	#Check if a value is valid. "Valid" means it matches, or wasn't specified
	def check_property(self, prop_name, target_value, query):
		prop_value = query.get(prop_name, None)
		if prop_value == None: #If the value wasn't given, we assume it "could" match.
			return True
		return prop_value == target_value
