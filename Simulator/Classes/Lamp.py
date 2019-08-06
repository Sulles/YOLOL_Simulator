"""
Created: July 13, 2019
Last Updated: August 3, 2019

Author: StolenLight

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


class Lamp(PygameObj):
    def __init__(self, input_settings):
        """
        :param input_settings: dictionary of settings.
            Expected dictionary keys are: name, on, lumens, hue, saturation, value, range, center, width and height
        """
        settings = {'name': 0, 'on': False, 'lumens': 600, 'hue': 360, 'saturation': 0, 'value': 200, 'range': 10,
                    'center': [0, 0], 'width': 30, 'height': 30,
                    'color_map': [colorsys.hsv_to_rgb(360, 0, 200), (0, 0, 0)],
                    'shapes': [
                        {'type': 'circle',
                         'color': None,
                         'settings':
                             {'center': [0, 0],
                              'radius': 50}},
                        {'type': 'rect',
                         'color': (0, 0, 0),
                         'width': 2,
                         'settings':
                             {'center': [0, 0],
                              'width': 30,
                              'height': 30}},
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

    def toggle_on_off(self):
        if self.lampon:
            self.lampon = False
        else:
            self.lampon = True
        self.enable_disable()

    def print(self):
        print("=== LAMP INFORMATION ===\n"
              "Name: {0}\n"
              "Is ON: {1}\n"
              "Current Lumens: {2}\n"
              "Current Hue: {3}\n"
              "Current Saturation: {4}\n"
              "Current Value: {5}\n"
              "Current Range: {6}".format(
            self.name, self.lampon, self.lamplumens, self.lampcolorhue,
            self.lampcolorsaturation, self.lampcolorvalue, self.lamprange))

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
            self.toggle_on_off()


# Unit test
if __name__ == "__main__":
    lamp = Lamp({'name': 'lamp_name',
                 'state': 1,
                 'center': [0, 0]})
    lamp.print()
    lamp.toggle_on_off()
    lamp.print()
