This is a Server and client code that enables chat between users (including protocol).
The server works with several clients that communicate with each other and supports commands: NAME , GET_NAMES, MSG and EXIT.

The NAME command allows us to set a name for our client. For example: NAME A would determine the
The name A for the client, so now messages destined for A will be forwarded to it by
the server. The server will answer it with HELLO with the specified name. For example: HELLO A. If
The name A is already occupied by another client, the server will reply that the name is occupied.

The GET_NAMES command will cause the server to send the list of all names to the client
The clients that are connected to the server.

The MSG command will cause a message to be sent to the client by its name. For example MSG A HELLO
will cause HELLO to be sent to client A. The server will add before that who the sender is
the message, for example if B sent the message to A then A will show B sent HELLO.

The EXIT command will disconnect the client and close its socket
