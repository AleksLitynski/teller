import json
import queries
from graph_writer import *


class query_fielder:
	#Takes a query in the format below, devises an answer, and returns a string as a reply.
	def field_query(self, query, ontology):

		#parse the query into a python structure
		query_parsed = json.loads(query)

		#default query response is not impimented error
		reply = ("query-not-implimented", [])

		#load the query handler specified in the type
		query_module = getattr(queries, query_parsed.get("type"), None)
		querier = getattr(query_module, query_parsed.get("type"), None)

		#If there was a valid handler, run the query
		if querier != None: reply = querier(query_parsed.get("search"), ontology)


		#Take the graph node that was returned and convert it to a structure
		result_data = graph_writer().to_json(reply[1], ontology.graph, query_parsed["params"])

		#convert strucuture to json string
		return json.dumps({"type": reply[0],"reply": result_data})





"""
Query Structure:

	{
		"type":"NAME OF A FILE IN QUERIES FOLDER",
		"params": {
					  "depth":"INTIGER DEPTH TO EXPLORE EACH SUBEDGE/TERMINAL"
				  },
		"search": {
					  #STRUCTURE WILL BE PASSED TO SPECIFIED QUERY
				  }

	}


"""
