from helpers import query_helper

def get(search, ontology):
	node_list = query_helper().find_nodes(search, ontology.graph)
	return ("get-success", node_list)


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
