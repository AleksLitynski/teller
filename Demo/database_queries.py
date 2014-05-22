import re
import time
import json
import random
from roombuilder.helper import *
from RefCode.Query_Explorer import *


#====database talk==============
#query() moved to helper


#Give node a name and a depth; 2 is default, and higher is said to cause issues
def describe_noun(noun_name, depth=2):
    #the only thing that really changes is name, the rest are defaults
    txt = '{"type": "get", "params": {"depth":'+str(depth)+'}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1",' +\
           '"terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "'+noun_name+'"}}]}}]}}'
    return txt

#searches in the database for a node with a certain id
#to a certain depth (todo: describe consequences)
def get_node(node_id, depth=2):
    return '{"type": "get", ' \
           '"params": {"depth":'+str(depth)+'}, ' \
           '"search": {"id":"'+node_id+'"}}'


#uses queries to get the node based on its name
def get_node_by_name(name):
    #get the JSON for the node
    query_string = describe_noun(name, 1)
    print (query_string)
    #ask the database using it
    q = query(query_string)
    noun = get_noun(q)

    return noun

#gets the node by its name, and then filters it based
#on whether the player would know it exists.
def get_known_node(name):
    noun = get_node_by_name(name)
    return noun
    if noun:
        if len(noun.get_all_type("knows_of"))>0:
            return noun
    return None



#returns the ID of the node that connotes the english language
def english():
    query_result = query(json.dumps({
        "type":"get",
        "params": {"depth":-1},
        "search":{"type":"noun",
            "edges":[
                {"terminal":{"type":"relationship",
                    "edges":[
                        {"terminal":{"type":"type", "value":"named"}},
                        {"terminal":{"type":"value","value":"english"}}
        ]}}]}}))

    return query_result["reply"][0]["id"]



def new_noun():
	return fork_core_node("noun")


#add a property to a noun (property == type+value+target_noun)
#from_id is your starting noun
#type is the property's type (ie: named or has_a)
#value is it's value (ie: frank or true)
#noun_id is the noun it reguard. For words, it should be a language. See "english()" function
def add_property(from_id, _type, value, noun_id):

    relationship_id = fork_core_node("relationship")
    value_id = fork_core_node("value", value)
    type_id = fork_core_node("type", _type)


    update_edge_between(relationship_id, value_id, "has_value")
    update_edge_between(relationship_id, type_id, "has_type")

    update_edge_between(relationship_id, from_id, "describes")
    update_edge_between(relationship_id, noun_id, "reguarding")


#Two ID's and an optional weight for extending edges. Still debugging this function
def update_edge_between(left_id, right_id, _type, weight=100):
    query_result = query(json.dumps({
        "type": "update",
        "params":{"depth":1},
        "search":{
            "weight":weight,
            "time": 1,
            "type":_type,
            "left-node": { "id":left_id },
            "right-node": {"id":right_id}}}))


#========database talk end========================
#=======Joe's creation code start==========================

#creates a node with set parameters, takes a name, lists of attributes and values, and whether or not you want it to print
def devCreateSet(name, attList=None, valList=None, displayInfo=None, known=None):
    #set up the name
    temp_noun = new_noun()
    add_property(temp_noun, "named", name, english())
    
    #Player knows about this
    if known:
         
        pl = get_node_by_name("player")
        add_property(pl.get_value("id"), "knows_of", name, english())
        
        #AttributeError: 'unicode' object has no attribute 'get_value'
        update_edge_between(pl.get_value("id"), temp_noun, "knows_of", 100)
        print(pl.get_value("knows_of"))
    
    #only print things if displayInfo is set to something
    if displayInfo:
        print(name)
    
    #set iterator to 0
    iterator = 0 
    #only add attributes if there is one
    if len(attList) > 0:
        #add a new attribute and corresponding value
        for att in attList:
            add_property(temp_noun, attList[iterator], valList[iterator], english())
            
            if displayInfo:
                print(attList[iterator] + ": " + valList[iterator])     #proves that attList[iterator] and valList[iterator] are working
            
            iterator += 1
            
    #return the new noun
    return temp_noun
    
#Name of value; dictionary of attributes (keys), each of which contains a list of potential values; and whether or not you want it to print
def devCreateRandom(name, attDict=None, displayInfo=None, known=None):
    
    temp_noun = new_noun()
    add_property(temp_noun, "named", name, english())
    #print(temp_noun)
    
    if known:
        pl = get_node_by_name("player")
        add_property(pl.get_value("id"), "knows_of", name, english())
        
        #AttributeError: 'unicode' object has no attribute 'get_value'
        update_edge_between(pl.get_value("id"), temp_noun, "knows_of", 100)
        #print(pl.get_value("knows_of"))
    
    if displayInfo:
        print(name)
        
    #set iterator to 0
    iterator = 0 
    #don't do this if the dictionary is empty
    if len(attDict) > 0:
        #add a new attribute and corresponding value
        for att in attDict:
            
            #get random number from 0 to length of list inside dictionary
            tempRand = random.randrange(0, len(attDict[attDict.keys()[iterator]]))
            #set temporary value to a random value from each list (all of which are keys), in order
            tempVal = attDict[attDict.keys()[iterator]][tempRand]
            
            add_property(temp_noun, attDict.keys()[iterator], tempVal, english())
            
            if displayInfo:
                print(attDict.keys()[iterator] + ": " + tempVal)     #proves that attList[iterator] and valList[iterator] are working
            iterator += 1
            
    #return the new noun
    return temp_noun

