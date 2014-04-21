state().loaded(function(){

	nodeListIter(".visualizer-option-selection", function(e, i, a){
		e.onmouseup = function(){
			set_active_button(e);
		}

	})

	function set_active_button(active_button){
			disable_all_selections();
			active_button.classList.add("active-button");

			function toggle_if_self(nm){

				if(active_button.classList.contains(nm + "-button")){
					document.querySelector("." + nm + "-visualizer").style.display = "block";
				}
			}
			toggle_if_self("json");
			toggle_if_self("graph");
			toggle_if_self("dataflow");
			toggle_if_self("threed");



	}


	function disable_all_selections(){
		nodeListIter(".visualizer-option-selection", function(e, i, a){
			e.classList.remove("active-button");
		})

		nodeListIter(".visualizer-body", function(e, i, a){
			e.style.display = "none";
		})

		 
	}

	set_active_button(document.querySelector(".json-button"));

})