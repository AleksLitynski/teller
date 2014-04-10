import node_writer

class edge_writer:

	#takes a node and returns a json form of it, recursivinly including edges to a certain depth
	def to_json(self, data_to_jsonify, graph, params):

		nw = node_writer.node_writer()

		toReturn = []
		for data in data_to_jsonify:

			toReturn.append( {
				"cardinality":data["properties"]["cardinality"],
				"weight-time":data["properties"]["weight-time"],
				"weight-value":data["properties"]["weight-value"],
				"type":data["properties"]["type"],
				"left-node":nw.to_json([data["left-node"]], graph, params)[0],
				"right-node":nw.to_json([data["right-node"]], graph, params)[0]
			})

		return toReturn
