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
		"time":"FLOAT TIME OF CREATION",
		"target-node": {
						   #GET QUERY THAT RETURNS EXACTLY ONE NOUN TYPE NODE
					   }
	}
"""

