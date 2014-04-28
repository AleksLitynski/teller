state().loaded(function(){


	state().visualizer().json(function(new_json){
		display_json(new_json);
		return true;
	})


	function display_json(to_display){

		if( typeof to_display == "string" ){
			to_display = JSON.parse(to_display);
		}

		var current_vis = document.querySelector(".node-container");
		if(current_vis != null){
			current_vis.parentNode.removeChild( current_vis );
		}


		new PrettyJSON.view.Node({ 
            el: document.querySelector(".json-visualizer"),
            data: to_display
        });
	}

	display_json('{"string":"foo","number":5,"array":[1,2,3],"object":{"property":"value","subobj":{"arr":["foo","ha"],"numero":1}}}');

/*
var i = 0; 
	(function redraw(){

	setTimeout(function(){

		i++;
		if(i%2==0){
			display_json('{  "array": [    1,    2,    3  ],  "boolean": true,  "null": null,  "number": 123,  "object": {    "a": "b",    "c": "d",    "e": "f"  },  "string": "Hello World"}');
		} else {
			display_json('{"string":"foo","number":5,"array":[1,2,3],"object":{"property":"value","subobj":{"arr":["foo","ha"],"numero":1}}}');
		}

		redraw();
	}, 1000);
	})()*/


})


        