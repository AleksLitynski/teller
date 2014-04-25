var state = stately(

{
	loaded:"boolean",

	database_name: "string",
	visualizer_mode: "string",

	editor: {
		tabs: [{body:"string", name: "string"}],
		current_tab: "number"
	},

	history: {
		queries: [{query:"string", result: "string"}],
		current_query: "number"
	},

	mutation: {
		mutations: [{
			value: "string",
			target: "string",
			makes_new_tab: "string",
			name: "string",
			description: "string"
		}],
		current_mutation: "number"
	},

	framing: {
		central: "number",
		left: "number",
		right: "number"
	},

	settings: {
		prompt_for_tab_name: "boolean"
	}

}


);



//importing helper
//TODO : Chop off this chunk of code at some point and make it as a separate file
var imported = document.createElement('script');
imported.src = '/visualizers/visualizer-helper.js';
document.head.appendChild(imported);

var TAG_VISUALIZER_GRAPH = "graph";

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
			console.log(graph);
			vivaGraphManager.init(obj,graph.nodes,graph.edges);
			});
		//document.write('<h2>Your Text and or HTML here.</h2>');
	}

state().visualizer_mode(function (tag) {
	if(tag != TAG_VISUALIZER_GRAPH) return true;
	var item = visualizerHelper.getTab(tag);
	search(item);
	console.log(item);




	return true;

});
//EndOfCode

state().settings().prompt_for_tab_name(false);