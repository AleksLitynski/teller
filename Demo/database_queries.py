import re
import socket
import subprocess
import threading
import time

import json

def is_string_id(string):
    return len(string) == 36


class node_named:
    def __init__(self, named, english):
        self.name = named
        self.english = english

    def named(self, name):
        it = fork_core_node("noun")
        add_property(it, self.name, name, self.english)
        return it

    def from_named(self, name, parent):
        it = fork_node(parent)
        add_property(it, self.name, name, self.english)
        return it


def fork_core_node(_type, value=""):
    query_result = query({
                                    "type": "fork",
                                    "params":{"depth":1},
                                    "search":{
                                              "new-value":value,
                                              "time": 1,
                                              "target-node": {
                                                              "type": _type,
                                                              "value":"***core-node***"}}})

    return query_result["reply"][0]["id"]

def fork_node(_id, value=""):
    query_result = query({
                                    "type": "fork",
                                    "params":{"depth":1},
                                    "search":{
                                              "new-value":value,
                                              "time": 1,
                                              "target-node": {"id":_id}}})

    return query_result["reply"][0]["id"]

def add_property(from_id, _type, value, noun_id):

    relationship_id = fork_core_node("relationship")

    type_id = _type
    if not is_string_id(_type):
        type_id = fork_core_node("type", _type)
    value_id = value
    if not is_string_id(value):
        value_id = fork_core_node("value", value)


    update_edge_between(relationship_id, value_id, "has_value")
    update_edge_between(relationship_id, type_id, "has_type")

    update_edge_between(relationship_id, from_id, "describes")
    update_edge_between(relationship_id, noun_id, "reguarding")



#Two ide's and an optional weight for extending edges. Still debugging this function
def update_edge_between(left_id, right_id, _type, weight=100):
    query_result = query({
                                    "type": "update",
                                    "params":{"depth":1},
                                    "search":{
                                              "weight":weight,
                                              "weight-time": 1,
                                              "type":_type,
                                              "left-node": { "id":left_id },
                                              "right-node": {"id":right_id}}} )
    print query_result

def query(query_obj):
    query_string = query_obj
    if type(query_obj) is not str:
        query_string = json.dumps(query_obj)


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', 5005))
    except:
        t = threading.Thread(target=lambda: subprocess.call(["python", "../../database/main.py"]))
        t.start()
        has_started = False
        while not has_started:
            try:
                s.connect(('127.0.0.1', 5005))
                time.sleep(1)
                has_started = True
            except:
                pass

    s.send(query_string)            #This fails on a bad query?
    query_response = s.recv(10000) #our replies are VERY long. don't recurse into nodes that already exist?
    s.close()


    return json.loads(query_response)

