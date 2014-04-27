state().loaded(function(){


	document.querySelector(".graph-viz").innerHTML = "";

	var graph = d3.layout.force().nodes([{ding:"red", s:10, name: "onetwo"},
										 {ding:"green", s:20, name: "three"},
										 {ding:"grey", s:12, name: "four"},
										 {ding:"blue", s:5, name: "five is"},
										 {ding:"green", s:10, name: "just nubmers"}])
	    .linkDistance(50)
	    .charge(-100)
	    .on("tick", tick);

	var svg = d3.select(".graph-viz").append("svg")
	    .attr("width", "100%")
	    .attr("height", "100%")
	    .on("mousemove", mousemove)
	    .on("mousedown", mousedown);

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

function mousemove() {
  //mouse pos: d3.mouse(this)
}

function mousedown(d) {
	console.log(d);

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

		if(state().debug() === true){

			console.log(d);
		}
		return "translate(" + d.x + "," + d.y + ")";
	})
}

state().framing().central(resize_update);
state().framing().right(resize_update);
window.onresize = resize_update;
state().visualizer().mode(resize_update);
function resize_update(){
	update();
	return true;
}

function update() {

	edge = edge.data(edges);
	edge.enter().insert("line").attr("class", "graph-edge");
	edge.exit().remove();

	node = node.data(nodes);
	node.enter().insert("circle")
		.attr("class", "graph-node")
		.attr("fill", function(d){
			if(d.type == "relationship"){ return "orange";}
			if(d.type == "noun"){ return "green";}
			if(d.type == "type"){ return "blue";}
			if(d.type == "value"){ return "red";}
		})
		.attr("r", function(d){
			if(d.type == "relationship"){ return 3;}
			if(d.type == "noun"){ return 7;}
			if(d.type == "type"){ return 3;}
			if(d.type == "value"){ return 3;}
		}).attr("stroke-width", 0)
		.call(graph.drag);
	node.exit().remove();

	label = label.data(nodes);
	label.enter().insert("text")
		.attr("class", "graph-label")
		.text(function(d){return d.value;})
		.attr("dx", 0)
		.attr("dy", 0);
	label.exit().remove();



	graph.size([$(".graph-viz").width(), $(".graph-viz").height()]).nodes(nodes).links(edges).start();
}



	state().visualizer().json(function(new_json){

		json_obj = JSON.parse(new_json);


		if(json_obj.type == "get-success"){
			vis_get_success(json_obj.reply);
		}



		return true;
	})


	function vis_get_success(json){


		nodes = [];
		labels = [];
		edges = [];

		json.forEach(function(node){
			add_node(node);
		})

		function add_node(node){
			if(node_with_id(node.id) === false){
				nodes.push(node);
			} else {
				console.log("redudant");
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
				console.log("real add");
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




		update();
    



	}



})


/*
{"type":"get", "params": {"depth":1}, "search":{}}

*/