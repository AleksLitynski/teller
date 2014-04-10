import ontology
from query_fielder import *


def test_query(ont, test_query, correct_output):
	qf = query_fielder()

	dear_god = qf.field_query(test_query, ont)
	#print dear_god
	#print len(dear_god)
	#print len(correct_output)

	return len(correct_output) == len(dear_god)


def test():
	#Creates ontology
	ont = ontology.ontology()
	#Fills ontology with simple sample
	ont.override_with_sample()

	print "get test: " + str(test_query(ont,
							 '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "fred"}}]}}]}}',
							 '{"reply": [{"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "type", "id": "d06ea435-beca-11e3-b982-0c8bfd663964", "value": "named"}, "direction": "inbound", "type": "has_type"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "d06e7d21-beca-11e3-93c3-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "regarding"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "value", "id": "d06ea436-beca-11e3-a049-0c8bfd663964", "value": "fred"}, "direction": "inbound", "type": "has_value"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "d06ea433-beca-11e3-bbd5-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "relationship", "id": "d06ea434-beca-11e3-ac0e-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "relationship", "id": "d06ea438-beca-11e3-b881-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "d06ea433-beca-11e3-bbd5-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}], "type": "noun", "id": "d06ea437-beca-11e3-a934-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}], "type": "noun", "id": "d06ea433-beca-11e3-bbd5-0c8bfd663964", "value": ""}], "type": "get-success"}'))


	ont.override_with_sample()
	print "fork test: " + str(test_query(ont,
							 '{"type": "fork", "params": {"depth": 2 },"search": { "time": 1, "new-value":"mini fred", "target-node": { "edges": [ { "direction": "inbound", "type": "describes", "weight-time": "1", "terminal": { "type": "relationship","edges": [ { "terminal": { "type": "type", "value": "named"}},{ "terminal": { "type": "value", "value": "fred" } }]}}]}}}',
							 '{"reply": [{"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "d06f6784-beca-11e3-b3f9-0c8bfd663964", "value": "mini fred"}, "direction": "inbound", "type": "is_a"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "d06f6780-beca-11e3-8b58-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "relationship", "id": "d06f4073-beca-11e3-8b84-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "d06f4072-beca-11e3-9737-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "is_a"}], "type": "noun", "id": "d06f6784-beca-11e3-b3f9-0c8bfd663964", "value": "mini fred"}], "type": "fork-success"}'))


	ont.override_with_sample()
	print "edge test: " + str(test_query(ont,
							 '{"params": {"depth": 2}, "search": {"weight-time": 1, "right-node": {"edges": [{"terminal": {"edges": [{"terminal": {"type": "type", "value": "named"}}, {"terminal": {"type": "value", "value": "greg"}}], "type": "relationship"}, "weight-time": "1", "direction": "inbound", "type": "describes"}]}, "left-node": {"edges": [{"terminal": {"edges": [{"terminal": {"type": "type", "value": "named"}}, {"terminal": {"type": "value", "value": "fred"}}], "type": "relationship"}, "weight-time": "1", "direction": "inbound", "type": "describes"}]}}, "type": "edges"}',
							 '{"reply": [{"left-node": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "28cd4f43-bec7-11e3-9f59-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "relationship", "id": "28cd7651-bec7-11e3-a957-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "28cd4f47-bec7-11e3-9556-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "28cd4f43-bec7-11e3-9f59-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "type", "id": "28cd4f45-bec7-11e3-a3dd-0c8bfd663964", "value": "named"}, "direction": "inbound", "type": "has_type"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "value", "id": "28cd4f46-bec7-11e3-a362-0c8bfd663964", "value": "fred"}, "direction": "inbound", "type": "has_value"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "28cd2830-bec7-11e3-9c44-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "regarding"}], "type": "relationship", "id": "28cd4f44-bec7-11e3-a284-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "28cd4f43-bec7-11e3-9f59-0c8bfd663964", "value": ""}, "weight-value": 100, "weight-time": 1, "cardinality": "outbound", "type": "knows_of", "right-node": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "28cd4f47-bec7-11e3-9556-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "relationship", "id": "28cd4f44-bec7-11e3-a284-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "28cd4f43-bec7-11e3-9f59-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "28cd4f47-bec7-11e3-9556-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "type", "id": "28cd7652-bec7-11e3-a308-0c8bfd663964", "value": "named"}, "direction": "inbound", "type": "has_type"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "value", "id": "28cd7653-bec7-11e3-a110-0c8bfd663964", "value": "greg"}, "direction": "inbound", "type": "has_value"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "28cd2830-bec7-11e3-9c44-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "regarding"}], "type": "relationship", "id": "28cd7651-bec7-11e3-a957-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "28cd4f47-bec7-11e3-9556-0c8bfd663964", "value": ""}}], "type": "edges-success"}') )


	ont.override_with_sample()
	print "update test: " + str(test_query(ont,
						   '{"params": {"depth": 2}, "search": {"weight-value": 5, "weight-time": 1, "right-node": {"edges": [{"terminal": {"edges": [{"terminal": {"type": "type", "value": "named"}}, {"terminal": {"type": "value", "value": "greg"}}], "type": "relationship"}, "weight-time": "1", "direction": "inbound", "type": "describes"}]}, "left-node": {"edges": [{"terminal": {"edges": [{"terminal": {"type": "type", "value": "named"}}, {"terminal": {"type": "value", "value": "fred"}}], "type": "relationship"}, "weight-time": "1", "direction": "inbound", "type": "describes"}]}}, "type": "update"}',
						   '{"reply": [{"left-node": {"edges": [{"weight-at-times": {"1": 5}, "terminal": {"edges": [{"weight-at-times": {"1": 5}, "terminal": {"edges": [], "type": "noun", "id": "bcb94b43-becd-11e3-a515-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "relationship", "id": "bcb97250-becd-11e3-8b3b-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "bcb9724f-becd-11e3-aa06-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "type", "id": "bcb94b45-becd-11e3-9875-0c8bfd663964", "value": "named"}, "direction": "inbound", "type": "has_type"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "value", "id": "bcb94b46-becd-11e3-866e-0c8bfd663964", "value": "fred"}, "direction": "inbound", "type": "has_value"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "bcb94b43-becd-11e3-a515-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "bcb92430-becd-11e3-a2bc-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "regarding"}], "type": "relationship", "id": "bcb94b44-becd-11e3-a5a4-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "bcb94b43-becd-11e3-a515-0c8bfd663964", "value": ""}, "weight-value": 5, "weight-time": 1, "cardinality": "outbound", "type": "knows_of", "right-node": {"edges": [{"weight-at-times": {"1": 5}, "terminal": {"edges": [{"weight-at-times": {"1": 5}, "terminal": {"edges": [], "type": "noun", "id": "bcb9724f-becd-11e3-aa06-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "relationship", "id": "bcb94b44-becd-11e3-a5a4-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "bcb94b43-becd-11e3-a515-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "knows_of"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [{"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "type", "id": "bcb97251-becd-11e3-a36f-0c8bfd663964", "value": "named"}, "direction": "inbound", "type": "has_type"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "value", "id": "bcb97252-becd-11e3-9010-0c8bfd663964", "value": "greg"}, "direction": "inbound", "type": "has_value"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "bcb9724f-becd-11e3-aa06-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}, {"weight-at-times": {"1": 100}, "terminal": {"edges": [], "type": "noun", "id": "bcb92430-becd-11e3-a2bc-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "regarding"}], "type": "relationship", "id": "bcb97250-becd-11e3-8b3b-0c8bfd663964", "value": ""}, "direction": "inbound", "type": "describes"}], "type": "noun", "id": "bcb9724f-becd-11e3-aa06-0c8bfd663964", "value": ""}}], "type": "update-success"}') )





def other_test():
	#ont.override_with_random_room()

	#A test get and test fork query
	room_test = '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "room"}}]}}]}}'
	all_nodes = '{"type":"get", "params":{"depth":1}, "search":{}}'
	gogo_test_o = '{"type": "get","params": {"depth": 0}, "search": {"edges": [{"terminal": {"edges": [ {"terminal": {"type": "type","value": "named"}},{"terminal": { "type": "value","value": "room"}}]}}]}}'

def test_tester():
	ont = ontology.ontology()
	#Fills ontology with simple sample
	ont.override_with_sample()

	qt = 	json.dumps({
				"type": "update",
				"params":
				{
					"depth": 2
				},
				"search":
				{
					"weight-time":1,
					#"cardinality":"inbound",
					"weight-value":5,
					#"type":"knows",
					"left-node":
					{
						"edges":
						[{
								"direction": "inbound",
								"type":"describes",
								"weight-time":"1",
								"terminal":
								{
									"type":"relationship",
									"edges":
									[{
											"terminal":
											{
												"type":"type",
												"value":"named"
											}},{
											"terminal":
											{
												"type":"value",
												"value":"fred"
											}}]}}]},
				"right-node":
				{
				"edges":
					[{
						"direction": "inbound",
						"type":"describes",
						"weight-time":"1",
						"terminal":
							{
							"type":"relationship",
							"edges":
								[{
									"terminal":
										{
										"type":"type",
										"value":"named"
										}},{
									"terminal":
										{
										"type":"value",
										"value":"greg"
										}
									}]}}]}}})

	qf = query_fielder()
	print qt
	#print qf.field_query(qt, ont)


if __name__ == '__main__':
	#test_tester()
	test()