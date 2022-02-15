#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
# Mimi Meyer 317924835

import socket
import os
import glob
import shutil
import subprocess
import pyautogui
from ex27 import protocol

IP = "0.0.0.0"
# The path + filename where the screenshot at the server should be saved
PHOTO_PATH = "C:\\Networks\\work\\ex27\\screen_server.jpg"


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    response = False, "Error", "blah"
    # Use protocol.check_cmd first
    if protocol.check_cmd(cmd):
        # Then make sure the params are valid
        split_cmd = cmd.split()
        # if command is Dir check if param is directory
        if split_cmd[0] == protocol.command_words[0]:
            if os.path.isdir(split_cmd[1]):
                response = True, split_cmd[0], split_cmd[1]
        # if command is delete check if param is file
        elif split_cmd[0] == protocol.command_words[1]:
            if os.path.isfile(split_cmd[1]):
                response = True, split_cmd[0], split_cmd[1]
        # if command is copy check if fist param is file and if the second file it doesn't exist create it
        elif split_cmd[0] == protocol.command_words[2]:
            if os.path.isfile(split_cmd[1]):
                if os.path.isfile(split_cmd[2]):
                    response = True, split_cmd[0], (split_cmd[1], split_cmd[2])
                else:
                    open(split_cmd[2], 'w')
                    response = True, split_cmd[0], (split_cmd[1], split_cmd[2])
        # if command is execute check if param is an executable file
        elif split_cmd[0] == protocol.command_words[3]:
            if os.access(split_cmd[1], os.X_OK):
                response = True, split_cmd[0], split_cmd[1]
            # if the command is exit, take_screenshot or send_photo don't need to check params
        else:
            response = True, split_cmd[0], "blah"
    return response


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        response: the requested data

    """
    # dir
    if command == protocol.command_words[0]:
        response = glob.glob(params+"/*")
    # delete
    elif command == protocol.command_words[1]:
        os.remove(params)
        response = 'file deleted successfully'
    # copy
    elif command == protocol.command_words[2]:
        try:
            shutil.copy(params[0], params[1])
            response = 'file copied successfully'
        # If source and destination are same
        except shutil.SameFileError:
            response = "Source and destination represents the same file."
        # For other errors
        except shutil.Error:
            response = "Error occurred while copying file."
    # execute
    elif command == protocol.command_words[3]:
        try:
            subprocess.call(params)
            response = 'file executed successfully'
        except PermissionError:
            response = "can't execute requested file PermissionError."
        except subprocess.CalledProcessError:
            response = "can't execute requested file CalledProcessError."
        except OSError:
            response = "not a valid Win32 application"
    # take screenshot
    elif command == protocol.command_words[5]:
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        response = 'Screnshot taken'
    # exit
    elif command == protocol.command_words[6]:
        response = 'EXIT successful'
    # send photo
    else:
        if os.path.isfile(PHOTO_PATH):
            response = PHOTO_PATH
        else:
            response = "Need to take screenshot first"
    return response


def main():
    # open socket with client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen()
    print("server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("client connected")
    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                # prepare a response using "handle_client_request"
                response = handle_client_request(command, params)
                # Exit
                if command == protocol.command_words[6]:
                    # add length field using "create_msg
                    msg_response = protocol.create_msg(str(response)).decode()
                    # send to client
                    client_socket.send(str(msg_response).encode())
                    break
                # save_photo
                if response == PHOTO_PATH:
                    msg_response = protocol.create_msg(str(os.path.getsize(response))).decode()
                    # Send the data itself to the client
                    file = open(response, "rb")
                    data = file.read()
                    client_socket.send(msg_response.encode())  # sending the length
                    client_socket.send(data)  # sending the data of the file
                    file.close()
                else:
                    # add length field using "create_msg
                    msg_response = protocol.create_msg(str(response)).decode()
                    # send to client
                    client_socket.send(str(msg_response).encode())

            else:
                # prepare proper error to client
                response = 'Bad command or parameters'
                msg_response = protocol.create_msg(str(response)).decode()
                # send to client
                client_socket.send(str(msg_response).encode())

        else:
            # prepare proper error to client
            response = 'Packet not according to protocol'
            msg_response = protocol.create_msg(str(response)).decode()
            # send to client
            client_socket.send(str(msg_response).encode())
            # Attempt to clean garbage from socket
            client_socket.recv(1024)

    # close sockets
    print("Closing connection")
    client_socket.close()
    server_socket.close()


if __name__ == '__main__':
    main()
