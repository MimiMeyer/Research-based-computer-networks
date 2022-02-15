# assignment 1 Miriam Meyer 317924835
def prints_value(v):
    print("You entered the number:", v)  # printing the number


def prints_digits(v):
    string = "The digits of this number are: {}".format(v[0])
    for i in range(1, len(v)):
        string += "," + v[i]
    print(string)  # printing the digits


def prints_sum(v):
    summary = 0  # initializing
    for i in v:
        summary += int(i)  # summing up
    print("The sum of the digits is:", summary)  # printing the sum


def main():
    val = input("Please enter a 5 digit number\n")  # receiving the input
    prints_value(val)  # printing the number
    prints_digits(val)  # printing the digits
    prints_sum(val)  # printing the sum


if __name__ == "__main__":
    main()
