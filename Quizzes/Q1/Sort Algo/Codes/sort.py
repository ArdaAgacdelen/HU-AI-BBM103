def input_to_list(input_file):
    """This function lists the given numbers in integer type."""
    input_list = []
    for lines in input_file:
        input_list.extend((lines.split()))
    #As we take numbers from a txt, type of listed numbers is string. Following loop changes the type into integer.
    for i in range(len(input_list)):
        input_list[i] = int(input_list[i])

    return input_list

def bubble_checker(first_number,second_number):
    """This function checks whether inside of 'bubble' is in the correct order."""
    if first_number > second_number:
        return False
    else:
        return True

def order_check(list):
    """This function checks whether content of the list is in the correct order."""
    return_value = True
    #The following loop checks for each number, except the last one, whether the numbers following it are smaller.
    for i in range(len(list)-1):
        for j in range(i+1, len(list)):
            if list[i] > list[j]:
                return_value = False
    return return_value

def one_step_bubble_sort(list):
    """This function sorts each 'bubble' which is possible in just one step; does not start again from beginning of list."""
    for i in range(len(list) - 1):
        #Following condition reverses integers in bubble, if inside of the bubble is not in the correct order.
        if not bubble_checker(list[i], list[i + 1]):
            bubble_number1 = list.pop(i)
            list.insert(i + 1, bubble_number1)
    return(list)

def main():
    import sys

    input_list = input_to_list(open(sys.argv[1]))
    output_bubble = open(sys.argv[2], mode="w")
    output_insert = open(sys.argv[3], mode="w")

    if not order_check(input_list):

        #Bubble sort part
        pass_counter = 1
        while not order_check(input_list):
            input_list = one_step_bubble_sort(input_list)
            #Write current pass and list after 'one step bubble sort'.
            output_bubble.write(f"Pass {pass_counter}:")
            for integers in input_list:
                output_bubble.write(f" {integers}")
            if not order_check(input_list):
                output_bubble.write("\n")

            pass_counter += 1

        #Insertion sort part
        input_list = input_to_list(open(sys.argv[1])) #Reset list to unsorted version.
        sublist = []
        pass_counter = 1

        """To create a sub-list and start insertion sort, check if first two element is sorted or not. If it is, write
        directly as a step; else, reverse them and write as a step."""
        if input_list[0] > input_list[1]:
            sublist.extend([input_list[1], input_list[0]])
            input_list[0:2] = sublist

            #Writing part
            output_insert.write(f"Pass {pass_counter}:")
            for integers in input_list:
                output_insert.write(f" {integers}")
            if not order_check(input_list):
                output_insert.write("\n")

            pass_counter += 1

        else:
            sublist.extend(input_list[0:2])

            #Writing part
            output_insert.write(f"Pass {pass_counter}:")
            for integers in input_list:
                output_insert.write(f" {integers}")
            if not order_check(input_list):
                output_insert.write("\n")

            pass_counter += 1

        while not order_check(input_list):
            """After creating two-element-sublist from first two element of input list, insert the remaining elements."""
            for i in range(2, len(input_list)):
                for j in range(len(sublist)):
                    #Place the element just before the integer which is greater than or equal to it, in the sub list.
                    if input_list[i] <= sublist[j]:
                        sublist.insert(j, input_list[i])
                        input_list[0:len(sublist)] = sublist #Update sub-list part in input list.

                        #Writing part
                        output_insert.write(f"Pass {pass_counter}:")
                        for integers in input_list:
                            output_insert.write(f" {integers}")
                        if not order_check(input_list):
                            output_insert.write("\n")

                        pass_counter += 1
                        break
                    #If there is not a greater integer then this element, place it at the end of the sub-list.
                    elif input_list[i] > sublist[-1]:
                        sublist.append(input_list[i])

                        #Writing part
                        output_insert.write(f"Pass {pass_counter}:")
                        for integers in input_list:
                            output_insert.write(f" {integers}")
                        if not order_check(input_list):
                            output_insert.write("\n")

                        pass_counter += 1
                        break
                """Following condition, controls the list after every single bubble change, to find out whether the list
                is sorted."""
                if order_check(input_list):
                    break
    else:
        output_insert.write("Already sorted!")
        output_bubble.write("Already sorted!")

if __name__ == "__main__":
    main()