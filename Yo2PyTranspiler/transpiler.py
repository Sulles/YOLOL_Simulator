"""
Created: July 14, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This script transpiles YOLOL code to Python
"""

import re


def __main__(file_name):
    try:
        yolol_file = open("../YOLOLCode/{}.txt".format(file_name), 'r')
        py_file = open("../PythonizedYOLOLCode/{}.py".format(file_name), 'w')

        for line in yolol_file:
            line = line.lower()

            assert len(line) <= 70, \
                'ERROR: Each line can only contain 70 characters! This line had {0}'.format(len(line))

            print("Parsing line: {}".format(line))

            if handle_conditional(line, py_file):
                print("Conditionals parsed")

        yolol_file.close()
        py_file.close()

    except Exception as e:
        print("Something went wrong!\n{}".format(e))
        raise e


def handle_conditional(line, output_file):
    """
    This function handles conditionals such as 'if', 'then', and 'else'
    :param line: the string of the line to handle conditionals for
    :param output_file: the output python file to write to
    :return: Boolean to indicate whether conditionals were found and parsed
    """

    verif = re.search('.*(if|then|else|end).*', line)
    try:
        print("Found {0} conditionals in '{1}'".format(len(verif.group(1)), verif.group()))
    # Raises AttributeError if no match
    except AttributeError:
        return False

    assert line[0:2] == 'if', "ERROR: Conditionals must start with 'if'! Your line was: '{}'".format(line)

    map_cond_state_expr = get_cond_state_expr(line)
    last_part = re.search('end (.*)', line)
    print("Parsed YOLOL conditional statement: {}".format(map_cond_state_expr))
    try:
        print("Found something after end: {}".format(last_part.group(1)))
    except AttributeError:
        pass

    return True


def get_cond_state_expr(line, map=[]):
    """
    Recursive function to find all conditional statements and their comparative expressions
    :param line: the line that matched a regex for conditional check
    :param map: 
    :return: 
    """
    # group 1: ([a-z]+) = captures conditional statement, i.e. if, then
    # group 2: ([a-z]+|:[a-z]+) = captures variable or function, 'var' or 'buttonstate' which is function of Button
    # group 3: (\W+) = captures conditional expressions, i.e. '=' or '~='
    # group 4: (\S*) = captures comparative value, i.e. '2' or '"some_string"'
    # group 5: (.*end.*) = captures everything else
    matches = re.search('([a-z]+) ([a-z]+|:[a-z]+)\s*(\W+)\s*(\S*) (.*end.*)', line)
    # print("Found conditional statement '{0}'\n"
    #       "Found variable or function '{1}'\n"
    #       "Found conditional expression '{2}'\n"
    #       "Found comparative value '{3}'\n".format(
    #         matches.group(1), matches.group(2), matches.group(3), matches.group(4)))

    map.append([str(matches.group(1)), str(matches.group(2)), str(matches.group(3)), str(matches.group(4))])
    try:
        map.append(get_cond_state_expr(matches.group(5)))
    except AttributeError:
        print("At the end of conditional parse.")

    return map[:-1]


# Unit test
if __name__ == "__main__":
    __main__("button_lamp")
