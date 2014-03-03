import json

# convert them to nodes for graph
# has [edges, id , value, type]  
# nodes for graph : 
# id : just use given id
# size == how heavy it is; how many connections it has
# x & Y, set them to 0,0, for now 
# label : describe the node here 
# { id,size, x,y, label} sweet
# http://stackoverflow.com/questions/1323410/has-key-or-in
_pos =0;
def convertToGraphNode(e):
	global _pos
	_pos += 1
	return {'id' : e['id'], 
			'size':3+ len(e['edges']),
			'x':(_pos % 20 ) *3,'y': int( _pos / 20) *3 ,
			'label': "Value : " + str(e['value']) + " Label : " + str(e['value'])}
def convertEdgeToNode(e): return e['terminal']
def helperAddNode(list,dic, e):
	#if it's new element, add this to list of nodes and dictionary to remember 
	if(not e['id'] in dic):
		list.append(convertToGraphNode(e))
		dic[e['id']] = list[len(list)-1]
		print "AddNode " +str(e['id'])
	else:
		print "AddNode duplicate"
def helperAddEdge(list,dic,edge):
	small = edge[0]; big =edge[1]
	if small['id'] > big['id']: small = edge[1]; big = edge[0]
	
	if not small['id'] in dic:
		dic[small['id']] = [big['id']]
		print "Edge New : "
	#so this is not new edge to begin with, then is the connection recorded?
	elif big['id'] in dic[small['id']] :
		dic[small['id']].append(big['id'])
		print "Edge added : "
	else : print "Edge duplicate"
	
	return ""
	
def add(listNodes,listEdges, dicNodes,dicEdges, e):
	print "Attempting to addNewNode...\nid    : " + str(e['id']) + "\nedges : " + str(len(e['edges']) )
	helperAddNode(listNodes,dicNodes,e);
	edges = e['edges'] #recursively add edge nodes, hopefully no infinite returns 
	for i in  range(0,len(edges) ):
		newNode = edges[i]['terminal']
		add(listNodes,listEdges,dicNodes,dicEdges,newNode);
		helperAddEdge(listEdges,dicEdges,[e,newNode]);
	#raw_input()
	
def read(s):
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
	for i in range(0,5):
		print graphNodes[i]
		
	#it = iter(nodes)
	#while True:
	#	print it.next()
	#	raw_input()
	#print item
	#print "Interpreter loaded : " + nodes
	return {'nodes':graphNodes , 'edges':[]}