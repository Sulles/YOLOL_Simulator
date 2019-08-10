"""
Created: July 13, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This class simulates the functionality of a YOLOL Chip in Starbase. As there are
three types of chips, all chips will have a subclass to inherit all common
features and checks to verify only valid commands are passed

for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))
"""
''' IMPORTS '''
if __name__ == "__main__":
    # noinspection PyUnresolvedReferences
    from pygame_obj import PygameObj
    # noinspection PyUnresolvedReferences
    from YoPy.Interpreter import *
else:
    from .pygame_obj import PygameObj
    from .YoPy.Interpreter import *
import os
import threading


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
        assert os.path.exists('YoPy/{}.txt'.format(name)), 'Could not find: "Classes/YoPy/%s.txt"' % name

        self.name = name
        self.chipwait = wait
        self.style = style
        self.total_lines = 0
        self.current_line = 0
        self.running = False

        # Pygame object init
        PygameObj.__init__(self, center, width, height, color_map, shapes)

        try:
            CylonAST = open('YoPy/{}.txt'.format(name), 'r')
            YoPy = open('YoPy/YoPy_{}.py'.format(name), 'w+')
            print('Found: {}.txt'.format(name))
        except Exception:
            print('Ruh roh! Could not read/write either YoPy/{0}.txt or YoPy/YoPy_{0}.py !'.format(name))
            raise

        json_struct = json.loads(CylonAST.read())
        # print(json.dumps(json_struct, indent=2, sort_keys=True))

        # create global list of all identifiers used in YOLOL script
        self.kwargs = list()

        for line in json_struct['program']['lines']:
            self.total_lines += 1
            parse(line, YoPy)

        handle_lines(YoPy)
        local_identifiers, all_identifiers = handle_variables(json_struct, YoPy)
        # convert all_identifiers to dictionary
        self.kwargs = dict()
        for _ in all_identifiers:
            self.kwargs[str(_)] = 0
        # print('Found {0} unique identifiers: {1}'.format(len(global_identifiers), global_identifiers))
        handle_indents(YoPy)

        CylonAST.close()
        YoPy.close()

        # TODO: this is almost done!
        self.line_0 = __import__('YoPy.YoPy_{}'.format(self.name), globals(), locals(), ['line_0']).line_0

        print('testing calling lines...')
        self.line_0(self.kwargs)

    def _print(self):
        print("=== CHIP INFORMATION ===")
        print("Chip Name: {0}\n"
              "Chip Wait: {1}\n"
              "Chip Style: {2}\n"
              "Number of lines: {3}".format(self.name, self.chipwait, self.style, self.total_lines))

    def run_next_line(self):
        if not self.running:
            self.running = True
            # Thread this:
            # self.call_line((self.current_line + 1) % self.lines)
        else:
            return

    # def call_line(self, line):
    #     """
    #
    #     :return:
    #     """
    #     self.kwargs, next_line = 1, 2
    #     self.running = False
    #     if next_line:
    #         self.current_line = line
    #         self.call_line(next_line)


# This is the main chip class
# TODO: Add chip-specific functionality and verify code compatibility for each chip type
class Chip(_chip):
    def __init__(self, input_settings):
        settings = {'name': "", 'wait': 0, 'style': 0, 'center': [0, 0], 'width': 50, 'height': 40,
                    'color_map': [(100, 100, 100), (100, 150, 100)],
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


# Unit test
if __name__ == "__main__":
    print("Running unit test for Chip class...")
    chip = Chip({'name': "test_chip"})
    chip.print()
