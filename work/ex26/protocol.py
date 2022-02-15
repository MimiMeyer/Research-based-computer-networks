"""EX 2.6 protocol implementation
   Author: Miriam Meyer 317924835
   Date:29/10/2021
"""
from datetime import datetime
import random

LENGTH_FIELD_SIZE = 2
PORT = 8820
command_words = ("TIME", "NAME", "RAND", "EXIT")


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    if data in command_words:
        return True
    else:
        return False


def create_msg(data):
    """Create a valid protocol message, with length field"""
    length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    return length + data


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    number = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if number.isdigit():
        return True, my_socket.recv(int(number)).decode()
    else:
        return False, "Error"


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == command_words[0]:
        # returning the current time
        return datetime.now()
    if cmd == command_words[1]:
        # returning a name I chose
        return "Mimi_Server"
    if cmd == command_words[2]:
        # returning random number from 1 to 10
        return random.randint(1, 10)
    else:
        return
