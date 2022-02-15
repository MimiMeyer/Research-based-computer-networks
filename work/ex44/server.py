# Miriam Meyer 317924835
# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os

# TO DO: set constants
DEFAULT_URL = "C:/Networks/work/ex44/webroot"
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.1
special_files = {'/blah.txt': "HTTP/1.1 403 Forbidden\r\n",
                 '/page1.txt': "HTTP/1.1 302 Moved Temporarily\r\nLocation: /index.html\r\n"}
bytes_needed = 1024


def get_file_data(filename):
    """ Get data from file """
    if os.path.isfile(filename):  # if file exists open
        if "imgs" in filename:  # if file is in imgs need to be rb
            with open(filename, 'rb') as f:
                data = f.read()
        else:
            with open(filename, encoding='utf-8') as f:
                data = f.read()
        return data
    else:
        return "Error"


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    if resource == '/':
        url = DEFAULT_URL + "/index.html"
    else:
        url = resource
    # TO DO: check if URL had been redirected, not available or other error code. For example:
    if url in special_files:
        # TO DO: send 302, 403 redirection response
        http_response = special_files[url]
        client_socket.send(http_response.encode())
    # TO DO: extract requested file type from URL (html, jpg etc)
    else:
        http_header = ""  # initializing
        url_split = url.split(".")
        filetype = url_split[-1]
        if url == DEFAULT_URL + "/index.html":
            filename = url
        else:
            filename = DEFAULT_URL + url
        data = get_file_data(filename)  # getting the data
        if data == "Error":  # file doesn't exist
            http_header = 'HTTP/1.1 404 Not Found\r\n'
        # TO DO: generate proper HTTP header
        elif filetype == 'html' or filetype == 'txt':
            http_header = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: " \
                          + str(len(data)) + "\r\n\r\n"
        # TO DO: generate proper jpg header
        elif filetype == 'jpg':
            http_header = "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: " \
                          + str(len(data)) + "\r\n\r\n"
        # TO DO: handle all other headers
        # TO DO: generate proper js header
        elif filetype == 'js':
            http_header = "HTTP/1.1 200 OK\r\nContent-Type: text/javascript; charset=UTF-8\r\nContent-Length: " \
                          + str(len(data)) + "\r\n\r\n"
        # TO DO: generate proper css header
        elif filetype == 'css':
            http_header = "HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: " \
                          + str(len(data)) + "\r\n\r\n"
        elif filetype == 'ico':
            http_header = "HTTP/1.1 200 OK\r\nContent-Type: image/x-icon\r\nContent-Length: " \
                          + str(len(data)) + "\r\n\r\n"

        # TO DO: read the data from the file
        if "imgs" in filename:  # data is in bytes so no need to encode the data just the header
            http_response = http_header.encode() + data
            client_socket.send(http_response)
        else:
            http_response = http_header + data
            client_socket.send(http_response.encode())
    return


def validate_http_request(request):
    """ Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL """
    # TO DO: write function
    length_of_request = 3
    request_split = request.split(" ")
    # checking of valid http request
    if len(request_split) == length_of_request and request_split[0] == "GET" and request_split[2] == "HTTP/1.1\r\n":
        return True, request_split[1]
    else:
        # not a valid http request
        return False, "HTTP/1.1 500 Internal Server Error\r\n"


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')

    while True:
        # TO DO: insert code that receives client request
        # ...
        full_client_request = client_socket.recv(bytes_needed).decode()
        client_request = full_client_request.splitlines(True)[0]  # getting the first line with \r\n
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            client_socket.send(resource.encode())  # send 500 Internal Server Error
            print('Error: Not a valid HTTP request')
            break

    print('Closing connection')
    client_socket.close()
    return


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print('New connection received')
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_client(client_socket)
        except Exception as error:
            print(error)


if __name__ == "__main__":
    # Call the main handler function
    main()
