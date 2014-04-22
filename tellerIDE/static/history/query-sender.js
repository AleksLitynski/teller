state().loaded(function(){


	document.querySelector(".run-query-button").onclick = function(){
		send_query( state().editor().tabs().get( state().editor().current_tab() ).body() );
	}


	function send_query(query){
		jQuery.ajax({

			type: "POST",
			url: "query",
			data: {"query": query},
			success: receive_query,
			dataType: "json"
		})
	}
	function receive_query(data){
		console.log("dats");
		console.log(data.data);
	}


});