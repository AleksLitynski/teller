loaders.push(function(){

	var tab_data = [];

	var CodeArea = CodeMirror(document.querySelector(".query-editor-body"), {
		value:"\n".repeat(30),
        lineNumbers: true,
		mode: {name: "javascript", json: true},
		theme: "default"
    });

	document.querySelector(".add-tab").onclick = add_tab;
	




	function add_tab(){
		
		var tab_name = "Tab " + (tab_data.length + 1);


		var new_tab = document.createElement("div");
		new_tab.classList.add("query-editor-tab");

		var new_tab_name = document.createElement("span");
		new_tab_name.innerHTML = tab_name
		new_tab_name.classList.add("query-editor-tab-name");
		new_tab.appendChild(new_tab_name); 


		var new_tab_icon = document.createElement("img");
		new_tab_icon.src = "query-editor/cross.svg";
		new_tab_icon.classList.add("query-editor-tab-icon");
		new_tab.appendChild(new_tab_icon); 


		new_tab_icon.onclick = function(){
			var was_ative_tab = this.parentNode.classList.contains("active-tab");
			var tab = this.parentNode;
			var tabSet = tab.parentNode;

			setTimeout(function(){
				tabSet.removeChild(tab);
			},150);
			
			tab.style.animation =  "shrinkTab 0.15s";
			tab.style.overflow = "hidden";
			
			
			if(was_ative_tab && tabSet.querySelectorAll("div").length > 1){
				select_tab(tabSet.querySelectorAll("div")[0]);
			}

		}

		new_tab.onclick = function(event){
			clickedTab = event.target;
			if(event.target.classList.contains("query-editor-tab-name")){
				clickedTab = event.target.parentNode;
			}
			if(event.target.classList.contains("query-editor-tab-icon")){
				return;
			}
			select_tab(clickedTab);
		}


		function select_tab(target_tab){

			var tab_text = "";
			tab_data.forEach(function(tab_info){
				if(tab_info.tab.classList.contains("active-tab")){
					tab_info.value = CodeArea.getDoc().getValue();

				}
				tab_info.tab.classList.remove("active-tab");


				if(tab_info.tab == target_tab){
					tab_text = tab_info.value;
				}
			});


			target_tab.classList.add("active-tab");
			CodeArea.getDoc().setValue(tab_text);
		}


		document.querySelector(".query-editor-tabs").insertBefore(new_tab, document.querySelector(".add-tab"));



		tab_data.push({
			tab: new_tab,
			name: tab_name,
			value: "\n".repeat(30)
		});

		select_tab(new_tab);


	}
	add_tab();


	



})