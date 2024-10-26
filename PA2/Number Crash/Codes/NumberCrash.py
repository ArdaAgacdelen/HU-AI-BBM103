import sys

def initial_rows_list(txt):
    """This function lists the initial states of rows."""
    return_list = [row.split() for row in txt]
    for rows in return_list:           #Turn values into integer from string.
        for index in range(len(rows)):
            rows[index] = int(rows[index])
    return return_list

def rows_to_columns(rows_list):
    """This function creates/changes global list of columns from the given argument (current list of rows)."""
    global columns_list
    columns_list = [[] for i in range(len(rows_list[0]))] if len(rows_list) != 0 else []
    for rows in rows_list:
        for index in range(len(rows)):
            columns_list[index].append(rows[index])

def columns_to_rows(columns_list):
    """This function creates/changes global list of rows from the given argument (current list of columns)."""
    global rows_list
    rows_list = [[] for i in range(len(columns_list[0]))] if len(columns_list) != 0 else []
    for lists in columns_list:
        for index in range(len(lists)):
            rows_list[index].append(lists[index])

def value_founder(location, rows_list):
    """This function finds the current value at the given location (location format: (row-number, column-number))"""
    return rows_list[location[0]-1][location[1]-1]

def adjacent_finder(location, rows_list, columns_list):
    """This function returns the adjacents of given location if there exists. (return type: Tuple)"""
    given_row, given_column = location[0], location[1]

    upper_location = (given_row - 1, given_column) if given_row != 1 else None
    lower_location = (given_row + 1, given_column) if given_row != len(rows_list) else None
    right_location = (given_row, given_column + 1) if given_column != len(columns_list) else None
    left_location = (given_row, given_column - 1) if given_column != 1 else None
    return (upper_location, lower_location, right_location, left_location)

def slider():
    """This function slides down the numbers if there is space below and deletes empty rows and columns if there is."""
    for columns in columns_list:    #Put all spaces(means empty) to the beginning of the columns to slide down the numbers.
        if " " in columns:
            free_cell_amount = columns.count(" ")
            for i in range(free_cell_amount):
                columns.remove(" ")
            for i in range(free_cell_amount):
                columns.insert(0," ")
    columns_to_rows(columns_list)    #Since sliding operation is done in columns-list, we also need to update rows-list.

    empty_index, k = [], 0
    for row_index in range(len(rows_list)):
        if rows_list[row_index].count(" ") == len(rows_list[row_index]): #All elements of row is " "(means an empty row).
            empty_index.append(row_index)
    for i in empty_index:    #Delete all rows which are detected as empty.
        rows_list.pop(i-k)
        k += 1
    rows_to_columns(rows_list)  #Since deleting operation is done in rows-list, we also need to update columns-list.

    """Delete empty columns with the same method as used above."""
    empty_index, k = [], 0
    for column_index in range(len(columns_list)):
        if columns_list[column_index].count(" ") == len(columns_list[column_index]):
            empty_index.append(column_index)
    for i in empty_index:
        columns_list.pop(i-k)
        k += 1
    columns_to_rows(columns_list) #Since deleting operation is done in columns-list, we also need to update rows-list.

def cleaner(location):
    """This function deletes the number at the given location and returns the deleted number."""
    global rows_list
    number_cleaned = rows_list[location[0]-1].pop(location[1]-1)
    rows_list[location[0] - 1].insert(location[1] - 1, " ")
    return number_cleaned

def writer(rows_list):
    "This function prints the current statement of the game."
    for rows in rows_list:
        print(*rows, sep=" ")

def game_over():
    """This function checks if there are any possible moves remaining. If there is, returns True; If there is not, returns False."""

    """Check for every location if there is an adjacent which is equal. (except free cells(" "))"""
    check_list = [(row_index+1,column_index+1) for row_index in range(len(rows_list)) for column_index in range(len(columns_list))]
    for locations in check_list:
        for adjacents in adjacent_finder(locations, rows_list, columns_list):
            if adjacents != None:
                if value_founder(locations, rows_list) == value_founder(adjacents, rows_list) and value_founder(locations, rows_list) != " " :
                    return True

    return False

rows_list = initial_rows_list(open(sys.argv[1]))
rows_to_columns(rows_list)
score = []
writer(rows_list)
print()
print("Your score is: 0")
print()
while game_over():
    input_value = input("Please enter a row and a column number: ")
    print()
    given_location = tuple([int(i) for i in input_value.split()])
    if given_location[0] == 0 or given_location[0] > len(rows_list) or given_location[1]==0 or given_location[1] > len(columns_list) or value_founder(given_location, rows_list) == " ":
        print("Please enter a correct size!")
        print()
        continue

    garbage_list = [given_location] #Locations that will be deleted if there is same-value adjacents.
    for locations in garbage_list:
        for adjacents in adjacent_finder(locations, rows_list, columns_list):
            if adjacents != None and not adjacents in garbage_list:
                if value_founder(given_location, rows_list) == value_founder(adjacents, rows_list) :
                    garbage_list.append(adjacents)

    if len(garbage_list) == 1:      #This conditional means there is no same-value adjacent.
        print("No movement happened try again")
        print()
        writer(rows_list)
        print()
        print(f"Your score is: {sum(score)}")
        print()
        continue

    total = [cleaner(garbages) for garbages in garbage_list] #Clean the cells and store cleaned values in this step.
    score.extend(total)   #All cleaned numbers are stored in score-list from begginning to this step to calculate current score.
    rows_to_columns(rows_list) #Since the cleaning operation is done in rows-list, we also need to update columns-list.
    slider()
    writer(rows_list)
    print() if rows_list != [] else None
    print(f"Your score is: {sum(score)}")
    print()

print("Game Over")