defmodule teller_graph do

	defrecord node, type: nil, value: ""
	defrecord edge, type: nil, weight: 

	#weight.


	def new do
		:digraph.new
	end

	def add_node(graph, type, value) do
		if node_type type do
			new_node = node.new(type: type, value: value)
			:digraph.add_vertex(graph, new_node)
			{:ok, new_node}
		else
			{:failure, node.new(type: nil, value: "Node Type Invalid")}
		end
	end

	def add_edge(graph, type, origin, target, weight, time_range) do
		if edge_type(type, origin.type, target.type) do

		end
	end



	def node_type(:noun), 		  do: true
	def node_type(:verb), 		  do: true
	def node_type(:change), 	  do: true
	def node_type(:relationship), do: true
	def node_type(:value), 		  do: true
	def node_type(:type), 		  do: true
	def node_type(:constraint),   do: true
	def node_type(_), 			  do: false


	#go back and confirm edge has valid from/to
	def edge_type(:describes), 		   do: true #relationship -> ANY
	def edge_type(:knows_of), 		   do: true #noun -> ANY
	def edge_type(:is_a), 	           do: true #noun -> noun
	def edge_type(:has_value),         do: true #relationship -> value
	def edge_type(:has_type), 		   do: true #relationship -> type
	def edge_type(:is_constrained_by), do: true #relationship -> constraint
	def edge_type(:reguarding), 	   do: true #relationship -> noun
	def edge_type(:leads_to),   	   do: true #verb -> verb
	def edge_type(:causes),   		   do: true #verb -> change
	def edge_type(_), 				   do: false



end



dg = :digraph
		graph = dg.new()
		a_node = [noun: "guyman"] #equivent of {:noun, "guyman"}
		b_node = [noun: "nefeller"]
		dg.add_vertex(graph, a_node)
		dg.add_vertex(graph, b_node)
		dg.add_edge(graph, a_node, b_node)

		print_verts = fn
			[[noun: name] | rest], next -> #next is the recursive part. Jose says don't use it. Just use a real function that CAN properly recurse
				IO.puts name
				next.(rest, next) #doesn't optimize tail recursion
			[], _ -> 
		end

		print_verts.(dg.vertices(graph), print_verts)