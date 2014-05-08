try:
	import socketserver
except:
	import SocketServer as socketserver
import query_fielder
import ontology

class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("Received comm from: " + self.client_address[0])
        self.data = self.request.recv(1024).strip()
        fielder = query_fielder.query_fielder()
        self.request.sendall( fielder.field_query(self.data, game_ontology) )


if __name__ == '__main__':
    game_ontology = ontology.ontology()
    #game_ontology.override_with_sample()
    game_ontology.override_with_random_room()
    #game_ontology.add_core_objects()
    print("starting TCP listener")
    server = socketserver.TCPServer(("localhost", 5005), TCPHandler)
    server.serve_forever()

