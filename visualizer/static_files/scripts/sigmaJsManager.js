//must include 
//scripts/sigma.min.js
//scripts/plugins/sigma.parsers.json.min.js
var sigmaJsManager = {
	sig : "",
	init : function (id , ns, es) {
		sigmaJsManager.addEvents();
		sig ={container: document.getElementById(id),settings: {defaultNodeColor: '#eb2148'} };
		sig.graph = {nodes: ns, edges: es };
		sig = new sigma(sig);
		sigmaJsManager.newDataAdded(sig);
	},
	includeJs : function (jsFilePath) {
		var js = document.createElement("script");
	
		js.type = "text/javascript";
		js.src = jsFilePath;
	
		document.body.appendChild(js);
	},
	addEvents : function (){
		sigma.classes.graph.addMethod('neighbors', function(nodeId) {
		var k,
			neighbors = {},
			index = this.allNeighborsIndex[nodeId] || {};
	
		for (k in index)
		neighbors[k] = this.nodesIndex[k];
	
		return neighbors;
		});
	},
	patchNewData : function (nodes, edges){
		for (var i  = 0 ; i < nodes.length;i++){
			n = nodes[i];
			try{
				//console.log(nodes[i]);
				sig.graph.addNode(n);
			}
			catch(exception){console.log("Failed to node at " +i);}
		}
		for (var i  = 0 ; i < edges.length;i++){
			n = edges[i];
			try{
				//console.log(nodes[i]);
				sig.graph.addEdge(n);
			}
			catch(excep){console.log("Failed to edge at " +i);}
		}
		
		sig.refresh();
		sig.render();
	},
	addSearchResult : function (){
		var xhr = sigma.utils.xhr();
		xhr.open('GET', 'search', true);
		
		xhr.onreadystatechange  = function(){
			if (xhr.readyState === 4) {
					graph = JSON.parse(xhr.responseText);
					sigmaJsManager.patchNewData(graph.nodes,graph.edges);
				}
		};
		xhr.send();
	},
	addInstancesSeparated : function (){
		var xhr = sigma.utils.xhr();
		xhr.open('GET', 'dataDummy00', true);
		
		xhr.onreadystatechange  = function(){
			if (xhr.readyState === 4) {
					graph = JSON.parse(xhr.responseText);
					sigmaJsManager.patchNewData(graph.nodes,graph.edges);
				}
		};
		xhr.send();
	},
	addInstancesOverlapping : function (){
		var xhr = sigma.utils.xhr();
		xhr.open('GET', 'dataDummy01', true);
		
		xhr.onreadystatechange  = function(){
			if (xhr.readyState === 4) {
					graph = JSON.parse(xhr.responseText);
					sigmaJsManager.patchNewData(graph.nodes,graph.edges);
				}
		};
		xhr.send();
	},
	addInstance_Dot : function () {
		var xhr = sigma.utils.xhr();
		console.log("instantiate" + graph);
	
		sig.graph.addNode({
					"id": "n3",
					"label": "I Am the dot but I don't really help you to improve this graph",
					"x": 0,
					"y": 0,
					"size": 3
					});
		sig.refresh();
		sig.render();
	},
	
	newDataAdded : function (s) {
      // We first need to save the original colors of our
      // nodes and edges, like this:
      s.graph.nodes().forEach(function(n) {
        n.originalColor = n.color;
      });
      s.graph.edges().forEach(function(e) {
        e.originalColor = e.color;
      });

      // When a node is clicked, we check for each node
      // if it is a neighbor of the clicked one. If not,
      // we set its color as grey, and else, it takes its
      // original color.
      // We do the same for the edges, and we only keep
      // edges that have both extremities colored.
      s.bind('clickNode', function(e) {
        var nodeId = e.data.node.id,
            toKeep = s.graph.neighbors(nodeId);
			toKeep[nodeId] = e.data.node;

        s.graph.nodes().forEach(function(n) {
          if (toKeep[n.id])
            n.color = n.originalColor;
          else
            n.color = '#eee';
        });

        s.graph.edges().forEach(function(e) {
          if (toKeep[e.source] && toKeep[e.target])
            e.color = e.originalColor;
          else
            e.color = '#eee';
        });

        // Since the data has been modified, we need to
        // call the refresh method to make the colors
        // update effective.
        s.refresh();
      });

      // When the stage is clicked, we just color each
      // node and edge with its original color.
      s.bind('clickStage', function(e) {
        s.graph.nodes().forEach(function(n) {
          n.color = n.originalColor;
        });

        s.graph.edges().forEach(function(e) {
          e.color = e.originalColor;
        });

        // Same as in the previous event:
        s.refresh();
      });
    }
	
};