state().loaded(function(){


	document.querySelector(".run-query-button").onclick = function(){
		send_query( state().editor().tabs().get( state().editor().current_tab() ).body() );
	}


	function send_query(query){
		jQuery.ajax({

			type: "POST",
			url: "query",
			data: {"query": query},
			success: function(data){receive_query(query, data)},
			dataType: "json"
		})
	}

	function receive_query(query, result){
		console.log(query, result);
		state().history().queries().insert( state().history().queries().length() );
		var new_item = state().history().queries().get( state().history().queries().length() - 1 );
		new_item.query(query);
		new_item.result(JSON.stringify(result));

	}


	state().history().queries(function(type, index){

		function create_dom_history_query(query_index){
					
			state().history().queries().get(query_index).query(function(query_body){
				if(query_body == "") {query_body = "	";}
				history_query.querySelector(".history-query-query").innerHTML = query_body;
				return true;
			});
			state().history().queries().get(query_index).result(function(query_result){
				if(query_result == "") {query_result = "	";}
				history_query.querySelector(".history-query-result").innerHTML = query_result;
				state().visualizer().json(query_result);
				return true;
			});

			var history_query = document.createElement("div");
			history_query.classList.add("history-query");

			history_query.classList.add("history-height");
			setTimeout(function(){history_query.classList.remove("history-height");},0);

			var query_query = document.createElement("span");
			query_query.classList.add("history-query-query");
			query_query.classList.add("history-query-query");
			query_query.onclick = function(){
				state().editor().tabs().insert( state().editor().tabs().length() );
				state().editor().tabs().get( state().editor().tabs().length() - 1 ).body(
					state().history().queries().get(query_index).query()
				);
				state().editor().tabs().get( state().editor().tabs().length() - 1 ).name("Query");
				state().editor().current_tab( state().editor().tabs().length() - 1 );

			}
			history_query.appendChild(query_query);

			var query_result = document.createElement("span");
			query_result.classList.add("history-query-result");
			query_result.onclick = function(){
				state().visualizer().json(
					state().history().queries().get(query_index).result()
				);
			}
			history_query.appendChild(query_result);


			return history_query;

		}

		if(type == "insert"){
			document.querySelector(".history").insertBefore(create_dom_history_query(index), document.querySelector(".history").children[document.querySelector(".history").children.length - index]);
		}
		if(type == "remove"){
			document.querySelector(".history").removeChild(document.querySelector(".history").children[index]);
		}
		if(type == "general"){
			for(var i = state().history().queries().length()-1; i >= 0; i--){
				document.querySelector(".history").appendChild(create_dom_history_query(i));
			}
		}


		return true;
	});

	/*history: {
		queries: [{query:"string", result: "string"}],
		current_query: "number"
	},*/


});