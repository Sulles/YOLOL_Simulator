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
else:
    from .pygame_obj import PygameObj
import importlib
import os
import re


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

        # Pygame object init
        PygameObj.__init__(self, center, width, height, color_map, shapes)

        # Code parse & import
        self.YoPyfile = open('YoPy/{}.txt'.format(name), 'r')
        self.lines = re.search(r'lines: [0-9]{0,2}', self.YoPyfile.read())[-2:]     # grab only numbers
        self.YoPyfile.close()
        # ?
        importlib.import_module('YoPy.{}.txt'.format(self.name))

    def _print(self):
        print("=== CHIP INFORMATION ===")
        print("Chip Name: {0}\n"
              "Chip Wait: {1}\n"
              "Chip Style: {2}\n"
              "Number of lines: {3}".format(self.name, self.chipwait, self.style, self.lines))


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

        _chip.__init__(self, settings['name'], settings['name'], settings['style'], settings['center'],
                       settings['width'], settings['height'], settings['color_map'], settings['shapes'])

    def print(self):
        self._print()

    def draw(self, surface):
        self._draw(surface)


# Unit test
if __name__ == "__main__":
    print("Running unit test for Chip class...")
    chip = Chip("")
    chip.print()
