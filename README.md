teller
======

A game engine dedicated to making generative content easier to make.

[![Gitter chat](https://badges.gitter.im/tavoe/teller.png)](https://gitter.im/tavoe/teller) <~~ Chat channel

How to run
----------

1. In the database folder, call "python main.py"
2. In the visualizer folder, call "python server.py"
3. In a web browser, goto: 127.0.0.1:8080. You should see a few nodes/edges on screen.


How it works
------------

The database.

1. It has a simple, in memory ontology. There are three classes. Edges, Nodes, and "the ontology". Each node has a list of corosponding edges. Each edge names the nodes it conjoins, and the ontology stores both the nodes and edges. They can print themselves into a json file (not coincedtally of the exact same structure sigma.js requires.)

2. The TCP server. In the main function, we create an ontology and load in a few edges/nodes. We than spawn a new thread that listens for a TCP connection. Upon receiving ANY message over that connection, it dumps the while ontology in json format. The second thread is spawned, because when listening for a TCP connection, the program is rendered interminable. By putting it onto another thread, we can kill the main thread via ctrl+c, and it will bring the background thread down with it.


The Visualizer.

1. On startup, we connect to the database once and get the json dump. We store it in a global variable.

2. We start a web server and sever out of the static_files folder. If we are asked for data.json, we swoop in and send out the database json instead.


The Website.

1. We load a tiny index page that grabs sigma and the json in turn. It draws the json via signma. 
