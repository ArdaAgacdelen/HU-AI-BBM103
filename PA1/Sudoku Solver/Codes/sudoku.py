import sys

def list_rows(input_sudoku):
    """This Function separates the input sudoku line by line and puts the cells in a common row list.
    Then, returns a main list that includes all rows from top to bottom, respectively."""

    rows_list = []
    for lines in input_sudoku:
        row = lines.split()
        rows_list.append(row)
    return rows_list

def list_columns(rows_list):
    """This function classify cells inside rows according to which column it belongs to and puts in a common column list.
    Then, returns a main list that includes all columns from left to right, respectively."""

    columns_list = [[] for i in range(9)]
    for rows in rows_list:
        for index in range(9):                       # Index of a cell in row must be same with a column list index
            columns_list[index].append(rows[index])  # in columns_list for any same cell.
    return columns_list

def list_blocks(rows_list):
    """This function classify cells inside rows according to which block it belongs to and puts in a common block list.
    Then, returns a main list that includes all blocks first from left to right,then downward, respectively."""

    blocks_list = [[] for i in range(9)]
    for rows in rows_list[0:3]:           # classify the blocks for first three row.
        blocks_list[0].extend(rows[0:3])  # put into the indexes 0, 1, 2 for blocks_list
        blocks_list[1].extend(rows[3:6])
        blocks_list[2].extend(rows[6:9])

    for rows in rows_list[3:6]:           # classify the blocks for last three row.
        blocks_list[3].extend(rows[0:3])  # put into the indexes 3, 4, 5 for blocks_list
        blocks_list[4].extend(rows[3:6])
        blocks_list[5].extend(rows[6:9])

    for rows in rows_list[6:9]:           # classify the blocks for last three row.
        blocks_list[6].extend(rows[0:3])  # put into the indexes 6, 7, 8 for blocks_list
        blocks_list[7].extend(rows[3:6])
        blocks_list[8].extend(rows[6:9])
    return blocks_list

def find_row(place):
    """This function finds for given cell (numbered 1 to 81 (first from left to right,then downward)) which row it
    belongs to. """
    if place % 9 == 0:
        return place // 9
    else:
        return (place // 9) + 1

def find_column(place):
    """This function finds for given cell (numbered 1 to 81) which column it belongs to. """
    if place % 9 == 0:
        return 9
    else:
        return place % 9

def find_block(place):
    """This function finds for given cell (numbered 1 to 81) which block it belongs to. """
    row = find_row(place)
    column = find_column(place)
    if row in [1, 2, 3]:
        if column in [1, 2, 3]:
            return 1
        elif column in [4, 5, 6]:
            return 2
        else:
            return 3

    if row in [4, 5, 6]:
        if column in [1, 2, 3]:
            return 4
        elif column in [4, 5, 6]:
            return 5
        else:
            return 6

    else :
        if column in [1, 2, 3]:
            return 7
        elif column in [4, 5, 6]:
            return 8
        else:
            return 9

def possible_value(place, rows_list, columns_list, blocks_list):
    """This function returns a list that includes "possible values" for given cell (numbered 1 to 81) via checking which
    digits are already exist in its row, column and block."""
    values_found = []
    possible_values = []
    if rows_list[find_row(place)-1][find_column(place)-1] == "0" :  # checking whether given cell is empty.
        for i in range(1,10):
            if str(i) in rows_list[find_row(place)-1]:
                values_found.append(str(i))                         # save existing digits in the same row.

            elif str(i) in columns_list[find_column(place)-1]:
                values_found.append(str(i))                         # save existing digits in the same column.

            elif str(i) in blocks_list[find_block(place)-1]:
                values_found.append(str(i))                         # save existing digits in the same block.

        for i in range(1,10):
            if not str(i) in values_found:
                possible_values.append(str(i))
    return possible_values

def empty_cell_check(rows_list):
    """This function looks for if there is any free cell; if there is, returns True and else, returns False."""
    feedback = False
    for rows in rows_list:
        if "0" in rows:
            feedback = True
    return feedback

def main():
    rows_list = list_rows(open(sys.argv[1]))
    columns_list = list_columns(rows_list)
    blocks_list = list_blocks(rows_list)
    output_file = open(sys.argv[2], mode="w")
    step_counter = 1

    while empty_cell_check(rows_list):  # Stay in the loop while there is at least one empty cell.
        for place in range(1,82):
            if len(possible_value(place, rows_list, columns_list, blocks_list)) == 1: #
                # Find empty cells which have only one possible digit to fill.
                new_value = (possible_value(place, rows_list, columns_list, blocks_list))[0]

                rows_list[find_row(place) - 1][find_column(place)-1] = new_value  # Put new value into rows_list
                columns_list = list_columns(rows_list)                            # Put new value into columns_list
                blocks_list = list_blocks(rows_list)                              # Put new value into blocks_list

                output_file.write(18*"-")
                output_file.write("\n")
                output_file.write(f"Step {step_counter} - {new_value} @ R{find_row(place)}C{find_column(place)}")
                output_file.write("\n")
                output_file.write(18 * "-")

                for rows in rows_list:          # Visualize the current sudoku
                    output_file.write("\n")
                    x = 0
                    for cells in rows:
                        output_file.write(cells)
                        x += 1
                        if not x == 9:
                            output_file.write(" ")
                output_file.write(("\n"))
                step_counter += 1
                break                        # Break the for loop to start from the initial cell when a cell is changed.

    output_file.write(18*"-")
    output_file.flush()
    output_file.close()

if __name__ == "__main__":
    main()