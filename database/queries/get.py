from database.queries.helpers import node_writer
from helpers.node_search import node_search


def get(search, params, ontology):
	node_list = node_search().find_nodes(search, ontology.graph)

	nw = node_writer.node_writer()
	result_data = nw.to_json(node_list, ontology.graph, params)
	return ("get-success", result_data)


"""
Valid Query Structure:


{
	"id":"ID OF TARGET NODE(S)",
	"type":"TYPE OF TARGET NODE(S)",
	"value":"VALUE OF TARGET NODES(S)",
	"edges":[ #LIST OF ALL EDGES CONNECTED TO NODE
				{
					"cardinality":"inbound OR outbound",
					"weight-time":"TIME TIME THE WEIGHT VALUE WILL BE LOOKED UP AT",
					"weight-value":"THE VALUE OF THE EDGEWEIGHT AT WEIGHT-TIME",
					"terminal": {} #A RECURSIVE SEARCH OF (GET) TYPE
				}
			]
}


"""
