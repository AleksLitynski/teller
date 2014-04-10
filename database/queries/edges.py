from helpers.node_search import node_search
from helpers.edge_search import edge_search
from helpers.edge_writer import edge_writer

def edges(search, params, ontology):

	left_node_list =  node_search().find_nodes(search.get("left-node"),  ontology.graph)
	right_node_list = node_search().find_nodes(search.get("right-node"), ontology.graph)

	es = edge_search()
	valid_edges = es.find_edges(left_node_list, right_node_list, {"weight-time":search.get("weight-time"),
															 "cardinality":search.get("cardinality"),
															 "weight-value":search.get("weight-value"),
															 "type":search.get("type")}, ontology.graph)

	ew = edge_writer()
	edgeson = ew.to_json(valid_edges, ontology.graph, params)

	return ("edges-success", edgeson)



"""
	Valid Query Structure:


	{
		"time":"EDGE TIME",
		"left-node": {
						   #A "GET" QUERY FOR THE PATTERN ON THE LEFT OF THE EDGE
					 },
		"right-node": {
						   #A "GET" QUERY FOR THE PATTERN ON THE RIGHT OF THE EDGE
					  }
	}
"""



"""
1) target (describe a node that we will create a new connection on
2) desired new node

3) new weight/time



If a node doesn't have a property, we can find one in it's is_a chain that fits a description
This function



option = (edge weight + time) between pattern A to pattern B

New queries:
1) List options (A, B, time) <- edges
2) Update option (A, B, new-val, time) <- update
3) Normalize option (list of desired options, unchanged options, and removed options, sort of vague still)
"""