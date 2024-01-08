#by Naama Iluz ID 212259204
import socket

PORT = 1234

def add_length_field(command):
    """Create a valid protocol message, with length field"""
    command = str(len(command)).zfill(2) + command
    return command


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    data_length = my_socket.recv(2).decode()
    if not data_length.isdigit():
        return False, ""
    data = my_socket.recv(int(data_length)).decode()
    return True, data