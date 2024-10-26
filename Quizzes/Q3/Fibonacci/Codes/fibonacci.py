value_list = [1, 1]
def fibonacci_eager(n,output_eager):
    """This function calculates the nth fibonacci number and updates the value list with every fibonacci numbers
     starting from 1 to the given number (n) to reach when it is needed again."""
    global value_list
    try:   # Checks whether nth fibonacci number calculated before or not.
        if n == 1 or n == 2:
            output_eager.write(f"fib({n}) = 1\n")
            return 1
        output_eager.write(f"fib({n}) = {value_list[n-1]}\n")
        return value_list[n-1]
    except IndexError:    # In case given fibonacci number is not calculated before.
         output_eager.write(f"fib({n}) = fib({n - 1}) + fib({n - 2})\n")
         first, second = fibonacci_eager(n-1, output_eager), fibonacci_eager(n-2, output_eager) # Recursive part
         value_list.append(first + second)
         return first + second

def fibonacci_naive(n, output_naive):
    """This function calculates the nth fibonacci number, recursively. Function does not save calculated fibonacci
    numbers, so it is not proper for big numbers. """
    if n == 1 or n == 2:
        output_naive.write(f"fib({n}) = 1\n")
        return 1
    else:
        output_naive.write(f"fib({n}) = fib({n-1}) + fib({n-2})\n")
        return fibonacci_naive(n-1, output_naive) + fibonacci_naive(n-2, output_naive) # Recursive part

def main():
    import sys
    input_file = open(sys.argv[1])
    output_naive = open(sys.argv[2], mode="w")
    output_eager = open(sys.argv[3], mode="w")

    for lines in input_file:
        f_number = int(lines.split()[0])  # Reaching input number on the line as an integer.

        output_eager.write("-" * 32 + "\n")
        output_naive.write("-" * 32 + "\n")
        output_eager.write(f"Calculating {f_number}. Fibonacci number:" + "\n")
        output_naive.write(f"Calculating {f_number}. Fibonacci number:" + "\n")

        if f_number <= 0:
            output_naive.write("ERROR: Fibonacci cannot be calculated for the non-positive numbers!\n")
            output_eager.write("ERROR: Fibonacci cannot be calculated for the non-positive numbers!\n")
            output_naive.write(f"{f_number}. Fibonacci number is: nan\n")
            output_eager.write(f"{f_number}. Fibonacci number is: nan\n")

        else:
            output_naive.write(f"{f_number}. Fibonacci number is: {fibonacci_naive(f_number, output_naive)}\n")
            output_eager.write(f"{f_number}. Fibonacci number is: {fibonacci_eager(f_number, output_eager)}\n")

    output_eager.write("-" * 32 + "\n")
    output_naive.write("-" * 32)
    output_eager.write(f"Structure for the eager solution:\n{value_list}\n" + "-"*32)

    input_file.close()
    output_eager.close()
    output_naive.close()

if __name__ == "__main__":
    main()