defmodule TCPServer do

  def listen(port, handler) do
    tcp_options = [:list, {:packet, 0}, {:active, false}, {:reuseaddr, true}]
    {:ok, listen_socket} = :gen_tcp.listen(port, tcp_options)
    wait_for_connection(listen_socket, handler)
  end
 

  defp wait_for_connection(listen_socket, handler) do
    {:ok, socket} = :gen_tcp.accept(listen_socket) #blocks until a connection is received
    thread_id = spawn(fn() -> do_server(socket, handler) end) #ends someone to deal with connection

    thread_id <- "A message for you!"
    wait_for_connection(listen_socket, handler) #keep on waiting
  end


  defp do_server(socket, handler) do
    case :gen_tcp.recv(socket, 0) do #wait until you have a message
      {:ok, data} -> #these is a message to receive

      spawn(fn() -> handler.(socket, data) end) #let the handler deal with the message

        do_server(socket, handler) #wait for their reply
 
      {:error, :closed} -> :ok #if no more messages, give it up
    end
  end



end