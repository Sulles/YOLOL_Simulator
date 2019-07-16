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
                "ERROR: Each line can only contain 70 characters! Your line '{0}' has {1} characters".format(
                    line, len(line))

            print("Parsing line: {}".format(line))

            if handle_conditional(line, py_file):
                print("Conditionals parsed")
            elif handle_set_value(line, py_file):
                print("Values set")

        yolol_file.close()
        py_file.close()

    except Exception as e:
        print("Something went wrong!\n{}".format(e))
        raise e


def handle_set_value(line, output_file):
    """

    :param line:
    :param output_file:
    :return:
    """
    verif = re.search('(={1}|\+=|-=|\+\+|--|\*=|/=|%=)', line)
    try:
        print("Found set value {0} in '{1}'".format(verif.group(0), line))
    # Raises AttributeError if no match
    except AttributeError:
        return False

    matches = re.findall('([a-z]+\s?)([^a-zA-Z0-9"\s]+)\s?("[^"]+"|\S+)\s?#?', line)

    print("Matches! '{}'".format(matches))

    for x in range(0, len(matches)):
        output_file.write("\n" + str(matches[x][0] + " " + matches[x][1]) + " " + matches[x][2])

    # Write stuff to output file!

    return True


def handle_conditional(line, output_file):
    """
    This function handles conditionals such as 'if', 'then', and 'else'
    :param line: the string of the line to handle conditionals for
    :param output_file: the output python file to write to
    :return: Boolean to indicate whether conditionals were found and parsed
    """

    verif = re.search('if|then|else|end', line)
    try:
        print("Found conditional {0} in '{1}'".format(verif.group(0), line))
    # Raises AttributeError if no match
    except AttributeError:
        return False

    assert line[0:2] == 'if', "ERROR: Conditionals must start with 'if'! Your line was: {}".format(line)

    map_cond_state_expr = get_cond_state_expr(line)
    # map_cond_state_expr = re.findall(
    #     'if\s+([a-z]+|:[a-z]+)\s*([^a-z0-9"\s]+)\s*(\S)\s+then\s+([a-z]+|:[a-z]+)\s*([^a-z0-9"\s]+)\s*(\S)\s+([a-z]+\s?#?)',
    #     line)
    last_part = re.search('end (.*)', line)
    print("Parsed YOLOL conditional statement: {}".format(map_cond_state_expr))
    try:
        last_part = last_part.group(1)
        print("Found something after end: {}".format(last_part))
    # Raises AttributeError if no match found
    except AttributeError:
        last_part = None

    # Write stuff to output file!

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
    matches = re.search('([a-z]+) ([a-z]+|:[a-z]+)\s*(\W+)\s*(\S*) (.*end.*)\s?#?', line)
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
    __main__("")
