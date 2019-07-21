"""
Created: July 14, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This script transpiles YOLOL code to Python
"""

import re
re_dict = {'statement': '((:?[a-z]+[a-z0-9]*)\s?([\+?\-\*\/\%=]{1,2})\s?([:?a-z0-9\+\-\*\/\%]+|"[^"]+"))',
           'expression_if': '(if (:?[a-z0-9]+)\s?(==|~=|>=?|<=?)\s?(:?[a-z0-9]*|".*") then (.*) end\b)',
           'expression_then': ''}


def __main__(file_name):
    try:
        yolol_file = open("../YOLOLCode/{}.txt".format(file_name), 'r')
        py_file = open("../PythonizedYOLOLCode/{}.py".format(file_name), 'w')

        line_counter = 0

        for line in yolol_file:
            line_counter += 1
            line = line.lower()

            assert len(line) <= 70, \
                "ERROR: Each line can only contain 70 characters! Your line '{0}' has {1} characters".format(
                    line, len(line))
            assert line_counter <= 20, \
                "ERROR: Your file has more than 20 lines!"

            print('Adding marker for line in case GOTO needed')
            py_file.write('\n\n# Line %d' % line_counter)

            try:
                parse_line(line.replace('\n', ''), py_file)
            except Exception as e:
                print("CRITICAL ERROR: %s" %e)
                raise e

        yolol_file.close()
        py_file.close()

    except FileNotFoundError as e:
        print("YOLOL file '%s' not found! Please make sure file is .txt "
              "and is placed in the YOLOLCode folder.\n%s" % (file_name, e))
        raise e

    except FileExistsError as e:
        print("Uhhhh file exists already?\n%s" % e)
        raise e


def parse_line(line, py_file, return_leftovers=False):
    """
    This function handles parsing every line
    :param line: string of lower case characters to interpret
    :param py_file: pythonized file to write transpilation to
    :param ret: return boolean, if want to return leftovers rather than re-parse
    :return leftovers: if there is extra stuff at the end of an interpretation,
        return the leftovers, what could not be interpreted
    """
    leftovers = ""

    print("Parsing line: '{}'".format(line))

    if re.findall('(\s*)', line)[0] == line:
        print("Only white space found, skipping...")
        return

    if is_comment(line):
        py_file.write('\n# COMMENT: ' + line[2:])
        print("Comment handled")
    elif is_statement(line):
        leftovers = handle_statement(line, py_file)
        print("Conditional parsed")
    elif is_expression(line):
        leftovers = handle_expression(line, py_file)
        print("Values set")
    else:
        print("What even is this? '%s'" % line)
        raise AssertionError

    if return_leftovers:
        return leftovers
    elif leftovers is not None and leftovers != "\n" and leftovers != "":
        print("Found some leftovers!: '{}'".format(leftovers))
        parse_line(leftovers, py_file)


def is_comment(line):
    # All comments must start with '//'
    if line[0:2] == '//':
        return True
    else:
        return False


def is_expression(line):
    # All expressions must start with 'if' and have 'then' and 'end'
    if re.match('if .* then .* end', line):
        return True
    else:
        return False


def is_statement(line):
    if re.match(re_dict['statement'], line):
        return True
    else:
        return False


def handle_expression(line, output_file):
    """
    This function handles 'if ... then ... end' expressions
    :param line: string of lower case characters to interpret
    :param output_file: pythonized file to write transpilation to
    """
    print("Got line: '{}'".format(line))
    match = re.findall(re_dict['expression_if'], line)
    print("Match: '{}'".format(match))
    if match != []:
        print("Found match: '{}'".format(match))
    else:
        print("???")
    # else:
    #     match = re.findall(re_dict['expression_then'], line)
    #     if match == []:
    #         raise (AttributeError, "Ummmm, what is this? {}".format(line))
    #     print("Found match: '{}'".format(match))


def handle_statement(line, output_file):
    """
    This function handles statements such as 'a = b' and 'd += 4'
    :param line: string of lower case characters to interpret
    :param output_file: pythonized file to write transpilation t0

    WARNING: This program does not support string addition, i.e. a = "one" + 2
    """
    if re.findall('\+\+', line) or re.findall('\-\-', line):
        print("Statement Exception Found!")
        print("Len of line: %d" % len(line))
        line = handle_statement_exceptions(line, output_file)
        print("Len of line: %d" % len(line))

    matches = re.findall(re_dict['statement'], line)
    for m in matches:
        send_match_to_output(m[1:], output_file)

        print("Trying to find '%s' in '%s'" % (m[0], line))
        last_indx = line.index(m[0]) + len(m[0])

        try:
            line = line[last_indx:]
            print("Updated line: '{}'".format(line))
        # Exception raised when out of index error occurs
        except ValueError:
            line = ""
            pass

    if len(line) > 1:
        return line
    else:
        return None


def handle_statement_exceptions(line, output_file):
    """
    This function handles the exceptions to generic reg-ex for statements.
    The known exceptions are:
        -> n++
        -> n--
        -> ++n
        -> --n
    """
    matches = re.findall('((:?[a-z]+)\s?(\+\+|\-\-)|(\+\+|\-\-)\s?(:?[a-z]+))', line)
    print("Found matches! '{}'".format(matches))
    send_to_print = [None, None]
    for m in matches:
        if m[1] is not "":
            send_to_print[0] = m[1]
        else:
            send_to_print[0] = m[4]

        if m[2] == "++":
            send_to_print[1] = "+= 1"
        else:
            send_to_print[1] = "-= 1"

        send_match_to_output(send_to_print, output_file)

        start_indx = line.index(m[0])
        end_indx = start_indx + len(m[0])

        print("start index: %s \nend index: %s" % (start_indx, end_indx))

        line = line[:start_indx] + line[end_indx:]

    if len(line) > 1:
        return line
    else:
        return None


def send_match_to_output(match, output_file):
    print("Sending match to output file: '{}'".format(match))
    output = "\n"
    for m in match:
        output += m + " "

    output_file.write(output)



# Unit test
if __name__ == "__main__":
    __main__("")
