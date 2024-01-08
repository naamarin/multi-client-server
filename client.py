#by Naama Iluz ID 212259204
import socket
import protocol
import select
import msvcrt


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", protocol.PORT))

user_input = b""
response = ""
key = ""

print("Please enter commands\n")

while True:
    ready, write,x = select.select([client_socket], [client_socket], [], .1)
    #if client_socket in ready[0]:
    for current_socket in ready:
        if current_socket is client_socket:
            valid_msg, response = protocol.get_msg(client_socket)
            if valid_msg:
                print("Server sent: " + response)
    if msvcrt.kbhit():
        key = msvcrt.getch()
        if key == b'\r': # Enter key
            if user_input.decode("utf-8") == "EXIT":
                client_socket.send(protocol.add_length_field(user_input.decode("utf-8")).encode())
                break
            print()
            client_socket.send(protocol.add_length_field(user_input.decode("utf-8")).encode())
            user_input = b""
        else:
            user_input += key
            print(key.decode("utf-8"),end="",flush=True)

client_socket.close()