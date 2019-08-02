"""
Created July 31, 2019

Author: StolenLight
"""

import json


def __main__():
    """
    Main function, opens files and creates python translation
    """
    cAST = open('CAST.txt', 'r')
    global CPy
    CPy = open('CPy.py', 'w')

    json_struct = json.loads(cAST.read())
    # print(json.dumps(json_struct, indent=2, sort_keys=True))

    for line in json_struct['program']['lines']:
        parse(line)

    handle_indents()

    cAST.close()
    CPy.close()


def handle_indents():
    """
    This function handles indents for Python
    """
    # move pointer to front of CPy
    # for line in Cpy.readline():
    #   if START IF, tab_count += 1
    #   CPy.write(tab_count * '    ' + line)


def parse(line):
    """
    This function parses a dictionary, aka JSON structure, and passes the python equivalent to global CPy.py file
    :param line: JSON structure of the line to parse
    :return: N/A
    """
    CPy.write('\n# NEW LINE!\n')
    # print('NEW LINE!')
    if len(line['comment']) > 0:
        CPy.write('\n# {}'.format(line['comment']))
        print('Wrote comment: %s' % line['comment'])
    elif len(line['code']) > 0:
        for code_bit in line['code']:
            if code_bit['type'] == 'statement::assignment' or code_bit['type'] == 'statement::expression':
                CPy.write('\n' + handle_value(code_bit))
            elif code_bit['type'] == 'statement::if':
                CPy.write('\n' + handle_if(code_bit))
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
        condition = handle_value(statement['condition']) + ':' + ' \t# START IF'
        print('parsed condition: <{}>'.format(condition))

        body = ""
        for b in statement['body']:
            print('found something in body: "{}"'.format(b))
            if b['type'] == 'statement::if':
                body += handle_if(b) + ' \t# END IF'
            else:
                body += handle_value(b)
        print('parsed body: <{}>'.format(body))

        else_body = ""
        for e in statement['else_body']:
            print('found something in else_body: "{}"'.format(e))
            if e['type'] == 'statement::if':
                else_body += handle_if(e) + ' \t# END IF'
            else:
                else_body += handle_value(e) + ' \t# END IF'
        print('parsed else body: <{}>'.format(else_body))

        ret += 'if ' + condition + ':\n' + body + '\n' + 'else:\n' + else_body
        print('output: {}'.format(ret))

    return ret


def handle_value(value):
    """
    This function handles the different types of values an assignment statement can be
    """
    print('handling value: "{}"'.format(value))
    ret = ""

    if isinstance(value, list):
        for _ in value:
            return handle_value(_)
    try:
        if value['type'] == 'statement::assignment':
            print('found assignment')
            return value['identifier'] + ' ' + value['operator'] + ' ' + handle_value(value['value'])
        elif value['type'] == 'statement::expression':
            print('found expression')
            return handle_value(value['expression'])
        elif value['type'] == 'expression::binary_op':
            print('found binary operation')
            return handle_value(value['left']) + ' ' + value['operator'] + ' ' + handle_value(value['right'])
        elif value['type'] == 'expression::unary_op':
            return handle_value(value['operand']) + ' ' + value['operator']
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
