var vivaGraphManager = {
	init : function(id, nodes, edges){
		var graphGenerator = Viva.Graph.generator();
		
		var graph = Viva.Graph.graph();
		var i = 0;
		
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

            // Render the graph
            var renderer = Viva.Graph.View.renderer(graph, {
					layout     : layout,
                    graphics : graphics,
					container : document.getElementById(id)
                });
            renderer.run();
		
		renderer.run();
	}

}