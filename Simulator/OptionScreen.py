"""
Created August 13, 2019

Author: Sulles

This file houses the Options Screen class and is a part of the GUI for the simulator

Available options:
    1. Edit networks:
        A. Modify objects on an existing network
        A. Create a new network
        B. Remove a network
    2. Edit code for YOLOL chips
        A. Select YOLOL chip from list of available chips
            - Edit code and click save
    3. Edit simulator settings
        A. Change size of window
        B. Change FPS (default 60)
"""

# noinspection PyUnresolvedReferences
from Classes import Button, Chip, Lamp, map, Network, pygame_obj
from pygame import font
from math import sqrt


class ErrorObj(pygame_obj.PygameObj):
    def __init__(self, text, screen_size):
        center = [int(screen_size['width'] / 2), int(screen_size['height'] / 2)]
        pygame_obj.PygameObj.__init__(self, center,
                                      0, 0, [(200, 0, 0)], [
                                          {'type': 'rect',
                                           'color': None,
                                           'settings': {
                                               'center': [0, 0],
                                               'width': 500,
                                               'height': 500
                                           }}
                                      ],
                                      text=text,
                                      Font=font.Font('src/Cubellan.ttf', 20))


class ListObj:
    def __init__(self, list_of_entries, screen_size, width=300, height=50, x_offset=0, y_offset=0):
        """
        Constructor
        :param list_of_entries: a list of strings
        :param screen_size: list/tuple of length 2 where id 0 = width and id 1 = height
        :param width: int pixel width of box for each item in the list
        :param height: int pixel height of box for each item in the list
        :param x_offset: int of how far left/right the screen list will start to be displayed in pixels
        :param y_offset: int of how far up/down the screen list will start to be displayed in pixels
        """
        self.entries = list_of_entries
        self.screen_size = screen_size
        self.objects = []
        self.font = font.Font('src/Cubellan.ttf', 16)
        self.active_entry = None
        self.width = width
        self.height = height
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.init_objects()

    def init_objects(self):
        # print('Instantiating new List Object. List of entries: {}'.format(
        #     list_of_entries))
        for x in range(0, len(self.entries)):
            # print('Creating shape for list entry "%s"' % list_of_entries[x])
            shapes = list()
            shapes.append(
                {'type': 'rect',
                 'color': (255, 255, 255),
                 'width': 2,
                 'settings': {
                     'center': [0, 0],
                     'width': self.width,
                     'height': self.height}})
            shapes.append(
                {'type': 'rect',
                 'color': None,
                 'settings': {
                     'center': [0, 0],
                     'width': self.width - 20,
                     'height': self.height - 10}})

            self.objects.append(
                pygame_obj.PygameObj([int(self.screen_size['width'] / 2) + self.x_offset,
                                      int(self.screen_size['height'] / 2 + (self.height * 1.5 * x) + self.y_offset)],
                                     self.width, self.height, [(0, 0, 0), (100, 100, 100), (0, 200, 0)], shapes,
                                     text=self.entries[x],
                                     Font=self.font))

    def update_text(self, text_list):
        try:
            assert len(text_list) == len(self.entries), \
                'Please provide a text list for every entry! You provided {0} entries, you need {1}!'.format(
                    len(text_list), len(self.entries))
            self.entries = text_list
            self.objects = list()
            self.init_objects()

        except Exception:
            print('Could not update text! Was given input: {}'.format(text_list))

    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

    def handle_hover(self, mouse_pos):
        self.active_entry = None
        for obj in self.objects:
            if obj.in_hit_box(mouse_pos):
                obj.update_color(1)
                self.active_entry = self.objects.index(obj)
            else:
                obj.update_color(0)

    def handle_left_mouse_down(self, mouse_pos):
        for obj in self.objects:
            if obj.in_hit_box(mouse_pos):
                print('Got left click "%s" in list object' % self.entries[self.active_entry])
                return self.active_entry
        print('Got un-interesting left click, ignoring')

    def handle_right_mouse_down(self, mouse_pos):
        for obj in self.objects:
            if obj.in_hit_box(mouse_pos):
                print('Got right click "%s" in list object' % self.entries[self.active_entry])
                return self.active_entry
        print('Got un-interesting right click, ignoring')

    @staticmethod
    def distance(a, b):
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class OptionScreen:
    def __init__(self, screen_size):
        self.is_active = False

        # Simple dictionary of all settings, with key as first layer text, and value as sub-layer text
        self.options_text = {
            'Edit networks': ['Create a new network', 'Edit objects in a network', 'Delete a network'],
            'Edit YOLOL code': [],
            'Edit simulator settings': ['Change screen size', 'Change FPS'],
            'Exit': []
        }

        self.main_list = ListObj([_ for _ in self.options_text.keys()], screen_size, y_offset=-150)
        self.network_list = ListObj(self.options_text['Edit networks'], screen_size, y_offset=-150)
        self.yolol_list = ListObj(self.options_text['Edit YOLOL code'], screen_size, y_offset=-150)
        # TODO: make sure yolol_list can be updated appropriately, will probably need to create a new obj for each
        #  new chip created
        self.simulator_list = ListObj(self.options_text['Edit simulator settings'], screen_size)
        self.selected_key = None
        self.current_list_obj = None
        self.update_current_list()

        self.error = None
        self.error_screens = dict()
        self.error_screens['incomplete_feature'] = ErrorObj('Incomplete Feature!', screen_size)

    def print(self):
        print('=== OPTION SCREEN INFO ===\n'
              'Error State: {0}\n'
              'Selected Key: {1}\n'
              'Current List Selected: {2}'.format(self.error, self.selected_key, self.current_list_obj.entries))

    def update_current_list(self):
        if isinstance(self.selected_key, int):
            key_map = []
            if self.current_list_obj == self.main_list:
                key_map = [str(_) for _ in self.options_text.keys()]
            elif self.current_list_obj == self.network_list:
                key_map = [str(_) for _ in self.options_text['Edit networks']]
            # elif self.current_list_obj == self.yolol_list:
            #     key_map =
            elif self.current_list_obj == self.simulator_list:
                key_map = [str(_) for _ in self.options_text['Edit simulator settings']]
            # print('Mapped key to: "%s"' % self.selected_key)
            self.selected_key = key_map[self.selected_key]

        # MAIN LIST OPTIONS
        if self.selected_key is None:
            self.current_list_obj = self.main_list
        elif self.selected_key == 'Edit networks':
            self.current_list_obj = self.network_list
        elif self.selected_key == 'Edit YOLOL code':
            if len(self.options_text['Edit YOLOL code']) == 0:
                print('No YOLOL chips edit!')
                self.current_list_obj = self.main_list
                self.selected_key = None
            else:
                print('what is yolol list right now? "{}"'.format(self.yolol_list))
                # TODO: self.current_list_obj = ???
        elif self.selected_key == 'Edit simulator settings':
            self.current_list_obj = self.simulator_list
        elif self.selected_key == 'Exit':
            return dict(type='terminate')

        # EDIT NETWORK OPTIONS
        elif self.selected_key == 'Create a new network':
            # print('You want to create a new network! Cool!')
            return dict(type='add_network')
        elif self.selected_key == 'Edit objects in a network':
            print('You want to edit something in a network! Cool!')
            return dict(type='edit_network')
        elif self.selected_key == 'Delete a network':
            print('CHOP CHOP time!')
            return dict(type='start_delete_network')

        else:
            print('what even is the selected key?: {}'.format(self.selected_key))
            # TODO: change this error type when all features have been implemented
            self.error = 'incomplete_feature'

        if self.current_list_obj is None:
            print('Nothing to display, returning to main menu...')
            self.current_list_obj = self.main_list

    def toggle_activate(self):
        if self.is_active:
            self.deactivate()
        else:
            self.activate()
        self.error = False

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def draw(self, surface):
        if self.error:
            self.error_screens[self.error].draw(surface)
        else:
            self.current_list_obj.draw(surface)

    def handle_action(self, action_type, mouse_pos=None):
        if action_type == 'ESCAPE' and self.selected_key is not None:
            self.selected_key = None
            self.update_current_list()
        elif action_type == 'ESCAPE':
            self.toggle_activate()
        elif action_type == 'MOUSE_HOVER':
            self.current_list_obj.handle_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            self.selected_key = self.current_list_obj.handle_left_mouse_down(mouse_pos)
            return self.update_current_list()
        else:
            print('Unsupported action detected! Got: ""{}""'.format(action_type))
        return None

    def show_incomplete_feature(self):
        self.is_active = True
        self.error = 'incomplete_feature'
