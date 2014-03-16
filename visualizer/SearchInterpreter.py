import json
import copy
# convert them to nodes for graph
# has [edges, id , value, type]  
# nodes for graph : 
# id : just use given id
# size == how heavy it is; how many connections it has
# x & Y, set them to 0,0, for now 
# label : describe the node here 
# { id,size, x,y, label} sweet
# http://stackoverflow.com/questions/1323410/has-key-or-in
_pos =-1;
def convertToGraphNode(e):
	global _pos
	_pos += 1
	data = copy.deepcopy(e)
	del data['edges']
	return {'id' : e['id'],
			'value' : e['value'],
			'type' : e['type'],
			'data' : data,
			'size': 1,
			'x':(_pos % 20 ) ,'y': int( _pos / 20),
			'label': " Value [ " + str(e['value']) + " & " + str(e['type'])+" ] neighbors : " + str(len(e['edges'] ) )
			}

countEdge = 0;
def convert2Edges(a,b):
	global countEdge;
	countEdge +=1;
	return {'id' : str(countEdge), 'source':a['id'], 'target':b['id']}
def convertEdgeToNode(e): return e['terminal']
def helperAddNode(list,dic, e):
	#if it's new element, add this to list of nodes and dictionary to remember 
	if(not e['id'] in dic):
		list.append(convertToGraphNode(e))
		dic[e['id']] = list[len(list)-1]
		#print "AddNode " +str(e['id'])
	#else:
		#print "AddNode duplicate"
def helperAddEdge(list,dicNodes,dicEdges,edge):
	small = edge[0]; big =edge[1]
	if small['id'] > big['id']: small = edge[1]; big = edge[0]
	
	#print dicNodes[edge[0]['id']]
	for i in range(0,2):
		dicNodes[edge[i]['id']]['size'] += 1 
		if(int(dicNodes[edge[i]['id']]['size']) > 6 ):dicNodes[edge[i]['id']]['size']=6
		
	#print dicNodes[edge[0]['size']]
	list.append(convert2Edges(edge[0],edge[1]) )
	#list.append(convert2Edges(small,big) )
	if not small['id'] in dicEdges:
		dicEdges[small['id']] = [big['id']]
		#print "Edge New : "
	#so this is not new edge to begin with, then is the connection recorded?
	elif not big['id'] in dicEdges[small['id']] :
		#list.append(convert2Edges(small,big) )
		dicEdges[small['id']].append(big['id'])
		#print "Edge added : "
	#else : print "Edge duplicate"
	
	return ""
	
def add(listNodes,listEdges, dicNodes,dicEdges, e):
	#print "Attempting to addNewNode...\nid    : " + str(e['id']) + "\nedges : " + str(len(e['edges']) )
	helperAddNode(listNodes,dicNodes,e);
	edges = e['edges'] #recursively add edge nodes, hopefully no infinite returns 
	for i in  range(0,len(edges) ):
		newNode = edges[i]['terminal']
		add(listNodes,listEdges,dicNodes,dicEdges,newNode);
		helperAddEdge(listEdges,dicNodes,dicEdges,[e,newNode]);
	#raw_input()
	
def read(s):
	global _pos
	_pos = -1
	graphNodes = []
	graphEdges = []
	dicNodes = {} 
	dicEdges = {}
	nodes = json.loads(s)['reply'];
	it = iter(nodes)
	number = 0
	for i in range(0, len(nodes)):
		add(graphNodes,graphEdges,dicNodes,dicEdges,nodes[i])
		
		#print "AT " + str(i)

		
	#it = iter(nodes)
	#while True:
	#	print it.next()
	#	raw_input()
	#print item
	#print "Interpreter loaded : " + nodes
	return {'nodes':graphNodes , 'edges':graphEdges}