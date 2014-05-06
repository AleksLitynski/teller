from helpers.node_search import node_search
from helpers.edge_search import edge_search
from helpers.edge_writer import edge_writer

def update(search, params, ontology):

	left_node_list =  node_search().find_nodes(search.get("left-node"),  ontology.graph)
	right_node_list = node_search().find_nodes(search.get("right-node"), ontology.graph)

	es = edge_search()
	valid_edges = es.find_edges(left_node_list, right_node_list,
					{"weight-time":search.get("weight-time"),
					"cardinality":search.get("cardinality"),
					"weight-value":None,
					"type":search.get("type")}, ontology.graph)


	if len(valid_edges) == 1:

		edge_obj = ontology.graph[valid_edges[0]["left-node"]][valid_edges[0]["right-node"]]["edge"]
		edge_obj.weights[search.get("weight-time")] = search.get("weight-value")

		valid_edges = es.find_edges(left_node_list, right_node_list,
									{"weight-time":search.get("weight-time"),
									 "cardinality":search.get("cardinality"),
									 "weight-value":search.get("weight-value"),
									 "type":search.get("type")}, ontology.graph)
		ew = edge_writer()
		edgeson = ew.to_json(valid_edges, ontology.graph, params)
		return ("update-success", edgeson)

	else:
		return ("update-failure-argument-count", [])




"""
	Valid Query Structure:

	#LEFT AND RIGHT MUST MATCH ONLY ONE PATTERN EACH
	{
		"time":"EDGE TIME",
		"weight":"NEW EDGE WEIGHT"
		"left-node": {
						   #A "GET" QUERY FOR THE PATTERN ON THE LEFT OF THE EDGE
					 },
		"right-node": {
						   #A "GET" QUERY FOR THE PATTERN ON THE RIGHT OF THE EDGE
					  }
	}
"""