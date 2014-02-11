import socket
import thread
import random

class node:
    id    = -1
    value = ""
    edges = []
    def __init__(self, count, value):
        self.id    = count
        self.value = value

    def add_edge(self, edge_id):
        self.edges.append(edge_id)

    def to_string(self):
        return "{ " \
        "\"id\": \"n" + str(self.id) + "\"," \
        "\"label\": \"" + str(self.value) + "\"," \
        "\"x\": " + str(random.uniform(0,10)) + "," \
        "\"y\": " + str(random.uniform(0,10)) + "," \
        "\"size\": " + str(3) + "}," 


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


class ontology:
    nodes = []
    edges = []
    node_count = 0
    edge_count = 0



    def __init__(self):
        pass

    def add_node(self, value):
        self.nodes.append( node(self.node_count, value))
        self.node_count = self.node_count + 1

    def add_edge(self, start, end):
        self.edges.append( edge(self.edge_count, start, end))
        self.nodes[start].add_edge(self.edge_count)
        self.nodes[end  ].add_edge(self.edge_count)
        self.edge_count = self.edge_count + 1


    def print_all(self):
        printed = "{ \"nodes\":["
        for node in self.nodes:
            printed = printed + node.to_string()
        printed = printed[:-1] + "], \"edges\": ["
        for edge in self.edges:
            printed = printed + "\n" + edge.to_string()
        printed = printed[:-1] + "]}"
        return printed

    def field_query(self, query, connection):
        connection.send( self.print_all() )




def run():

    the_ontology = ontology()
    the_ontology.add_node("node zero")
    the_ontology.add_node("node one")
    the_ontology.add_node("node two")
    the_ontology.add_node("node three")
    the_ontology.add_edge(0, 1)
    the_ontology.add_edge(0, 2)
    the_ontology.add_edge(0, 3)
    the_ontology.add_edge(2, 3)


    def listen_for_client():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 5005))
        s.listen(1)


        while True:
            print "waiting for new connection"
            conn, addr = s.accept()
            print "connected to: ", addr
            while True:
                data = conn.recv(1024)
                if not data: break
                the_ontology.field_query(data, conn)

            conn.close()

    thread.start_new_thread(listen_for_client, ())


    print "press CTRL + C to exit"
    while(True):
        pass








run()

