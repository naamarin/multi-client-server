#by Naama Iluz ID 212259204
import socket
import select
import protocol

#SERVER_PORT = 1234
SERVER_IP = "0.0.0.0"
#COMMANDS = ["NAME", "GET_NAMES", "MSG", "EXIT"]


print("Setting up server...")
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, protocol.PORT))
server_socket.listen()
print("Listening for clients...")

clients_list = []
messages_to_send = []
all_names = {}
answare = ""
def name(current_socket, words):
    if len(words) == 1:
        answare = "You need to write name"
    elif current_socket in list(all_names.values()):
        answare = "You already have name"
    elif words[1] in list(all_names.keys()):
        answare = "This name is not available"
    else:
        all_names[words[1]] = current_socket
        answare = "Hello " + words[1]
    messages_to_send.append((answare, current_socket))

def get_names(current_socket):
    answare = " ".join(list(all_names.keys()))
    messages_to_send.append((answare, current_socket))

def msg(current_socket, words):
    client_name = ""
    if len(words) == 1:
        answare = "You need to write the name of the reciper"
        messages_to_send.append((answare, current_socket))
    elif words[1] in list(all_names.keys()):
        for i in list(all_names.keys()):
            if all_names[i] == current_socket:
                client_name = i
        answare = client_name + " sent " + " ".join(words[2:])
        messages_to_send.append((answare, all_names[words[1]]))
    else:
        answare = "No user with this name exists"
        messages_to_send.append((answare, current_socket))

def exit(current_socket):
    print("Connection closed")
    for i in list(all_names.keys()):
        if all_names[i] == current_socket:
            all_names.pop(i)

def deal_messages(current_socket):
    valid_msg, cmd = protocol.get_msg(current_socket)
    if valid_msg:
        words = cmd.split(" ")
        if words == [''] or words[0] == "EXIT":
            exit(current_socket)
            return True
        elif words[0] == "NAME":
            name(current_socket, words)
        elif words[0] == "GET_NAMES":
            get_names(current_socket)
        elif words[0] == "MSG":
            msg(current_socket,words)
        else:
            answare = "Invalid command"
            messages_to_send.append((answare, current_socket))
        answare = ""
        return False
    else:
        answare = "Longitude field is invalid"
        messages_to_send.append((answare, current_socket))
        return False


while True:
    """The sockets ready for reading are accepted into rlist"""
    rlist, wlist, elist = select.select([server_socket]+clients_list, clients_list, [])
    for current_socket in rlist:
        if current_socket is server_socket:
            connection, client_address = current_socket.accept()
            print("New client joined!", client_address)
            clients_list.append(connection)
        else:
            print("Data from existing client\n")
            if deal_messages(current_socket):
                clients_list.remove(current_socket)
                current_socket.close()
    for message in messages_to_send:
        data, current_socket = message
        if current_socket in wlist:
            current_socket.send(protocol.add_length_field(data).encode())
            messages_to_send.remove(message)
