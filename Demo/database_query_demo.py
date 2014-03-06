#needed for user input
import socket
import json
import Query_Explorer
from helpers import *


def query(query_string):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5005))
    s.send(query_string)
    query_response = s.recv(10000) #our replies are VERY long. GOTTA fix that. At least, don't recurse into nodes that already exist
    s.close()
    return query_response

def describe_noun(noun_name, depth=2):
	#broke up the return into 2 lines to make it more readable
    return '{"type": "get", "params": {"depth":'+str(depth)+'}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1",' +
	'"terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "'+noun_name+'"}}]}}]}}'

def get_node(node_id, depth=2):
    return '{"type": "get", ' \
           '"params": {"depth":'+str(depth)+'}, ' \
                                            '"search": {"id":"'+node_id+'"}}'


def translate_type(type):
    return type




def get_noun_by_name(name, noun_table):
    if name in noun_table:
        query_string = describe_noun(name, 2)

        noun = Query_Explorer.get_noun(json.loads(query(query_string)))
        noun = pipe(query_string, [
            query,
            json.loads,
            Query_Explorer.get_noun
        ])


        return noun
    return Query_Explorer.noun()




#input() gets input from console!!
if __name__ == '__main__':
    noun_table = ["room"]
    room = get_noun_by_name("room", noun_table)

    usr_input = ""
    while input != "quit":
        print input()
        if any(noun in usr_input.split(" ") for noun in noun_table):
            print noun


    """
    relationships = {}
    for relationship_type in room.get_relationship_types():
        relationships[relationship_type] = []
        for rel in room.get_all(relationship_type):
            relationships[relationship_type].append(rel.reguarding)
    """




