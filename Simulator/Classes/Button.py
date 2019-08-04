"""
Created: July 13, 2019
Last Updated: August 3, 2019

Author: StolenLight

=== DESCRIPTION ===
This class simulates the functionality of a Button in Starbase. As there are
three types of buttons, all buttons will have a subclass to inherit all common
features
"""
from .pygame_obj import PygameObj


# This is the sub-class
class _button(PygameObj):
    def __init__(self, name, state, on_state, off_state, style, position, width, height, color_map):
        """
        :param state: The current state of the button
        :param on_state: The state which signifies button is in 'on state'
        :param off_state: The state which signifies button is in 'off state'
        :param style: The style of the button...
            0: Hold down and release
            1: Basic Toggle (simple click to toggle)
            2: 4-state switch (like a click pen)
        :param position: The position of the button on the main surface
        :param color_map: The color map for all potential states of the button
        """
        # Button parameters
        self.name = name
        self.buttonstate = state
        self.buttononstate = on_state
        self.buttonoffstate = off_state
        self.buttonstyle = style

        # Pygame object init
        PygameObj.__init__(self, position, width, height, color_map)

        # Assertions
        self.run_assert()

    def run_assert(self):
        if self.buttonstyle == 0 or self.buttonstyle == 1:
            assert self.buttonstate in range(0, 2), \
                'INVALID BUTTON STATE: Button Style "%s" only allows for 2 states' % self.buttonstyle
        elif self.buttonstyle == 2:
            assert self.buttonstate in range(0, 5), \
                'INVALID BUTTON STATE: Button Style "%s" only allows for 4 states' % self.buttonstyle

    def update_state(self, new_state):
        print("Button {0} updated state from {1} to {2}".format(
            self.name, self.buttonstate, new_state))
        self.buttonstate = new_state
        self.run_assert()
        self.update_color()

    def update_color(self):
        self.color = self.color_map[self.buttonstate]

    def _print(self):
        print("=== BUTTON INFORMATION ===\n"
              "Name: {0}\n"
              "Current State: {1}\n"
              "On State: {2}\n"
              "Off State: {3}\n"
              "Position: {4}\n"
              "Width/Height: {5}/{6}\n"
              "Color: {7}".format(self.name, self.buttonstate, self.buttononstate, self.buttonoffstate, self.position,
                                  self.width, self.height, self.color))


# This is the main button class
# TODO: Add button style specific settings
class Button(_button):
    def __init__(self, input_settings):
        settings = {'name': "", 'state': 0, 'on_state': 1, 'off_state': 0, 'style': 0,
                    'position': [0, 0], 'width': 10, 'height': 20, 'color_map': (100, 100, 100)}

        for set in settings.keys():
            if set in input_settings:
                settings[set] = input_settings[set]

        _button.__init__(self, settings['name'], settings['state'], settings['on_state'], settings['off_state'],
                         settings['style'], settings['position'], settings['width'], settings['height'],
                         settings['color_map'])

    # MISC
    def print(self):
        self._print()


# Unit test
if __name__ == "__main__":
    print("Running unit test for Button class...")
    butt = Button({"name": 'Test', "state": 1, "on_state": 2, "off_state": 0, "style": 2})
    butt.print()
    print("")
    print("Updating current state...")
    butt.update_state(2)
    butt.print()
