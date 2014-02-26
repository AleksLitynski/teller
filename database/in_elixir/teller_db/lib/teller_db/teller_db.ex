defmodule TellerDb do
	use Application.Behaviour

	# See http://elixir-lang.org/docs/stable/Application.Behaviour.html
	# for more information on OTP Applications
	def start(_type, _args) do
		TellerDb.Supervisor.start_link

		IO.puts "Starting TCP listener"
		TCPServer.listen 5005, fn(socket, data) -> 
			visualizer_with_quotes = String.replace(visualizer, "\'", "\"")
			:gen_tcp.send(socket, visualizer_with_quotes)
		end
	end
end

