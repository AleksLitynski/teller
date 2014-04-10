from database.queries.helpers import node_writer
from helpers.node_search import node_search


def fork(search, params, ontology):

	node_list = node_search().find_nodes(search.get("target-node"), ontology.graph)

	#make sure we only got one node as a response
	if len(node_list) == 1:
		new_node = [ ontology.fork(node_list[0], search.get("new-value", ""), search.get("time") ) ]
		nw = node_writer.node_writer()
		result_data = nw.to_json(new_node, ontology.graph, params)
		return ("fork-success", result_data)
	else:
		return ("fork-failure-wrong-number-of-nodes", "")




"""
	Valid Query Structure:


	{
		"new-value":"VALUE OF FORKED NODE",
		"time":"FLOAT TIME OF CREATION",
		"target-node": {
						   #GET QUERY THAT RETURNS EXACTLY ONE NOUN TYPE NODE
					   }
	}
"""

