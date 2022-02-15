
#   Ex. 2.7 template - protocol
# Mimi Meyer 317924835

LENGTH_FIELD_SIZE = 4
PORT = 8820
command_words = ("DIR", "DELETE", "COPY", "EXECUTE", "SEND_PHOTO", "TAKE_SCREENSHOT", "EXIT")


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\\work\\file.txt is good, but DELETE alone is not
    """
    no_params = 1
    one_param = 2
    two_params = 3
    split_data = data.split()
    # if the command is exit , take_screenshot or send_photo shouldn't have any parameters
    if split_data[0] == command_words[4] or split_data[0] == command_words[5] or split_data[0] == command_words[6]:
        if len(split_data) == no_params:
            return True
    # if the command is dir , delete or execute should only have one parameter
    if split_data[0] == command_words[0] or split_data[0] == command_words[1] or split_data[0] == command_words[3]:
        if len(split_data) == one_param:
            return True
    # if the command is copy should only have two parameters
    if split_data[0] == command_words[2]:
        if len(split_data) == two_params:
            return True
    else:
        # not one of the commands or not in the right amount of parameters
        return False


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """
    length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    return (length + data).encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """
    number = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if number.isdigit():
        return True, my_socket.recv(int(number)).decode()
    else:
        return False, "Error"
