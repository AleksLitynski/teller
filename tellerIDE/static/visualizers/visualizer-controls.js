state().loaded(function(){

	nodeListIter(".visualizer-option-selection", function(e, i, a){
		e.onclick = function(){
			state().visualizer_mode(e.dataset["vistype"]);
		}
	})

	//when someone sets the mode, toggle to the proper mode, visually.
	state().visualizer_mode(function(current_mode){
		set_active_button(current_mode);
		return true;
	});




	function set_active_button(button_type){

		//disable all buttons
		nodeListIter(".visualizer-option-selection", function(e, i, a){
			e.classList.remove("active-button");
		})

		nodeListIter(".visualizer-body", function(e, i, a){
			e.style.display = "none";
		})

		//enable the correct button
		var active_button = document.querySelector("[data-vistype='"+button_type+"']");
		active_button.classList.add("active-button");
		document.querySelector( "." + button_type + "-visualizer").style.display = "block";
	}

	//set to json by default
	state().visualizer_mode("json");

})