state().loaded(function(){


	document.querySelector(".graph-viz").innerHTML = "";

	var graph = d3.layout.force()
	    .linkDistance(50)
	    .charge(-100)
	    .on("tick", tick);

	var svg = d3.select(".graph-viz").append("svg")
	    .attr("width", "100%")
	    .attr("height", "100%");

	svg.append("rect")
	    .attr("width", "100%")
	    .attr("height", "100%");

	var nodes = graph.nodes(),
	    edges = graph.links(),
	    labels = [],
	    node = svg.selectAll(".graph-node"),
	    edge = svg.selectAll(".graph-edge"),
	    label = svg.selectAll(".graph-label");


update();


function mouseovernode(a){

	nodes.forEach(function(n){
		n.active = false;
	})

	a.active = true;
	neighbors2(a).forEach(function(n){
		n.active = true;
	})

	update();
}

function neighbors2(a){
	var neigh = neighbors(a);

	var neighbors2 = neigh;
	neigh.forEach(function(e){
		neighbors2 = neighbors2.concat(neighbors(e));
	})
	return neighbors2;
}
function neighbors(node){
	var neighbors = [];
	edges.forEach(function(e){
		if(e.source == node){
			neighbors.push(e.target);
		}
	})
	return neighbors;
}


state().framing().central(resize_update);
state().framing().right(resize_update);
window.onresize = resize_update;
state().visualizer().mode(resize_update);
var resize_timer = -1;
function resize_update(){
	/*if(resize_timer == -1){
		graph.on("tick", function(){});
		graph.stop();

		d3 = {};
		graph = {};


		document.querySelector("svg").innerHTML = "";
	}

  	window.clearTimeout(resize_timer);
	resize_timer = setTimeout(function(e){

		graph.on("tick", tick);
		resize_timer = -1;
		update();
	}, 10000);*/
	update();
	return true;
}


function mouseoutnode(a){

	nodes.forEach(function(e){
		e.active = true;
	})

	update();
}

//called on each node? Syncs D3 value and node value, I think...
function tick() {
	edge.attr("x1", function(d) { return d.source.x; })
		.attr("y1", function(d) { return d.source.y; })
		.attr("x2", function(d) { return d.target.x; })
		.attr("y2", function(d) { return d.target.y; });

	node.attr("cx", function(d) { return d.x; })
		.attr("cy", function(d) { return d.y; });

	label.attr("transform", function transform(d) {
		return "translate(" + d.x + "," + d.y + ")";
	})
}


function update() {


	edge = edge.data(edges);
	edge.enter().insert("line").attr("class", "graph-edge")
	.attr("stroke", function(d){
			if(d.type == "relationship"){ return "orange";}
			if(d.type == "noun"){ return "green";}
			if(d.type == "type"){ return "blue";}
			if(d.type == "value"){ return "red";}
	});
	edge.exit().remove();

	node = node.data(nodes);
	node.enter().insert("circle")
		.attr("class", "graph-node")
		.attr("stroke", "transparent")
		.on("mouseover", mouseovernode)
		.on("mouseout", mouseoutnode)
		.call(graph.drag);
	node.call(function(n){
		n.attr("fill", function(d){
			if(d.active == false){return "transparent";}

			if(d.type == "relationship"){ return "orange";}
			if(d.type == "noun"){ return "green";}
			if(d.type == "type"){ return "blue";}
			if(d.type == "value"){ return "red";}
		})
		.attr("r", function(d){

			if(d.active == false){return 1;}

			if(d.type == "relationship"){ return 4;}
			if(d.type == "noun"){ return 7;}
			if(d.type == "type"){ return 3;}
			if(d.type == "value"){ return 3;}
		})
	});

	node.exit().remove();

	label = label.data(nodes);
	label.enter().insert("text")
		.attr("class", "graph-label")
		
		.text(function(d){return d.value;})
		.attr("dx", 0)
		.attr("dy", 0);
	label.call(function(l){
		l.attr("font-size", function(d){
			if(d.active == false){
  				return '6.5px';
			} else {
  				return '14.5px';
			}
		})
	})
	label.exit().remove();




	graph.size([$(".graph-viz").width(), $(".graph-viz").height()]).nodes(nodes).links(edges).start();
}



	state().visualizer().json(function(new_json){
		nodes = [];
		labels = [];
		edges = [];

		json_obj = JSON.parse(new_json);


		if(json_obj.type == "get-success"){
			vis_get_success(json_obj.reply);
		}


		update();
    


		return true;
	})


	function vis_get_success(json){



		json.forEach(function(node){
			add_node(node);
		})

		function add_node(node){
			if(node_with_id(node.id) === false){
				node.active = true;
				nodes.push(node);
			}
			node.edges.forEach(function(e){
				add_node(e.terminal);
			})
		}

		function node_with_id(id){
			var nodes_with_id = nodes.filter(function(e){
				return e.id == id;
			})

			return nodes_with_id.length == 0 ? false : nodes_with_id[0];
		}





		json.forEach(function(node){
			node.edges.forEach(function(edge){
				add_edge(edge, node);
			})
		})

		function add_edge(edge, node){

			edge.source = node_with_id(node.id);
			edge.target = node_with_id(edge.terminal.id);

			if(!is_edge_present(edge)){
				edges.push(edge);
			}

			edge.terminal.edges.forEach(function(edge){
				add_edge(edge, edge.terminal);
			})

		}
	
		function is_edge_present(edge){
			return edges.some(function(e){
				return e["weight-at-times"] == edge["weight-at-times"]
						&& e.direction == edge.direction 
						&& e.type == node.type
						&& nodes_match(e.source, edge.source)
						&& nodes_match(e.target, edge.target);
			})
		}






	}



})


/*
{"type":"get", "params": {"depth":1}, "search":{}}

*/