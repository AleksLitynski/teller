state().loaded(function(){

	

	
	state().mutation().mutations(function(type, index){
		if(type != "insert"){return true;}

		function mut_prop(prop_name){
			var mut_prop = document.createElement("span");
			mut_prop.classList.add("mutation-property");
			mut_prop.classList.add(prop_name);
			return mut_prop;
		}
		var mutation = document.createElement("div");
		mutation.classList.add("mutation");
		mutation.appendChild(mut_prop("mutation-name"));
		mutation.appendChild(mut_prop("mutation-value"));
		mutation.appendChild(mut_prop("mutation-target"));
		mutation.appendChild(mut_prop("mutation-description"));
		mutation.appendChild(mut_prop("mutation-new-tab"));

		var mut_btn = document.createElement("span");
		mut_btn.classList.add("apply-mutation");
		mut_btn.innerHTML = "Apply";
		mutation.appendChild(mut_btn);

		document.querySelector(".mutations").insertBefore(mutation, document.querySelector(".mutations").children[index]);

		return true;

	});

	jQuery.ajax({
	      url: 'mutations/mutations.json',
	      contentType: 'application/json',
	      success: load_success
	})

	function load_success(data){

		var muts = data.mutations;
		for(mutation_primative in muts ){
			var mp = muts[mutation_primative];

			state().mutation().mutations().insert(0);
			var new_object = document.querySelector(".mutations").children[0];

			var cms = state().mutation().mutations().get(0);


			cms.value(function(value){
				new_object.querySelector(".mutation-value").innerHTML = value;
				return true;
			});
			cms.value(mp.value);	
	

			cms.target(function(target){
				new_object.querySelector(".mutation-target").innerHTML = target;
				return true;
			});
			cms.target(mp.target);	
	

			cms.makes_new_tab(function(makes_new_tab){
				new_object.querySelector(".mutation-new-tab").innerHTML = makes_new_tab;
				return true;
			});
			cms.makes_new_tab(mp.makes_new_tab);	


			cms.name(function(name){
				new_object.querySelector(".mutation-name").innerHTML = name;
				return true;
			});
			cms.name(mp.name);	
	

			cms.description(function(description){
				new_object.querySelector(".mutation-description").innerHTML = description;
				return true;
			});
			cms.description(mp.description);	



		}
}


})
