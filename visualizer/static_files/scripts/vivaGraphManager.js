//var graph = graphGenerator.randomNoLinks(500);
		//var graph = graphGenerator.completeBipartite(10, 10);
		//var graph = graphGenerator.complete(100);
		//var graph = graphGenerator.balancedBinTree(10);
		var VivaCustomNode ={
			isCreateNewLink : true,
			nodeSelected :[""],
			EVENT_AddNewLink : function(graph,from, to){
				console.log("VivaCustomNode::EVENT_ADDNEWLINK");
				vivaGraphManager.helperAddLink(graph,from,to);
			},
			EVENT_NewNodeSeleccted : function(graphics,nodeId){
	//https://developer.mozilla.org/en-US/docs/Web/API/Element
	//access ui svelement
	//to get child "rect" then change its color
	//well for latter I suppose.
	
	var ui = graphics.getNodeUI(nodeId);
		//ui.focuse();
        //var img = graphics.getNodeUI(nodeId).getElementById('img');
        console.log(ui);
        console.log(ui.attributes);
        console.log(ui.children);
		//console.log(ui.getElementById('img'));
		//console.log(img);
		//ui.attr('fill','red');
	},
	EVENT_NodeDeSelected: function(graphics,nodeId){
		var ui = graphics.getNodeUI(nodeId);
		//ui.attr('fill','blue');
	},
	init : function(graphics,graph,node,obj) {
		addNewLink = function(node){
			arr = VivaCustomNode.nodeSelected;
			
			if(arr[0] == "") {
				arr[0] = node.id;
				VivaCustomNode.EVENT_NewNodeSeleccted(graphics,node.id);
			}
			else if(arr[0] == node.id);//duplicate click
			else {
				VivaCustomNode.EVENT_NodeDeSelected(graphics,arr[0]);
				VivaCustomNode.EVENT_AddNewLink(graph, arr[0],node.id);
				arr[0] = "";
				
			}
			
			console.log("Click");
			console.log(arr);
		};
		highlightRelatedNodes = function(nodeId, isOn) {
            // just enumerate all realted nodes and update link color:
            graph.forEachLinkedNode(nodeId, function(node, link){
				//console.log(link)
				var linkUI = graphics.getLinkUI(link.id);
				if (linkUI) {
                    // linkUI is a UI object created by graphics below
                    linkUI.attr('stroke', isOn ? 'red' : 'gray');
                }
            });
        };
        changeEdgeLength = function(nodeId, size) {
        	nodeChanges =[]
            // just enumerate all realted nodes and update link color:
            graph.forEachLinkedNode(nodeId, function(node, link){
            	var ui = graphics.getLinkUI(link.id);
            	nodeChanges.push([link,link.fromId,link.toId,{lengthRatio : size}]);
            });
            for(i in nodeChanges){
            	var link = nodeChanges[i];
            	graph.removeLink(link[0]);
            	graph.addLink(link[1],link[2],link[3]);
				//console.log("changesMade");
			}
		};
		$(obj).mousedown(function() {
			if(VivaCustomNode.isCreateNewLink)
				addNewLink(node);
			console.log("clicked "  + node.id);
			changeEdgeLength(node.id,.005);
		});
		$(obj).mouseup(function() {
			console.log("clicked "  + node.id);
			changeEdgeLength(node.id,1);
		});
		$(obj).hover(function() { // mouse over
			highlightRelatedNodes(node.id, true);
			}, function() { // mouse out
				highlightRelatedNodes(node.id, false);
			});
	},
	isRemoveLink : true,
	//nodeSelected : 0,
	initLink : function(graphics,graph,node,obj){
		$(obj).mousedown(function() {
			//removeLink
			//console.log("clicked "  + node);
			//console.log( node);
			if(VivaCustomNode.isRemoveLink)graph.removeLink(node);
		});
		$(obj).hover(function() { // mouse over
			//console.log(obj);
			//obj.attr('stroke','blue');
			//if(VivaCustomNode.nodeSelected !=0){
			//	VivaCustomNode.nodeSelected.attr('stroke','gray');
			//}
			//VivaCustomNode.nodeSelected = obj
                           //.attr('stroke', 'gray')
				//highlightRelatedNodes(node.id, true);
			}, function() { // mouse out
				//obj.attr('stroke','gray');
				//highlightRelatedNodes(node.id, false);
			});
	}
}
var vivaGraphManager = {
	myLayout: "layout",
	getLayOut:function(graph){
		var idealLength = 500;
		return Viva.Graph.Layout.forceDirected(graph, {
			springLength : idealLength,
			springCoeff : 0.0001,
			dragCoeff : 0.031,
			gravity : -25.2,
		// This is the main part of this example. We are telling force directed
		// layout, that we want to change length of each physical spring
		// by overriding `springTransform` method:
		springTransform: function (link, spring) {
			spring.length = idealLength * link.data.lengthRatio;
		}
	})
	},
	helperAddLink : function(graph,source,target, length) {
		length = typeof a !== 'undefined' ? length : 1;
		graph.addLink(source,target,{lengthRatio: length});
	},
	getRenderer :function (graph, layout,graphics,id){
		return Viva.Graph.View.renderer(graph, {
			layout     : layout,
			graphics : graphics,
			container : document.getElementById(id)
		});
	},
	
	initEventsNode : function (graphics,graph){
		var nodeSize = 20;
		graphics.node(function(node) {
			 var ui = Viva.Graph.svg('g'),
			 	svgText = Viva.Graph.svg('text').attr('y', '-0px').attr('font-size','20')
			 	.text(node.data.label + " / " + node.data.type + " "+node.data.data),
			 	img = Viva.Graph.svg('rect')
			 	.attr('width', nodeSize)
			 	.attr('height', nodeSize)
			 	.attr('fill', 'blue')
			 	.attr('id', 'img');
			 ui.append(img);
			 ui.append(svgText);
			 VivaCustomNode.init(graphics,graph,node,ui);
			 return ui;
                 	});
	graphics.placeNode(function(nodeUI, pos) {
		// 'g' element doesn't have convenient (x,y) attributes, instead
		 // we have to deal with transforms: http://www.w3.org/TR/SVG/coords.html#SVGGlobalTransformAttribute
		 nodeUI.attr('transform',
			'translate(' + (pos.x - nodeSize/2) + ',' + (pos.y - nodeSize/2) + ')');
		});
	},
	initLink : function (graphics,graph){
		var nodeSize = 10;
		var geom = Viva.Graph.geom();
		graphics.link(function(link){
                // Notice the Triangle marker-end attribe:
                var ui =  Viva.Graph.svg('path')
                .attr('stroke', 'gray')
                .attr('stroke-width',10)
                .attr('marker-end', 'url(#Triangle)');
                VivaCustomNode.initLink(graphics,graph,link,ui);
                return ui;
            });
		graphics.placeLink(function(linkUI, fromPos, toPos) {
              // Here we should take care about
              //  "Links should start/stop at node's bounding box, not at the node center."

              // For rectangular nodes Viva.Graph.geom() provides efficient way to find
              // an intersection point between segment and rectangle
              var toNodeSize = nodeSize,
              fromNodeSize = nodeSize;

              var from = geom.intersectRect(
                      // rectangle:
                              fromPos.x - fromNodeSize / 2, // left
                              fromPos.y - fromNodeSize / 2, // top
                              fromPos.x + fromNodeSize / 2, // right
                              fromPos.y + fromNodeSize / 2, // bottom
                      // segment:
                      fromPos.x, fromPos.y, toPos.x, toPos.y)
                         || fromPos; // if no intersection found - return center of the node

                         var to = geom.intersectRect(
                      // rectangle:
                              toPos.x - toNodeSize / 2, // left
                              toPos.y - toNodeSize / 2, // top
                              toPos.x + toNodeSize / 2, // right
                              toPos.y + toNodeSize / 2, // bottom
                      // segment:
                      toPos.x, toPos.y, fromPos.x, fromPos.y)
                          || toPos; // if no intersection found - return center of the node

                          var data = 'M' + from.x + ',' + from.y +
                          'L' + to.x + ',' + to.y;

                          linkUI.attr("d", data);
                      });

},
initEventsPath: function (graphics){
			// To render an arrow we have to address two problems:
            //  1. Links should start/stop at node's bounding box, not at the node center.
            //  2. Render an arrow shape at the end of the link.

            // Rendering arrow shape is achieved by using SVG markers, part of the SVG
            // standard: http://www.w3.org/TR/SVG/painting.html#Markers
            var createMarker = function(id) {
            	return Viva.Graph.svg('marker')
            	.attr('id', id)
            	.attr('viewBox', "0 0 10 10")
            	.attr('refX', "10")
            	.attr('refY', "5")
            	.attr('markerUnits', "strokeWidth")
            	.attr('markerWidth', "5")
            	.attr('markerHeight', "5")
            	.attr('orient', "auto");
            },

            marker = createMarker('Triangle');
            marker.append('path').attr('d', 'M 0 0 L 10 5 L 0 10 z');
			// Marker should be defined only once in <defs> child element of root <svg> element:

			var defs = graphics.getSvgRoot().append('defs');

			defs.append(marker);
			console.log(defs)
		},


		init : function(id, nodes, edges){
			var graphGenerator = Viva.Graph.generator();
			var graph = Viva.Graph.graph();
			var graphics = Viva.Graph.View.svgGraphics();
			var i = 0;

			console.log("mylayout"+ vivaGraphManager.myLayout);
			vivaGraphManager.myLayout = vivaGraphManager.getLayOut(graph)
			var renderer = vivaGraphManager.getRenderer(graph,vivaGraphManager.myLayout,graphics,id);
		renderer.run(); //Must run renderer prior
		//Otherwise SVG, the canvas thinging won't be created 
		//add events that will actually "affect" how it looks
		vivaGraphManager.initEventsNode(graphics,graph);
		vivaGraphManager.initEventsPath(graphics);
		vivaGraphManager.initLink(graphics,graph);
          // Render the graph
          vivaGraphManager.addAll(graph,nodes,edges)

      },
      addAll: function (graph, nodes,edges){
      	for (var n in nodes){
      		var me =nodes[n];
      		try {graph.addNode(me.id,{type : me.type, value : me.value, label : me.label} ); }
      		catch(exception){}
      	}
      	for (var n in edges){
      		try{vivaGraphManager.helperAddLink(graph,edges[n].source,edges[n].target);}
      		catch(exception){}
      	}
      }

  }