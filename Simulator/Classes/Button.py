"""
Created: July 13, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This class simulates the functionality of a Button in Starbase. As there are
three types of buttons, all buttons will have a subclass to inherit all common
features
"""

''' IMPORTS '''
if __name__ == "__main__":
    # noinspection PyUnresolvedReferences
    from pygame_obj import PygameObj
else:
    from .pygame_obj import PygameObj
from copy import copy


# This is the sub-class
class _button(PygameObj):
    def __init__(self, name, state, on_state, off_state, style, center, width, height, color_map, shapes):
        """
        Initializer for sub-class of all buttons
        :param state: The current state of the button
        :param on_state: The state which signifies button is in 'on state'
        :param off_state: The state which signifies button is in 'off state'
        :param style: The style of the button...
            0: Hold down and release
            1: Basic Toggle (simple click to toggle)
            2: 4-state switch (like a click pen)
        :param center: The center pixel of the button on the main surface
        :param color_map: The color map for all potential states of the button
        """
        # Button parameters
        self.name = name
        self.buttonstate = state
        # Internal state is what transitions button from onstate to offstate depending on interaction
        self.internal_state = True
        self.buttononstate = on_state
        self.buttonoffstate = off_state
        self.buttonstyle = style
        self.maxstate = 0
        # TODO: verify that these attributes are modifiable by YOLOL code!
        self.attribute_map = dict(buttonstate='buttonstate', buttononstate='buttononstate',
                                  buttonoffstate='buttonoffstate')

        # Pygame object init
        PygameObj.__init__(self, center, width, height, color_map, shapes)

        # Assertions
        self.run_assert()

    def run_assert(self):
        if self.buttonstyle == 0 or self.buttonstyle == 1:
            assert self.buttonstate in range(0, 2), \
                'INVALID BUTTON STATE: Button Style "%s" only allows for 2 states' % self.buttonstyle
            self.maxstate = 2
        elif self.buttonstyle == 2:
            assert self.buttonstate in range(0, 5), \
                'INVALID BUTTON STATE: Button Style "%s" only allows for 4 states' % self.buttonstyle
            self.maxstate = 5

    def toggle_internal_state(self):
        self.internal_state = (self.internal_state + 1) % 2
        # print('"%s" Internal state is: %d' % (self.name, self.internal_state))
        if self.internal_state:
            return self.update_state(self.buttononstate)
        else:
            return self.update_state(self.buttonoffstate)

    def update_state(self, new_state=None):
        # print('"{0}" buttonstate updated from {1} to {2}'.format(self.name, self.buttonstate, new_state))
        self.buttonstate = new_state
        self.run_assert()
        self._update_color(self.internal_state)
        return dict(buttonstate=copy(self.buttonstate))

    def get_attributes(self):
        return self.attribute_map.keys()

    def modify_attr(self, attr, new_value):
        """
        Function that allows YOLOL code to modify the attribute or 'global variable' value of an object
        :param attr: string of attribute/global variable to be changed
        :param new_value: new value for the corresponding attribute
        """
        try:
            if self.attribute_map[attr] == 'buttonstate':
                # print('"{0}" changed from {1} to {2}'.format(attr, self.buttonstate, new_value))
                self.buttonstate = new_value
            elif self.attribute_map[attr] == 'buttononstate':
                # print('"{0}" changed from {1} to {2}'.format(attr, self.buttononstate, new_value))
                self.buttononstate = new_value
            elif self.attribute_map[attr] == 'buttonoffstate':
                # print('"{0}" changed from {1} to {2}'.format(attr, self.buttonoffstate, new_value))
                self.buttonoffstate = new_value
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

    def _print(self):
        print("=== BUTTON INFORMATION ===\n"
              "Name: {0}\n"
              "Current State: {1}\n"
              "On State: {2}\n"
              "Off State: {3}\n"
              "Center: {4}\n"
              "Width/Height: {5}/{6}\n"
              "Color: {7}".format(self.name, self.buttonstate, self.buttononstate, self.buttonoffstate, self.center,
                                  self.width, self.height, self.color))

    def get_name(self):
        return copy(self.name)

    def get_info_attributes(self):
        attrs = list()
        attrs.append('Internal state: {}'.format('ON' if self.internal_state else 'OFF'))
        return attrs


# This is the main button class
class Button(_button):
    def __init__(self, input_settings):
        settings = {'name': "", 'state': 0, 'on_state': 1, 'off_state': 0, 'style': 0,
                    'center': [0, 0], 'width': 20, 'height': 40, 'color_map': (100, 100, 100),
                    'shapes': [
                        {'type': 'rect',
                         'color': (175, 175, 175),
                         'settings':
                             {'center': [0, 0],
                              'width': 20,
                              'height': 40}},
                        {'type': 'rect',
                         'color': None,
                         'settings':
                             {'center': [0, 0],
                              'width': 10,
                              'height': 30}}]}

        for set in settings.keys():
            if set in input_settings:
                settings[set] = input_settings[set]

        _button.__init__(self, settings['name'], settings['state'], settings['on_state'], settings['off_state'],
                         settings['style'], settings['center'], settings['width'], settings['height'],
                         settings['color_map'], settings['shapes'])

    def _handle_action(self, action_type):
        if action_type == 'LEFT_MOUSE_DOWN' or action_type == 'LEFT_MOUSE_UP':
            return self.toggle_internal_state()

    # MISC
    def print(self):
        self._print()


# Button0 is the 'hold down and release' button
class Button0(Button):
    def __init__(self, input_settings):
        # Handle unique properties for Button 0
        if 'style' not in input_settings:
            input_settings['style'] = 0
        else:
            assert input_settings['style'] == 0, 'INVALID STYLE FOR BUTTON 0'

        if 'color_map' in input_settings:
            assert len(input_settings['color_map']) >= 2, 'NEED AT LEAST TWO COLORS'
        else:
            input_settings['color_map'] = [(255, 0, 0), (0, 255, 0)]

        Button.__init__(self, input_settings)

    def handle_action(self, action_type):
        return self._handle_action(action_type)

    def draw(self, surface):
        self._draw(surface)


# Unit test
if __name__ == "__main__":
    print("Running unit test for Button class...")
    butt = Button0({'name': 'butt_name',
                    'state': 0,
                    'center': [0, 0]})
    butt.print()
    print("")
    print("Updating current state...")
    butt.update_state(1)
    butt.print()

    try:
        butt.toggle_internal_state()
        if butt.buttonstate not in range(butt.maxstate):
            print('UNIT TEST ERROR: This should have failed!')
    except AssertionError:
        pass
