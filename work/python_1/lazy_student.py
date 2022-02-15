# Mimi (Miriam) Meyer 317924835 lazy_student
import sys
import os
import operator


def check_params(params):
    """checks parameters that user entered if th files exist will return true"""
    num_of_params = 3
    if len(params) != num_of_params:  # making sure the user only put in two arguments
        return False, "Error, must enter two arguments"
    # checking the user put in files that exist
    if not os.path.isfile(params[1]) or not os.path.isfile(params[2]):
        return False, "Error, the files must exist"
    else:
        return True, "work"


def check_line(line):
    """ checks line to see if in right format number-space-operator-space-number"""
    operations: str = "+-/*"
    wanted_data = line.split(" ", 2)  # will split at space, maximum splits into 3
    wanted_len = 3  # wanted length of wanted_data [num, op ,num]
    if wanted_len != len(wanted_data):  # less then 2 spaces
        return False, "Error, must be in the format of num-space-operator-space-num"
    for i in wanted_data:  # if there's still a space then there is more then 2 spaces
        if ' ' in i:
            return False, "Too many spaces"
    if not wanted_data[0].isdigit() or not wanted_data[2].isdigit():
        return False, "Error, positive digits only no letters"
    if wanted_data[1] not in operations:
        return False, "Error, operator must be one of  + - * / "
    if wanted_data[1] == "/" and wanted_data[2] == "0":
        return False, "Error, can't divide number by zero"
    else:
        return True, wanted_data


def calc_line(line):
    """returns the calculated equation """
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    return round(ops[line[1]](int(line[0]), int(line[2])))


def asserts():
    """checking that the functions function the way there are supposed too"""
    try:
        user_input = ['C:/Networks/work/lazy_student.py', 'homework.txt', 'solutions.txt']
        assert check_params(user_input)[0], "Assertion Error, check_params"
        assert check_line("0 + 5")[0], "Assertion Error, check_line"
        assert calc_line(['0', '+', '5']) == 5, "Assertion Error, calc_line"
    except AssertionError as error:
        print(error)


def main():
    asserts()
    check_params_response = check_params(sys.argv)
    if check_params_response[0]:  # if the files are correct
        input_file = open(sys.argv[1], 'r')
        output_file = open(sys.argv[2], 'w')
        for line in input_file:
            line = line.rstrip(os.linesep)  # removing end line from line
            cl_response = check_line(line)  # getting the response if the line is in thr right format
            if cl_response[0]:
                # if the line was in the right format
                output_file.write(line + " = " + str(calc_line(cl_response[1])) + "\n")
            else:
                output_file.write(cl_response[1] + "\n")  # printing error message to file
    else:
        print(check_params_response[1])  # printing error message to user


if __name__ == "__main__":
    main()
