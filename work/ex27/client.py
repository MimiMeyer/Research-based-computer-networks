#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
# Mimi Meyer 317924835

import socket
import ast
from ex27 import protocol as protocol_solution

IP = "127.0.0.1"
# The path + filename where the copy of the screenshot at the client should be saved
SAVED_PHOTO_LOCATION = "C:\\Networks\\work\\ex27\\screen_user.jpg"


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # treat all responses except SEND_PHOTO
    bad_msg = "Bad command or parameters"
    send_photo_error = "Need to take screenshot first"
    valid_msg, msg = protocol_solution.get_msg(my_socket)
    if valid_msg:
        # if command is dir and is legals
        if protocol_solution.command_words[0] in cmd and bad_msg != msg:
            msg = ast.literal_eval(msg)
            for file_name in msg:
                print(file_name)
        # treat SEND_PHOTO
        elif protocol_solution.command_words[4] in cmd and send_photo_error != msg:
            data = my_socket.recv(int(msg))  # getting the data from server
            file = open(SAVED_PHOTO_LOCATION, 'wb')
            file.write(data)
            file.close()
        else:
            print(msg)
    else:
        print("not a valid message")


def main():
    # open socket with the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((IP, protocol_solution.PORT))
    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol_solution.check_cmd(cmd):
            packet = protocol_solution.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()
