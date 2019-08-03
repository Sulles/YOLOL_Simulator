"""
Created July 31, 2019

Author: StolenLight
"""

import json
import re


def __main__():
    """
    Mai
    n function, opens files and creates python translation
    """
    cAST = open('CAST.txt', 'r')
    global C_Py
    C_Py = open('CPy.py', 'w+')

    json_struct = json.loads(cAST.read())
    # print(json.dumps(json_struct, indent=2, sort_keys=True))

    for line in json_struct['program']['lines']:
        parse(line)

    handle_indents()
    handle_globals()

    cAST.close()
    C_Py.close()


def handle_globals():
    """
    This function handles the preceding ':' for external variables
    """
    output = ""
    C_Py.seek(0, 0)
    for line in C_Py.readlines():
        matches = re.findall(r'(:[a-z0-9]+)', line)
        if matches:
            for m in matches:
                new_m = 'GLOBAL_' + m[1:]
                line = line.replace(m, new_m)
        output += line

    # print(output)
    C_Py.seek(0, 0)
    C_Py.write(output)


def handle_indents():
    """
    This function handles indents for Python
    """
    output = ""
    C_Py.seek(0, 0)
    tab_counter = 0
    tab = '    '
    for line in C_Py.readlines():
        new_line = tab_counter * tab + line
        output += new_line
        # print(new_line)

        start = re.findall(r'# START INDENT', line)
        if len(start) > 0:
            tab_counter += 1 * len(start)

        end = re.findall(r'# END INDENT', line)
        if len(end) > 0:
            tab_counter -= 1 * len(end)

    # print(output)
    C_Py.seek(0, 0)
    C_Py.write(output)


def parse(line):
    """
    This function parses a dictionary, aka JSON structure, and passes the python equivalent to global CPy.py file
    :param line: JSON structure of the line to parse
    :return: N/A
    """
    C_Py.write('\n# NEW LINE!\n')
    # print('NEW LINE!')
    if len(line['comment']) > 0:
        C_Py.write('\n# {}'.format(line['comment']))
        print('Wrote comment: %s' % line['comment'])
    if len(line['code']) > 0:
        for code_bit in line['code']:
            if code_bit['type'] == 'statement::assignment' or code_bit['type'] == 'statement::expression':
                C_Py.write('\n' + handle_assignment(code_bit))
            elif code_bit['type'] == 'statement::if':
                C_Py.write('\n' + handle_if(code_bit))
            else:
                print('Got code bit: "%s"' % code_bit)
    return


def handle_if(statement):
    """
    This function handles if - then - else if - else - end statements
    """
    print('handling if statement: "{}"'.format(statement))
    ret = ""
    if statement['type'] == 'statement::if':
        condition = handle_assignment(statement['condition']) + ':' + ' \t# START INDENT'
        print('parsed if: <{}>'.format(condition))

        body = ""
        for b in statement['body']:
            print('found if: "{}"'.format(b))
            if b['type'] == 'statement::if':
                body += handle_if(b) + ' \t# END INDENT'
            else:
                body += handle_assignment(b) + ' \t# END INDENT'
        print('parsed body: <{}>'.format(body))

        if statement['else_body']:
            else_body = '\nelse: \t# START INDENT\n'
            for e in statement['else_body']:
                print('found else: "{}"'.format(e))
                if e['type'] == 'statement::if':
                    else_body += handle_if(e) + ' \t# END INDENT'
                else:
                    else_body += handle_assignment(e) + ' \t# END INDENT'
            print('parsed else: <{}>'.format(else_body))
            ret += 'if ' + condition + '\n' + body + '\n' + else_body
        else:
            ret += 'if ' + condition + '\n' + body + '\n# END INDENT'
        # print('output: {}'.format(ret))

    return ret


def handle_assignment(value):
    """
    This function handles the different types of values an assignment statement can be
    """
    print('handling value: "{}"'.format(value))

    if not isinstance(value, dict):
        print('What did you pass?!')
        return handle_assignment(_)
    try:
        if value['type'] == 'statement::assignment':
            print('found assignment')
            return value['identifier'] + ' ' + value['operator'] + ' ' + handle_assignment(value['value'])
        elif value['type'] == 'statement::expression':
            print('found expression')
            return handle_assignment(value['expression'])
        elif value['type'] == 'expression::group':
            print('found group')
            return '(' + handle_assignment(value['group']) + ')'
        elif value['type'] == 'expression::binary_op':
            print('found binary operation')
            return handle_assignment(value['left']) + ' ' + value['operator'] + ' ' + handle_assignment(value['right'])
        elif value['type'] == 'expression::unary_op':
            return handle_assignment(value['operand']) + ' ' + value['operator']
        elif value['type'] == 'expression::string':
            print('returning string')
            return '"' + value['str'] + '"'
        elif value['type'] == 'expression::number':
            print('returning number')
            return value['num']
        elif value['type'] == 'expression::identifier':
            print('returning name')
            return value['name']

    except TypeError:
        print('Did not find anything noteworthy in: "{}"'.format(value))
        return ""

    print('got leftovers?: {}'.format(value))
    return ""


if __name__ == "__main__":
    __main__()
