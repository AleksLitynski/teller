import socket
import thread
import random

#holds a single node
class node:
    id    = -1
    value = ""
    #a list of edges by their index in the ontology's edge array.
    edges = []
    def __init__(self, count, value):
        self.id    = count
        self.value = value

    def add_edge(self, edge_id):
        self.edges.append(edge_id)

    #prints perfectly formatted json. The X, Y, Size should be removed soon.
    def to_string(self):
        return "{ " \
        "\"id\": \"n" + str(self.id) + "\"," \
        "\"label\": \"" + str(self.value) + "\"," \
        "\"x\": " + str(random.uniform(0,10)) + "," \
        "\"y\": " + str(random.uniform(0,10)) + "," \
        "\"size\": " + str(3) + "}," 

#an edge. Has the id/index of the start and end point.
class edge:
    id    = -1
    start = -1
    end   = -1
    def __init__(self, count, start, end):
        self.id    = count
        self.start = start
        self.end   = end

    def to_string(self):
        return "{ " \
        "\"id\": \"e" + str(self.id) + "\"," \
        "\"source\": \"n" + str(self.start) + "\"," \
        "\"target\": \"n" + str(self.end) + "\"}," 

#Holds an entire graph.
class ontology:
    nodes = []
    edges = []
    node_count = 0
    edge_count = 0



    def __init__(self):
        #pass tells the interpriter that we are just stubbing out the method.
        pass

    #Adds a node to the graph
    def add_node(self, value):
        self.nodes.append( node(self.node_count, value))
        self.node_count = self.node_count + 1

    #adds an edge. No removal.
    def add_edge(self, start, end):
        self.edges.append( edge(self.edge_count, start, end))
        self.nodes[start].add_edge(self.edge_count)
        self.nodes[end  ].add_edge(self.edge_count)
        self.edge_count = self.edge_count + 1

    #prints out the whole graph.
    def print_all(self):
        printed = "{ \"nodes\":["
        for node in self.nodes:
            printed = printed + node.to_string()
        printed = printed[:-1] + "], \"edges\": ["
        for edge in self.edges:
            printed = printed + "\n" + edge.to_string()
        printed = printed[:-1] + "]}"
        return printed

    #just a stub. Eventually, it could parse a query and do better than a fat dump.
    def field_query(self, query, connection):
        connection.send( self.print_all() )






def run():

    #createes an ontology and adds some fakie nodes.
    the_ontology = ontology()
    the_ontology.add_node("node zero")
    the_ontology.add_node("node one")
    the_ontology.add_node("node two")
    the_ontology.add_node("node three")
    the_ontology.add_edge(0, 1)
    the_ontology.add_edge(0, 2)
    the_ontology.add_edge(0, 3)
    the_ontology.add_edge(2, 3)

    #You can define function in functon.
    #This will be called in a new thread to await TCP connections.
    def listen_for_client():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 5005)) #binds to a port and waits
        s.listen(1)

        #loops forever waiting for a connection.
        while True:
            print "waiting for new connection"
            conn, addr = s.accept()
            print "connected to: ", addr
            while True:
                #receives data over the connection 
                data = conn.recv(1024)
                if not data: break #if there is no more data, break.
                the_ontology.field_query(data, conn) #once all the data is through, filed the query.

            conn.close()

    #spawn the TCP thread
    thread.start_new_thread(listen_for_client, ())


    print "press CTRL + C to exit"
    #keeps the main thread awake so the program don't quit.
    while(True):
        pass







#runs the program.
run()

