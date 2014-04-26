state().loaded(function(){


	//++ Setup

	var CodeArea = CodeMirror(document.querySelector(".query-editor-body"), {
		value:"\n".repeat(30),
        lineNumbers: true,
		mode: {name: "javascript", json: true},
		theme: "default"
    });

	var ed = state().editor;

	//store the state of the code field every time you hit a key.
	document.querySelector(".query-editor-body").onkeyup = function(){

		ed().tabs().get( ed().current_tab() ).body( CodeArea.getDoc().getValue() );
	}

	document.querySelector(".add-tab").onclick = add_tab_event;
	function add_tab_event(){
		ed().tabs().insert( ed().tabs().length() );

	};

	function close_tab_event(event){

		ed().tabs().remove( tic(event.target.parentNode) );
	}

	function select_tab_event(event){
		target_tab = event.target;
		if(event.target.classList.contains("query-editor-tab-name")){
			target_tab = event.target.parentNode;
		}
		if(event.target.classList.contains("query-editor-tab-icon")){
			return;
		}

		ed().current_tab( tic(target_tab) );
	}

	//alert me when a new tab is added
	ed().tabs(function(type, index){


		if(type == "insert"){
			add_tab( tic( index ) );

			ed().tabs().get(index).name(function(name){
				set_tab_name( tic( index ), name );
				return true;
			});

			var tab_name = "Tab " + ed().tabs().length() ;
			if(state().settings().prompt_for_tab_name()){
				tab_name = window.prompt('Tab Name: ', "Tab " + ed().tabs().length() );
			}
			ed().tabs().get(index).name(tab_name);
			ed().tabs().get(index).body( "\n".repeat(30) );
			ed().current_tab(index);
		}

		if(type == "remove"){
			if( tic( index ).classList.contains("active-tab") 
				&& tic( index ).parentNode.querySelectorAll("div").length > 2){
		 		ed().current_tab(0);
			}
			close_tab( tic( index ) );
			
		}

		return true;

	});

	ed().current_tab(function(current_tab){
		select_tab( tic(current_tab) );
		set_tab_body( tic(current_tab), ed().tabs().get( ed().current_tab() ).body() );
		return true;
	})
	
	add_tab_event();


	//++ Modify View Of Tabs

	function close_tab(target_tab){
		setTimeout(function(){
			target_tab.parentNode.removeChild(target_tab);
		},150);
		
		target_tab.style.animation =  "shrinkTab 0.15s";
		target_tab.style.overflow = "hidden";
	}

	function select_tab(target_tab){

		nodeListIter(".query-editor-tabs .query-editor-tab", function(tab){
			tab.classList.remove("active-tab");
		});

		target_tab.classList.add("active-tab");
	}

	function add_tab(){
		var new_tab = document.createElement("div");
		new_tab.classList.add("query-editor-tab");

		var new_tab_name = document.createElement("span");
		new_tab_name.classList.add("query-editor-tab-name");
		new_tab.appendChild(new_tab_name); 
		new_tab.onclick = select_tab_event;

		var new_tab_icon = document.createElement("img");
		new_tab_icon.src = "general/icons/cross.svg";
		new_tab_icon.classList.add("query-editor-tab-icon");
		new_tab.appendChild(new_tab_icon);
		new_tab_icon.onclick = close_tab_event;

		document.querySelector(".query-editor-tabs").insertBefore(new_tab, document.querySelector(".add-tab"));

	}

	function set_tab_name(tab, tab_name){
		tab.querySelector(".query-editor-tab-name").innerHTML = tab_name;
	}

	function set_tab_body(tab, tab_body){
		if(tab.classList.contains("active-tab") || typeof tab_body == "undefined"){
			CodeArea.getDoc().setValue( tab_body );
		}
	}


	//++ Untils

	//tab to index converter + index to tab converter tic(0) => {a}, tic({b}) => 1
	function tic(tab){
		var tabs = document.querySelectorAll(".query-editor-tabs .query-editor-tab");
		if(typeof tab == "number"){
			return tabs[tab]; 
		}
		for(var i = 0; i < tabs.length; i++){
			if(tabs[i] == tab){
				return i;
			}
		}	
	}

})