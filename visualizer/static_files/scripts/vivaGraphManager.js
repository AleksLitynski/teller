var vivaGraphManager = {
	init : function(id, nodes, edges){
		var graphGenerator = Viva.Graph.generator();
		
		var graph = Viva.Graph.graph();
		var i = 0;
		
		
		
		//var graph = graphGenerator.randomNoLinks(500);
		//var graph = graphGenerator.completeBipartite(10, 10);
		//var graph = graphGenerator.complete(100);
		//var graph = graphGenerator.balancedBinTree(10);
		
		var layout = Viva.Graph.Layout.forceDirected(graph, {
		springLength : 500,
		springCoeff : 0.0001,
		dragCoeff : 0.031,
		gravity : -25.2
		});
		
		var graphics = Viva.Graph.View.svgGraphics();
		var nodeSize = 24;
		var renderer = Viva.Graph.View.renderer(graph, {
					layout     : layout,
                    graphics : graphics,
					container : document.getElementById(id)
                });
		renderer.run();
		
		graphics.node(function (node) {
                    var ui = Viva.Graph.svg("rect")
                         .attr("width", 10)
                         .attr("height", 10)
                         .attr("fill", "#00a2e8");
                    ui.addEventListener('click', function () {
                        // toggle pinned mode
                        layout.pinNode(node, !layout.isNodePinned(node));
                    });
                    return ui;
                });
		
		//var renderer = Viva.Graph.View.renderer(graph, {
		//		
		//		graphics   : graphics
		//	});
		//https://github.com/anvaka/VivaGraphJS/blob/master/demos/tutorial_svg/06%20-%20Composite%20Nodes.html
		graphics.node(function(node) {
              // This time it's a group of elements: http://www.w3.org/TR/SVG/struct.html#Groups
              var ui = Viva.Graph.svg('g'),
                  // Create SVG text element with user id as content
                  svgText = Viva.Graph.svg('text').attr('y', '-4px').text(node.data),
                  img = Viva.Graph.svg('image')
                     .attr('width', nodeSize)
                     .attr('height', nodeSize)
                     .link('https://secure.gravatar.com/avatar/' + node.data); //TODO : take care of this code latter 

              ui.append(svgText);
              ui.append(img);
              return ui;
            }).placeNode(function(nodeUI, pos) {
                // 'g' element doesn't have convenient (x,y) attributes, instead
                // we have to deal with transforms: http://www.w3.org/TR/SVG/coords.html#SVGGlobalTransformAttribute
                nodeUI.attr('transform',
                            'translate(' +
                                  (pos.x - nodeSize/2) + ',' + (pos.y - nodeSize/2) +
                            ')');
            });

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
                               .attr('markerWidth', "20")
                               .attr('markerHeight', "15")
                               .attr('orient', "auto");
                },

            marker = createMarker('Triangle');
            marker.append('path').attr('d', 'M 0 0 L 10 5 L 0 10 z');
			// Marker should be defined only once in <defs> child element of root <svg> element:
			console.log(renderer)
			var defs = graphics.getSvgRoot().append('defs');
			
            defs.append(marker);
			console.log(defs)
			
			
            var geom = Viva.Graph.geom();

            graphics.link(function(link){
                // Notice the Triangle marker-end attribe:
                return Viva.Graph.svg('path')
                           .attr('stroke', 'gray')
                           .attr('marker-end', 'url(#Triangle)');
            }).placeLink(function(linkUI, fromPos, toPos) {
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
			
            // Render the graph
           vivaGraphManager.addAll(graph,nodes,edges)
		
	},
	addAll: function (graph, nodes,edges){
		for (var n in nodes){
			var me =nodes[n];
			try {graph.addNode(me.id, me.label);}
			catch(exception){}
		}
		for (var n in edges){
			//console.log(edges[0]);
			try{graph.addLink(edges[n].source,edges[n].target);}
			catch(exception){}
		}
	}

}