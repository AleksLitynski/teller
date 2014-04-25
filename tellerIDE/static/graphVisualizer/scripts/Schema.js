//GraphVisualizer's Schema
//importing helper
//TODO : Chop off this chunk of code at some point and make it as a separate file
var imported = document.createElement('script');
imported.src = '/visualizers/visualizer-helper.js';
document.head.appendChild(imported);

var VISUALIZER_TAG_GRAPH = "graph";
var VISUALIZER_BODY_GRAPH = "visualizer-body graph-visualizer";

//https://developer.mozilla.org/es/docs/XMLHttpRequest/Usar_XMLHttpRequest
function helperXHR(request,path,data,f){
	var xhr = sigma.utils.xhr();
	xhr.open(request, path, true);
	var formData = new FormData();

	formData.append("data",data);
	xhr.send(formData);
	xhr.onreadystatechange = function() {
		if (xhr.readyState === 4)f(xhr);
	};	
	console.log(xhr);
}

function search(obj){
		//var input = document.getElementById("searchKeyword").value;
		//var data = ["keyword",input];
		
		//#$("#graph-container").empty();
		//console.log("Trying to POST , and sending data [ " + data + " ]");
		//JSON.stringify(data)
		var data = '{"type": "get", "params": {"depth":2}, "search": {"edges": [{"direction": "inbound","type": "describes","weight-time": "1","terminal": {"type": "relationship","edges": [{"terminal": {"type": "type","value": "named"}},{"terminal": {"type": "value","value": "room"}}]}}]}}'
		//data = "hi ";// + data;
		//data = "hellow";
		helperXHR('POST','sendToDataBase',data,function(xhr){
			graph = JSON.parse(xhr.responseText);
			console.log("Graph data to be displayed is : ");
			console.log(graph);
			vivaGraphManager.init(obj,graph.nodes,graph.edges);
			});
		//document.write('<h2>Your Text and or HTML here.</h2>');
	}

state().visualizer_mode(function (tag) {
	if(tag != VISUALIZER_TAG_GRAPH) return true;
	console.log("Hi, Graph visualizer is now initiating, please stand by.");
	var item = visualizerHelper.getBody(VISUALIZER_BODY_GRAPH);
	console.log("The tag we are going to put our graph is : ");
	console.log(item);
	search(item);




	return true;

});
//EndOfCode