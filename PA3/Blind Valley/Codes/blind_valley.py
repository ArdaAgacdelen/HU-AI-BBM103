"""Since we cannot define functions in main(), functions can not reach variables which are defined in main.
I cannot found a way except giving them as parameters, so some of them takes quite many. """

def restrictions(input_file):
    """This function takes restrictions from file."""
    input_file.seek(0)
    restriction = [input_file.readline().split() for i in range(4)]
    return restriction


def brick_packages(input_file):
    """This function puts cells and their brick-adjacents in a tuple and returns a list which includes all tuples."""
    input_file.seek(0)
    for i in range(4):
        input_file.readline()
    bricks_list = [lines.split() for lines in input_file]
    counter = 0   # Counter for cells
    brick_packages_list = []
    for rows in bricks_list:
        for cells in rows:
            counter += 1
            if cells == "L":
                brick_packages_list.append((counter, counter + 1))
            elif cells == "U":
                brick_packages_list.append((counter, counter + len(bricks_list[0])))
    return brick_packages_list


def brick_adjacent_finder(place, brick_adjacent_list):
    """This function finds brick-adjacent of the given cell."""
    brick_adjacent = 0
    for bricks in brick_adjacent_list:
        if place in bricks:
            brick_adjacent = bricks[0] if bricks[1] == place else bricks[1]
    return brick_adjacent


def find_row_column(place, how_many_column):
    """This function finds row and column number for the given cell."""
    if place % how_many_column == 0:
        return place // how_many_column, how_many_column
    else:
        return (place // how_many_column) + 1, place % how_many_column


def adjacent_finder(place, how_many_column, brick_adjacent_list):
    """This function returns adjacents' row and column information for given cell.
     (Brick-adjacent and lower location excluded)"""
    row, column = find_row_column(place, how_many_column)[0], find_row_column(place, how_many_column)[1]
    brick_adjacent_location = find_row_column(brick_adjacent_finder(place, brick_adjacent_list), how_many_column)

    upper_location = (row - 1, column) if row != 1 and (row - 1, column) != brick_adjacent_location else None
    right_location = (row, column + 1) if column != how_many_column and (row, column + 1) != brick_adjacent_location else None
    left_location = (row, column - 1) if column != 1 and (row, column - 1) != brick_adjacent_location else None
    return upper_location, right_location, left_location


def value_founder(location, current_state):
    """This function finds the value for the given cell."""
    row, column = location[0], location[1]
    return current_state[row - 1][column - 1]


def adjacent_values(place, how_many_column, brick_adjacent_list, current_state):
    """This function returns adjacents' values for the given cell in a list.(lower location excluded)"""
    adjacents_values = []
    for adjacents in adjacent_finder(place, how_many_column, brick_adjacent_list):
        if adjacents != None:
            adjacents_values.append(value_founder(adjacents, current_state))
    return adjacents_values


def is_finished(current_state, restrictions_list):
    """If game is finished return True; else, return False."""

    def column_list(current_state):
        """This function lists the columns."""
        columns_list = [[] for i in range(len(current_state[0]))] if len(current_state) != 0 else []
        for rows in current_state:
            for index in range(len(rows)):
                columns_list[index].append(rows[index])
        return columns_list

    columns_list = column_list(current_state) # To make it easy vertical control.

    for index in range(len(restrictions_list[0])):
        if int(restrictions_list[0][index]) >= 0:
            if current_state[index].count("H") != int(restrictions_list[0][index]):
                return False

    for index in range(len(restrictions_list[1])):
        if int(restrictions_list[1][index]) >= 0:
            if current_state[index].count("B") != int(restrictions_list[1][index]):
                return False

    for index in range(len(restrictions_list[2])):
        if int(restrictions_list[2][index]) >= 0:
            if columns_list[index].count("H") != int(restrictions_list[2][index]):
                return False

    for index in range(len(restrictions_list[3])):
        if int(restrictions_list[3][index]) >= 0:
            if not columns_list[index].count("B") == int(restrictions_list[3][index]):
                return False
    return True


def placer(index, current_state, restrictions_list, how_many_column, brick_adjacent_list, first, last):
    """This function tries all cases until reaching the solution or last case."""
    # index variable is used for cell's index in first.
    # first is a list which includes cell numbers that represent brick.
    place = first[index]

    if not is_finished(current_state, restrictions_list):
        if index < len(first) - 1:

            x = adjacent_values(place, how_many_column, brick_adjacent_list, current_state)
            y = adjacent_values(brick_adjacent_finder(place, brick_adjacent_list), how_many_column,
                                brick_adjacent_list, current_state)

            first_row, first_column = find_row_column(place, how_many_column)
            second_row, second_column = find_row_column(brick_adjacent_finder(place, brick_adjacent_list),
                                                        how_many_column)
            if not "H" in x and not "B" in y:
                current_state[first_row - 1][first_column - 1] = "H"
                current_state[second_row - 1][second_column - 1] = "B"

                if placer(index + 1, current_state, restrictions_list, how_many_column,
                          brick_adjacent_list, first, last):
                    return True

            if not "B" in x and not "H" in y:
                current_state[first_row - 1][first_column - 1] = "B"
                current_state[second_row - 1][second_column - 1] = "H"

                if placer(index + 1, current_state, restrictions_list, how_many_column,
                          brick_adjacent_list, first, last):
                    return True

            current_state[first_row - 1][first_column - 1] = "N"
            current_state[second_row - 1][second_column - 1] = "N"

            if placer(index + 1, current_state, restrictions_list, how_many_column, brick_adjacent_list,
                      first, last):
                return True




        elif place == last:  # last variable represents the last brick.
            x = adjacent_values(place, how_many_column, brick_adjacent_list, current_state)
            y = adjacent_values(brick_adjacent_finder(place, brick_adjacent_list), how_many_column,
                                brick_adjacent_list, current_state)

            first_row, first_column = find_row_column(place, how_many_column)
            second_row, second_column = find_row_column(brick_adjacent_finder(place, brick_adjacent_list),
                                                        how_many_column)
            if not "H" in x and not "B" in y:
                current_state[first_row - 1][first_column - 1] = "H"
                current_state[second_row - 1][second_column - 1] = "B"

                if is_finished(current_state, restrictions_list):
                    return True


            if not "B" in x and not "H" in y:
                current_state[first_row - 1][first_column - 1] = "B"
                current_state[second_row - 1][second_column - 1] = "H"

                if is_finished(current_state, restrictions_list):
                    return True


            current_state[first_row - 1][first_column - 1] = "N"
            current_state[second_row - 1][second_column - 1] = "N"

            if is_finished(current_state, restrictions_list):
                return True



def main():
    import sys

    input_file = open(sys.argv[1])
    how_many_row = len(input_file.readline().split())
    input_file.readline()
    how_many_column = len(input_file.readline().split())

    current_state = [["x" for i in range(how_many_column)] for j in range(how_many_row)]
    brick_adjacent_list = brick_packages(input_file)
    restrictions_list = restrictions(input_file)

    input_file.close()

    first = [i[0] for i in brick_adjacent_list]
    last = first[-1]

    placer(0, current_state, restrictions_list, how_many_column, brick_adjacent_list, first, last)

    output_file = open(sys.argv[2], mode="w")

    if is_finished(current_state, restrictions_list):
        counter = 0
        for lines in current_state:
            output_file.write(" ".join(lines))
            counter += 1
            if not counter == len(current_state):
                output_file.write("\n")
    else:
        output_file.write("No solution!")

    output_file.close()



if __name__ == "__main__":
    main()