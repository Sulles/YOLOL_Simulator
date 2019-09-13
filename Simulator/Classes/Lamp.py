"""
Created: July 13, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This class simulates the funtionality of a Lamp in Starbase.
"""

''' IMPORTS '''
if __name__ == "__main__":
    # noinspection PyUnresolvedReferences
    from pygame_obj import PygameObj
else:
    from .pygame_obj import PygameObj
import colorsys
from copy import copy


class Lamp(PygameObj):
    def __init__(self, input_settings):
        """
        :param input_settings: dictionary of settings.
            Expected dictionary keys are: name, on, lumens, hue, saturation, value, range, center, width and height
        """
        settings = {'name': 0, 'on': False, 'lumens': 600, 'hue': 360, 'saturation': 0, 'value': 200, 'range': 10,
                    'center': [0, 0], 'width': 30, 'height': 30,
                    'color_map': [None, colorsys.hsv_to_rgb(360, 0, 200)],
                    'shapes': [
                        {'type': 'circle',
                         'color': None,
                         'settings':
                             {'center': [0, 0],
                              'radius': 50}},
                        {'type': 'circle',
                         'color': (225, 225, 0),
                         'settings':
                             {'center': [0, 0],
                              'radius': 10}}]}

        for set in settings.keys():
            if set in input_settings:
                settings[set] = input_settings[set]

        # Pygame object init
        PygameObj.__init__(self, settings['center'], settings['width'], settings['height'],
                           settings['color_map'],
                           settings['shapes'])

        self.name = settings['name']
        self.lampon = settings['on']
        self.lumens_list = [0, settings['lumens']]
        self.hue_list = [0, settings['hue']]
        self.saturation_list = [0, ['saturation']]
        self.value_list = [0, settings['value']]
        self.range_list = [0, settings['range']]

        self.lamplumens = self.lampcolorhue = self.lampcolorsaturation = \
            self.lampcolorvalue = self.lamprange = None
        self.enable_disable()

        self.attribute_map = dict(lampon='lampon')

    def toggle_on_off(self, on_off=None):
        if on_off is not None:  # if specified ON/OFF state
            if on_off:  # True is ON, False is OFF
                self.lampon = True
            else:
                self.lampon = False
        else:  # Toggle
            if self.lampon:
                self.lampon = False
            else:
                self.lampon = True
        # print('Lamp "%s" new state is: %d' % (self.name, self.lampon))
        self.enable_disable()
        return dict(lampon=copy(self.lampon))

    def print(self):
        print("=== LAMP INFORMATION ===\n"
              "Name: {0}\n"
              "Is ON: {1}\n"
              "Current Lumens: {2}\n"
              "Current Hue: {3}\n"
              "Current Saturation: {4}\n"
              "Current Value: {5}\n"
              "Current Range: {6}\n"
              "Attribute Map: {7}".format(
            self.name, self.lampon, self.lamplumens, self.lampcolorhue, self.lampcolorsaturation, self.lampcolorvalue,
            self.lamprange, self.attribute_map))

    def enable_disable(self):
        self.lamplumens = self.lumens_list[self.lampon]
        self.lampcolorhue = self.hue_list[self.lampon]
        self.lampcolorsaturation = self.saturation_list[self.lampon]
        self.lampcolorvalue = self.value_list[self.lampon]
        self.lamprange = self.range_list[self.lampon]
        self._update_color(self.lampon)

    def draw(self, surface):
        self._draw(surface)

    def handle_action(self, action_type):
        if action_type == 'LEFT_MOUSE_DOWN':
            return self.toggle_on_off()

    def get_attributes(self):
        return self.attribute_map.keys()

    def modify_attr(self, attr, new_value):
        """
        Function that allows YOLOL code to modify the attribute or 'global variable' value of an object
        :param attr: string of attribute/global variable to be changed
        :param new_value: new value for the corresponding attribute
        """
        # TODO: Add all other attributes to self.attribute_map and implement here
        try:
            if self.attribute_map[attr] == 'lampon':
                self.toggle_on_off(new_value)
        except AttributeError:
            print('"%s" does not support modifying "%s" at this time!' % (self.name, str(attr)))

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


# Unit test
if __name__ == "__main__":
    lamp = Lamp({'name': 'lamp_name',
                 'state': 1,
                 'center': [0, 0]})
    lamp.print()
    lamp.toggle_on_off()
    lamp.print()
    lamp.change_attr_name('lampon', 'lampstate')
    lamp.print()
