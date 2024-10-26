import sys

def lister():
    """This function lists operations on each line. Return format: [[operand1, operator, operand2]...]"""
    input_file = open(sys.argv[1])
    input_list = [lines.split() for lines in input_file]
    for i in range(input_list.count([])):
        input_list.remove([])   #Deleting free lines.

    input_file.close()
    return input_list

def calculator(operation_list):
    """This function calculates the operation which is given as argument(operation_list)"""
    operand1, operand2, str_operator = float(operation_list[0]), float(operation_list[2]), operation_list[1]
    if str_operator == "+":
        return operand1 + operand2
    elif str_operator == "-":
        return operand1 - operand2
    elif str_operator == "*":
        return operand1 * operand2
    elif str_operator == "/":
        return operand1 / operand2

def main():
    if len(sys.argv) == 3:   # 2 command-line argument check

        try:                 # To find out if there exists the input file
            input_file = open(sys.argv[1])
            input_list = lister()
            output_file = open(sys.argv[2], mode="w")
            counter = 0
            for operations in input_list:
                counter += 1

                if len(operations) == 3:  # To find out whether three object is given on same line.

                    try:                  # To find out whether the first operand is string or not.
                        operations[0] = float(operations[0]) if float(operations[0])!=int(float(operations[0])) else int(operations[0])
                        operations[0] = str(operations[0])

                        try:              # To find out whether the second operand is string or not.
                            operations[2] = float(operations[2]) if float(operations[2])!=int(float(operations[2])) else int(operations[2])
                            operations[2] = str(operations[2])

                            if operations[1] in ["+","-","*","/"]:   # To find out if operator is valid or not.
                                output_file.write(" ".join(operations) + "\n")
                                """Since everything is valid, calculator function is able to be called."""
                                output_file.write(f"={'%.2f' % calculator(operations)}")

                                if counter != len(input_list): # Not important (to make outputs identical)
                                    output_file.write("\n")
                                    output_file.flush()
                                else:
                                    output_file.close()

                            else:
                                output_file.write(" ".join(operations) + "\n")
                                output_file.write("ERROR: There is no such an operator!\n")

                        except ValueError:
                            output_file.write(" ".join(operations) + "\n")
                            output_file.write("ERROR: Second operand is not a number!\n")

                    except ValueError:
                        output_file.write(" ".join(operations) + "\n")
                        output_file.write("ERROR: First operand is not a number!\n")

                else:
                    output_file.write(" ".join(operations)+"\n")
                    output_file.write("ERROR: Line format is erroneous!\n")

        except FileNotFoundError:
            print(f"ERROR: There is either no such a file namely {sys.argv[1]} or this program does not have permission to read it!")
            print("Program is going to terminate!")

    else:
        print("ERROR: This program needs two command line arguments to run, where first one is the input file and the second one is the output file!")
        print("Sample run command is as follows: python3 calculator.py input.txt output.txt")
        print("Program is going to terminate!")

if __name__ == "__main__":
    main()