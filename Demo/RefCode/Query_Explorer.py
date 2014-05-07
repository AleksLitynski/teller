__author__ = 'Aleksander'
import json
from helpers import *


#Explores queries about nouns
class Query_Explorer:

    def __init__(self, query):
        pass
    def get_noun(self):
        pass



def get_noun(query):
    #we're looking for JSON, but if it isn't, we can fix that
    if type(query) is str:
        query = json.loads(query)

    first_result = query.get("reply")[0]

    new_noun = noun(first_result.get("id"))

    for edge in first_result.get("edges"):
        pipe("terminal",
             [edge.get,
              get_relationship,
              new_noun.relationships.append
            ])


    return new_noun



def get_relationship(query):
    type = get_edge_named(query.get("edges"), "has_type").get("value")
    describes = query.get("edges")[0]["type"]

    value = get_edge_named(query.get("edges"), "has_value").get("value")

    target = get_edge_named(query.get("edges"), "regarding").get("id")

    return relationship(type, describes, value, target)



def get_edge_named(edges, edge_name):
    for edge in edges:
        if edge.get("type") == edge_name:
            return edge.get("terminal")


class noun:

    def __init__(self, id):
        self.id = id
        self.relationships = []

    def get_value(self, relationship_type):
        value = None
        for noun_relationship in self.relationships:
            if noun_relationship.type == relationship_type:
                value = noun_relationship.value
        return value

    def set_value(self, rel_type, val):
        for noun_relationship in self.relationships:
            if noun_relationship.type == rel_type:
                value = val

    def get_all_type(self, relationship_type):
        relationships = []
        for noun_relationship in self.relationships:
            if noun_relationship.type == relationship_type:
                relationships.append(noun_relationship)
        return relationships

    def get_values(self, relationship_type):
        relationships = []
        for noun_relationship in self.relationships:
            if noun_relationship.type == relationship_type:
                relationships.append(noun_relationship.value)
                #print(noun_relationship.describes)
        return relationships

    def get_all(self):
        relationships = []
        for noun_relationship in self.relationships:
            relationships.append(noun_relationship)
        return relationships

    def get_relationship_types(self):
        relationship_types = set()
        for relationships in self.relationships:
            relationship_types.add(relationships.type)
        return relationship_types


    def print_noun(self):
        #Testing self.get_value() -- it works
        #print(self.get_value("named"))
        return self.get_value("named")

class relationship:
    def __init__(self, type, describes, value, regarding):
        self.type = type
        self.value = value
        self.describes = describes
        self.regarding = regarding


"""


def print_reply(to_print):

    re = Query_Explorer.response_explorer()
    name = re.get_node_name(to_print)
    if name is False:
        #or, query on id of node to get it's local name!
        name = "something"
    print name + " has: "
    for has_a in re.get_targets_of(to_print, "has_a"):
        print_reply(has_a)
    relationships = re.terminals_of_edges_named(to_print, "describes")
    return re.get_value_of_relationship_by_type(node, "named")





class response_explorer:
    def __init__(self):
        pass


    def get_node_name(self, node):
        pass

    def get_targets_of(node, rel_type):
        relationships = terminals_of_edges_named(node, "describes")
        targets = []
        for relationship in relationships:
            if relationship is not False:
                type = terminals_of_edges_named(relationship, "has_type")[0]
                reguarding = terminals_of_edges_named(relationship, "regarding")[0]

                type_value = get_property_clean(type, "value", False)
                if (type_value is not False) and (type_value == rel_type):
                    targets.append(reguarding)
        return targets

    def get_value_of_relationship_by_type(self, node, relationship_type):
        relationships = terminals_of_edges_named(node, "describes")
        for relationship in relationships:
            if relationship is not False:
                type = terminals_of_edges_named(relationship, "has_type")[0]
                value = terminals_of_edges_named(relationship, "has_value")[0]


                type_value = get_property_clean(type, "value", False)
                if type_value is not False and type_value == relationship_type:
                    return get_property_clean(value, "value", "")
        return False


    def terminals_of_edges_named(self, node, edge_name):
        terminals = []
        for edge in get_property_clean(node, "edges", []):
            if get_property_clean(edge, "type", False) == edge_name:
                terminals.append(get_property_clean(edge, "terminal", False))
        return terminals

    def get_property_clean(self, query, prop_name, on_fail = False):
        prop_value = on_fail
        try:
            prop_value = query[prop_name]
        except AttributeError: pass
        except KeyError: pass
        return prop_value






"""
