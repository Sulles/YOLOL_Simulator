"""
Created July 31, 2019

Author: Sulles
"""

import json
import re


def __main__():
    """
    Main function, opens files and creates python translation
    """
    CylonAST = open('.txt', 'r')
    YoPy = open('YoPy.py', 'w+')

    json_struct = json.loads(CylonAST.read())
    # print(json.dumps(json_struct, indent=2, sort_keys=True))

    # create global list of all identifiers used in YOLOL script
    global_identifiers = list()

    for line in json_struct['program']['lines']:
        parse(line, YoPy)

    handle_lines(YoPy)
    local_identifiers, global_identifiers = handle_variables(json_struct, YoPy)
    # print('Found {0} unique identifiers: {1}'.format(len(global_identifiers), global_identifiers))
    handle_indents(YoPy)

    YoPy.write('\n')

    CylonAST.close()
    YoPy.close()


def handle_lines(YoPy):
    """
    This function creates a function for each line as well compiles a
    :return:
    """
    YoPy.seek(0, 0)
    line_number = 1
    output = "from time import sleep"
    for line in YoPy.readlines():
        if re.search(r'# NEW LINE!', line):
            output += '\n# END INDENT'
            output += '\ndef line_{0}(kwargs):  # START INDENT'.format(line_number)
            line_number += 1
        else:
            output += line
    output += '\n# END INDENT'

    YoPy.seek(0, 0)
    YoPy.truncate()
    YoPy.write(output)


def handle_variables(json_struct, YoPy):
    local_identifiers = []
    for line in json_struct['program']['lines']:
        local_identifiers.append(get_identifiers(line))
        # print('found {0} identifiers: {1}'.format(len(local_identifiers[-1]), local_identifiers[-1]))

    global_identifiers = list()

    for x in range(len(local_identifiers)):
        # print('Line {0} has {1} identifiers: {2}'.format(x + 1, len(local_identifiers[x]), local_identifiers[x]))
        for y in range(len(local_identifiers[x])):
            if local_identifiers[x][y] not in global_identifiers:
                global_identifiers.append(local_identifiers[x][y])

    local_identifiers, global_identifiers = handle_globals(local_identifiers, global_identifiers, YoPy)

    # print('All local identifiers: {}'.format(local_identifiers))

    return local_identifiers, global_identifiers


def get_identifiers(AST, identifiers=None):
    if identifiers is None:
        identifiers = []
    # print('Dealing with {0}'.format(type(AST)))
    if isinstance(AST, list):
        for _ in AST:
            get_identifiers(_, identifiers)
    elif isinstance(AST, dict):
        for key, value in AST.items():
            # print('At {}'.format(key))
            if isinstance(value, list) or isinstance(value, dict):
                get_identifiers(value, identifiers)
            elif key == 'name' or key == 'identifier':
                if value not in identifiers:
                    # print('Added identifier! {}'.format(value))
                    identifiers.append(value)
    else:
        print('what even are you? {}'.format(AST))
        raise AssertionError
    return identifiers


def handle_globals(local_identifiers, global_identifiers, YoPy):
    """
    This function handles the preceding ':' for external variables
    """
    output = ""
    YoPy.seek(0, 0)
    for line in YoPy.readlines():
        matches = re.findall(r'(:[a-z0-9]+)', line)
        if matches:
            for m in matches:
                new_m = 'GLOBAL_' + m[1:]
                line = line.replace(m, new_m)
        output += line

    # print(output)
    YoPy.seek(0, 0)
    YoPy.truncate()
    YoPy.write(output)

    for ident in global_identifiers:
        matches = re.findall(r'(:[a-z0-9]+)', ident)
        if matches:
            for m in matches:
                new_m = 'GLOBAL_' + m[1:]
                global_identifiers[global_identifiers.index(ident)] = ident.replace(m, new_m)

    for x in range(len(local_identifiers)):
        for y in range(len(local_identifiers[x])):
            matches = re.findall(r'(:[a-z0-9]+)', local_identifiers[x][y])
            if matches:
                for m in matches:
                    new_m = 'GLOBAL_' + m[1:]
                    local_identifiers[x][y] = local_identifiers[x][y].replace(m, new_m)
    return local_identifiers, global_identifiers


def handle_indents(YoPy):
    """
    This function handles indents for Python
    """
    output = ""
    YoPy.seek(0, 0)
    tab_counter = 0
    tab = '    '
    for line in YoPy.readlines():
        new_line = tab_counter * tab + line
        output += new_line
        # print(new_line)

        start = re.findall(r'# START INDENT', line)
        if len(start) > 0:
            tab_counter += 1 * len(start)

        end = re.findall(r'# END INDENT', line)
        if len(end) > 0:
            tab_counter -= 1 * len(end)

        if tab_counter < 0:
            tab_counter = 0

    # print(output)
    YoPy.seek(0, 0)
    YoPy.truncate()
    YoPy.write(output)

    # remove comments to start/end indents
    YoPy.seek(0, 0)
    output = ""
    for line in YoPy.readlines():
        output += line.replace('# START INDENT', '').replace('# END INDENT', '')

    YoPy.seek(0, 0)
    YoPy.truncate()
    YoPy.write(output)


def parse(line, YoPy):
    """
    This function parses a dictionary, aka JSON structure, and passes the python equivalent to global YoPy.py file
    :param line: JSON structure of the line to parse
    :return: N/A
    """
    YoPy.write('\n\n# NEW LINE!\n')
    # print('NEW LINE!')
    if len(line['comment']) > 0:
        YoPy.write('\n# {}'.format(line['comment']))
        # print('Wrote comment: %s' % line['comment'])
    if len(line['code']) > 0:
        for code_bit in line['code']:
            if code_bit['type'] == 'statement::assignment' or code_bit['type'] == 'statement::expression':
                YoPy.write('\n' + handle_assignment(code_bit))
            elif code_bit['type'] == 'statement::if':
                YoPy.write('\n' + handle_if(code_bit))
            elif code_bit['type'] == 'statement::goto':
                print('code bit: {}'.format(code_bit))
                print('expression: {}'.format(code_bit['expression']))
                print('num? {}'.format(code_bit['expression']['num']))
                print('found goto! adding line in next_lines list: %d' % (int(code_bit['expression']['num'])))
                YoPy.write('\nreturn kwargs, %d' % (int(code_bit['expression']['num'])))
                return
            else:
                print('Got code bit: "%s"' % code_bit)
    YoPy.write('\nreturn kwargs, None')
    return


def handle_if(statement):
    """
    This function handles if - then - else if - else - end statements
    """
    # print('handling if statement: "{}"'.format(statement))
    ret = ""
    if statement['type'] == 'statement::if':
        condition = handle_assignment(statement['condition']) + ':' + '  # START INDENT'
        # print('parsed if: <{}>'.format(condition))

        body = ""
        for b in statement['body']:
            # print('found if: "{}"'.format(b))
            if b['type'] == 'statement::if':
                body += handle_if(b) + '  # END INDENT'
            else:
                body += handle_assignment(b) + '  # END INDENT'
        # print('parsed body: <{}>'.format(body))

        if statement['else_body']:
            else_body = '\nelse: \t# START INDENT\n'
            for e in statement['else_body']:
                # print('found else: "{}"'.format(e))
                if e['type'] == 'statement::if':
                    else_body += handle_if(e) + '  # END INDENT'
                else:
                    else_body += handle_assignment(e) + '  # END INDENT'
            # print('parsed else: <{}>'.format(else_body))
            ret += 'if ' + condition + '\n' + body + '\n' + else_body
        else:
            ret += 'if ' + condition + '\n' + body
        # print('output: {}'.format(ret))

    return ret


def handle_assignment(value):
    """
    This function handles the different types of values an assignment statement can be
    """
    # print('handling value: "{}"'.format(value))

    if not isinstance(value, dict):
        # print('What did you pass?!')
        raise AssertionError
    try:
        if value['type'] == 'statement::assignment':
            # print("found assignment: kwargs['%s']" % value['identifier'])
            return str("kwargs['{0}'] {1} {2}".format(
                value['identifier'], value['operator'], handle_assignment(value['value'])))
        elif value['type'] == 'statement::expression':
            # print('found expression')
            return handle_assignment(value['expression'])
        elif value['type'] == 'expression::group':
            # print('found group')
            return '(' + handle_assignment(value['group']) + ')'
        elif value['type'] == 'expression::binary_op':
            # print('found binary operation')
            return handle_assignment(value['left']) + ' ' + value['operator'] + ' ' + handle_assignment(value['right'])
        elif value['type'] == 'expression::unary_op':
            return handle_assignment(value['operand']) + ' ' + value['operator']
        elif value['type'] == 'expression::string':
            # print('returning string')
            return '"' + value['str'] + '"'
        elif value['type'] == 'expression::number':
            # print('returning number')
            return value['num']
        elif value['type'] == 'expression::identifier':
            # print("returning: kwargs['%s']" % value['name'])
            return str("kwargs['%s']" % value['name'])

    except TypeError:
        print('Did not find anything noteworthy in: "{}"'.format(value))
        return ""

    print('got leftovers?: {}'.format(value))
    return ""


if __name__ == "__main__":
    __main__()
