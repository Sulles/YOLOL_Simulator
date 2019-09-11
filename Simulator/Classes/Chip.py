"""
Created: July 13, 2019
Last Updated:

Author: Sulles

TODO: Make _chip dynamically create line functions with:
    https://stackoverflow.com/questions/3687682/python-define-dynamic-functions?lq=1

=== DESCRIPTION ===
This class simulates the functionality of a YOLOL Chip in Starbase. As there are
three types of chips, all chips will have a subclass to inherit all common
features and checks to verify only valid commands are passed

for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))
"""
import os
from copy import copy
from time import time

if __name__ == "__main__":
    # noinspection PyUnresolvedReferences
    from pygame_obj import PygameObj
    # noinspection PyUnresolvedReferences
    from YoPy.Interpreter import *
else:
    from .pygame_obj import PygameObj
    from .YoPy.Interpreter import *


# This is the sub-class
class _chip(PygameObj):
    def __init__(self, name, wait, style, center, width, height, color_map, shapes):
        """
        Initializer for sub-class of all YOLOL chips
        :param name: Name of the Yolol chip text file to parse
        :param wait: Negative values mean execution is paused, zero means script is being executed, and positive values
            mean execution will continue after the amount of line runs have passed that are equal to the value.
            i.e. wait = 5, will run after 5 * 0.2s = 1s
        :param style: Chip style, some chips will be capable of running more complex calculations than others
        :param center: The center pixel of the chip
        """
        assert os.path.exists('Classes/YoPy/{}.txt'.format(name)), 'Could not find: "Classes/YoPy/%s.txt"' % name

        self.name = name
        self.chipwait = wait
        self.style = style
        self.run_line = True
        self.last_run = time()
        self.lines = list()
        self.total_lines = 0
        self.current_line = 1
        self.attribute_map = dict(chipwait='chipwait')

        # Pygame object init
        PygameObj.__init__(self, center, width, height, color_map, shapes)

        try:
            CylonAST = open('Classes/YoPy/{}.txt'.format(name), 'r')
            YoPy = open('Classes/YoPy/YoPy_{}.py'.format(name), 'w+')
            print('Found: {}.txt'.format(name))
        except Exception:
            print('Ruh roh! Could not read/write either YoPy/{0}.txt or YoPy/YoPy_{0}.py !'.format(name))
            raise

        # Reading JSON Cylon AST file
        json_struct = json.loads(CylonAST.read())

        # Creating global list of all identifiers used in YOLOL script
        self.kwargs = list()

        # Parse JSON structure...
        for line in json_struct['program']['lines']:
            self.total_lines += 1
            parse(line, YoPy)
        handle_lines(YoPy)
        local_identifiers, all_identifiers = handle_variables(json_struct, YoPy)
        self.kwargs = dict()
        for _ in all_identifiers:  # convert all_identifiers to dictionary
            self.kwargs[str(_)] = 0
        handle_indents(YoPy)
        YoPy.write('\n')

        # Close files
        CylonAST.close()
        YoPy.close()

        # Import each line into Chip object
        try:
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_1']).line_1)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_2']).line_2)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_3']).line_3)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_4']).line_4)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_5']).line_5)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_6']).line_6)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_7']).line_7)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_8']).line_8)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_9']).line_9)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_10']).line_10)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_11']).line_11)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_12']).line_12)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_13']).line_13)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_14']).line_14)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_15']).line_15)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_16']).line_16)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_17']).line_17)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_18']).line_18)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_19']).line_19)
            self.lines.append(__import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_20']).line_20)
        except AttributeError as e:
            print('Parsed all lines, found %d!' % len(self.lines))
            for x in range(len(self.lines), 20):
                self.lines.append(None)
            pass
        except Exception as e:
            print('Unexpected Error! %s' % e)
            raise

    def _print(self):
        print("=== CHIP INFORMATION ===")
        print("Chip Name: {0}\n"
              "Chip Wait: {1}\n"
              "Chip Style: {2}\n"
              "Number of lines: {3}\n"
              "All variables: {4}".format(self.name, self.chipwait, self.style, self.total_lines, self.kwargs))

    def _run_next_line(self):
        if not self.run_line:
            print('ERROR: Chip disabled!')
            return None
        elif time() - self.last_run >= 0.2:
            self.last_run = time()

            # handle chip wait
            if self.chipwait != 0:
                self.chipwait -= 1
                print('Chip wait decremented to: %d' % self.chipwait)

            # TODO: if only 1 line in AST, make sure lines 2-20 are also 'executed'
            # print('Starting to execute line %d' % self.current_line)
            if self.lines[self.current_line - 1] is not None:
                self.kwargs, goto = self.lines[self.current_line - 1](self.kwargs)
                print('Chip Updated kwargs: {}'.format(self.kwargs))
                if goto:
                    # print('Got goto: %d' % goto)
                    self.current_line = goto
            return copy(self.kwargs)
        else:
            print('ERROR: Tried to run next line too soon!')
            return None

    def _handle_action(self, action_type):
        if action_type == 'LEFT_MOUSE_DOWN':
            print('self.run_thread?: {}'.format(self.run_line))
            self.update_color(self.run_line)
            if not self.run_line:
                self.run_line = True
                print('Got command to start next line!')
                self._run_next_line()
            else:
                print('Cancelling %s execution...' % self.name)
                self.run_line = False

    def _update_kwargs(self, updated_kwargs):
        for key, item in updated_kwargs.items():
            if key in self.kwargs:
                # print('Updating "{0}" from {1} to {2}'.format(key, self.kwargs[key], item))
                self.kwargs[key] = item

    def get_attributes(self):
        return self.attribute_map.keys()

    def modify_attr(self, attr, new_value):
        """
        Function that allows YOLOL code to modify the attribute or 'global variable' value of an object
        :param attr: string of attribute/global variable to be changed
        :param new_value: new value for the corresponding attribute
        """
        try:
            if self.attribute_map[attr] == 'chipwait':
                self.chipwait = new_value
        except AttributeError:
            print('The attribute provided is either not supported or cannot be modified by YOLOL code!')

    def change_attr_name(self, old_name, new_name):
        """
        This function allows for players to change the 'global variable' of an object
        :param old_name: string of name of current 'global variable' to be renamed
        :param new_name: string of new name for 'global variable'
        """
        new_attribute_map = dict()
        for key, item in self.attribute_map.items():
            if key == old_name:
                print('Updating attribute map for: "{0}" to "{1}"'.format(key, new_name))
                new_attribute_map[new_name] = item
            else:
                print('Copying over other attributes...')
                new_attribute_map[key] = item
        self.attribute_map = new_attribute_map


# This is the main chip class
# TODO: Add chip-specific functionality and verify code compatibility for each chip type
class Chip(_chip):
    def __init__(self, input_settings):
        settings = {'name': "", 'wait': 0, 'style': 0, 'center': [0, 0], 'width': 50, 'height': 40,
                    'color_map': [(100, 200, 100), (200, 100, 100)],
                    'shapes': [
                        {'type': 'rect',
                         'color': None,
                         'settings':
                             {'center': [0, 0],
                              'width': 50,
                              'height': 40}}]}

        for set in settings:
            if set in input_settings:
                settings[set] = input_settings[set]

        _chip.__init__(self, settings['name'], settings['wait'], settings['style'], settings['center'],
                       settings['width'], settings['height'], settings['color_map'], settings['shapes'])

    def print(self):
        self._print()

    def draw(self, surface):
        self._draw(surface)

    def step(self):
        return self._run_next_line()

    def disable(self):
        self.run_line = False

    def handle_action(self, action_type):
        return self._handle_action(action_type)

    def update_kwargs(self, updated_kwargs):
        self._update_kwargs(updated_kwargs)
