"""EX 2.6 server implementation
   Author: Miriam Meyer 317924835
   Date:29/10/2021
"""

import socket
from ex26 import protocol


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")
    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print(cmd)
            # 2. Check if the command is valid
            valid_command = protocol.check_cmd(cmd)
            # 3. If valid command - create response
            if valid_command:
                response = protocol.create_server_rsp(cmd)
            else:
                response = "Wrong command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client
        if cmd == "EXIT":
            break
        # Send response to the client
        else:
            # adding the length to the word
            msg_response = protocol.create_msg(str(response))
            client_socket.send(str(msg_response).encode())

    print("Closing\n")
    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
