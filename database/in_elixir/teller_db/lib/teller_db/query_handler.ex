defmodule teller_query do

	def field_query(graph, query) do
		@doc "the graph is the graph to query against. The query is a string of the query."
		"{ 'nodes':[{ 'id': 'n0','label': 'node zero','x': 5.69739287173,'y': 9.6015066302,'size': 3},{ 'id': 'n1','label': 'node one','x': 9.6072924962,'y': 2.04554255349,'size': 3},{ 'id': 'n2','label': 'node two','x': 5.18513900928,'y': 8.25245814187,'size': 3},{ 'id': 'n3','label': 'node three','x': 7.43236992424,'y': 4.37861356935,'size': 3}], 'edges': [{ 'id': 'e0','source': 'n0','target': 'n1'},{ 'id': 'e1','source': 'n0','target': 'n2'},{ 'id': 'e2','source': 'n0','target': 'n3'},{ 'id': 'e3','source': 'n2','target': 'n3'}]}"
	end

end
