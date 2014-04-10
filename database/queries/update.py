from helpers import query_helper

def fork(search, ontology):

	node_list = query_helper().find_nodes(search.get("target-node"), ontology.graph)

	#make sure we only got one node as a response
	if len(node_list) == 1:
		new_node = [ ontology.fork(node_list[0], search.get("time") ) ]
		return ("fork-success", new_node)
	else:
		return ("fork-failure-wrong-number-of-nodes", [])




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