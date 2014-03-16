import ontology
from query_fielder import *


def test():
    #Creates the fielder
    qf = query_fielder()
    #Creates ontology
    ont = ontology.ontology()
    #Fills ontology with simple sample
    ont.override_with_sample()
    #ont.override_with_random_room()

    #A test get and test fork query
    get_test_query = '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "fred"}}]}}]}}'
    room_test = '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "room"}}]}}]}}'
    fork_test_query = '{"type": "fork", "params": {"depth": 2 },"search": { "time": 1, "target-node": { "edges": [ { "direction": "inbound", "type": "describes", "weight-time": "1", "terminal": { "type": "relationship","edges": [ { "terminal": { "type": "type", "value": "named"}},{ "terminal": { "type": "value", "value": "fred" } }]}}]}}}'
    all_nodes = '{"type":"get", "params":{"depth":1}, "search":{}}'
    gogo_test_o = '{"type": "get","params": {"depth": 0}, "search": {"edges": [{"terminal": {"edges": [ {"terminal": {"type": "type","value": "named"}},{"terminal": { "type": "value","value": "room"}}]}}]}}'
    return qf.field_query(fork_test_query, ont)



if __name__ == '__main__':
	test()



print test()
