"""
Created: July 13, 2019
Last Updated: August 3, 2019

Author: StolenLight

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
        self.buttononstate = on_state
        self.buttonoffstate = off_state
        self.buttonstyle = style
        self.maxstate = 0

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

    def increment_state(self):
        self.update_state((self.buttonstate + 1) % self.maxstate)

    def update_state(self, new_state):
        print('Button "{0}" updated state from {1} to {2}'.format(
            self.name, self.buttonstate, new_state))
        self.buttonstate = new_state
        self.run_assert()
        self._update_color(self.buttonstate)

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
        if action_type == 'LEFT_MOUSE_DOWN':
            self.increment_state()

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
        if action_type == 'LEFT_MOUSE_DOWN':
            self.increment_state()
        if action_type == 'LEFT_MOUSE_UP':
            self.increment_state()

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
        butt.increment_state()
        if butt.buttonstate not in range(butt.maxstate):
            print('UNIT TEST ERROR: This should have failed!')
    except AssertionError:
        pass
