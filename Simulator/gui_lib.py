"""
Created: October 12, 2019

Author: Sulles

=== DESCRIPTION ===
This library file houses all the objects required for the GUI. It currently has:
- ListObj
- InputExtendedListObj
TODO: test DisplayExtendedList
- ErrorObj
- TabObj
- TabList
TODO: create new TextBox
"""

from copy import copy
from math import sqrt

from pygame import font as pygame_font

from Classes.pygame_obj import PygameObj
from src.constants import colors


def distance(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class ListObj:
    """
    This object will create a list of PygameObj objects to be displayed
    """

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
        self.font = pygame_font.Font('src/Cubellan.ttf', 16)
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
                PygameObj([int(self.screen_size['width'] / 2) + self.x_offset,
                           int(100 + (self.height * 1.5 * x) + self.y_offset)],
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
                self.active_entry = obj.get_name()
            else:
                obj.update_color(0)

    def handle_left_mouse_down(self, mouse_pos):
        for obj in self.objects:
            if obj.in_hit_box(mouse_pos):
                print('Got left click "%s" in list object' % self.active_entry)
                return self.active_entry
        print('Got un-interesting left click, ignoring')

    def handle_right_mouse_down(self, mouse_pos):
        for obj in self.objects:
            if obj.in_hit_box(mouse_pos):
                print('Got right click "%s" in list object' % self.active_entry)
                return self.active_entry
        print('Got un-interesting right click, ignoring')


class InputExtendedListObj:
    def __init__(self, list_of_entry_names, screen_size, width=100, height=30, x_offset=0, y_offset=0):
        """
        This object is a List object with an additional box to the right to display how many times the obj was
        selected (left-click) or deselected (right-click)
        :param list_of_entry_names: list of strings for objects to be selected
        :param screen_size: dictionary with 'width' and 'height' keys
        :param width: int of intended width of each List object
        :param height: int of intended height of each List object
        :param x_offset: int (pixel) x-offset from center of 'screen size'
        :param y_offset: int (pixel) y-offset from center of 'screen size'
        """
        self.entry_names = list_of_entry_names
        self.screen_size = screen_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.main_list = ListObj(list_of_entry_names, screen_size, width=width, height=height, x_offset=x_offset,
                                 y_offset=y_offset)
        self.entry_value_map = dict()
        for _ in list_of_entry_names:
            self.entry_value_map[_] = 0
        self.values_list = None
        self.update_values()

    def draw(self, surface):
        self.main_list.draw(surface)
        self.values_list.draw(surface)

    def check_values_range(self):
        for key, value in self.entry_value_map.items():
            if value < 0:
                self.entry_value_map[key] = 0

    def update_values(self):
        self.check_values_range()
        self.values_list = ListObj(list([str(_) for _ in self.entry_value_map.values()]), self.screen_size,
                                   width=30, height=30, x_offset=self.x_offset + 80, y_offset=self.y_offset)

    def get_network(self):
        return copy(self.entry_value_map)

    def clear_data(self):
        for key in self.entry_value_map.keys():
            self.entry_value_map[key] = 0

    def handle_action(self, action_type, mouse_pos=None):
        if action_type == 'LEFT_MOUSE_DOWN':
            active_entry = self.main_list.handle_left_mouse_down(mouse_pos)
            if active_entry is not None:
                self.entry_value_map[self.entry_names[active_entry]] += 1
                self.update_values()
        elif action_type == 'RIGHT_MOUSE_DOWN':
            active_entry = self.main_list.handle_right_mouse_down(mouse_pos)
            if active_entry is not None:
                self.entry_value_map[self.entry_names[active_entry]] -= 1
                self.update_values()
        elif action_type == 'MOUSE_HOVER':
            self.main_list.handle_hover(mouse_pos)
        else:
            return None


class DisplayExtendedList:
    """
    This object will display the name and info for a list of objects
    """

    def __init__(self, network, screen_size, width=100, height=30, x_offset=0, y_offset=0):
        """
        Constructor
        :param network: Network object
        :param screen_size: dictionary with 'width' and 'height' keys
        :param width: int of intended width of each List object
        :param height: int of intended height of each List object
        :param x_offset: int (pixel) x-offset from center of 'screen size'
        :param y_offset: int (pixel) y-offset from center of 'screen size'
        """
        self.network = network
        self.name_list = [obj.get_name() for obj in network.objects]
        self.name_obj = ListObj(self.name_list, screen_size, width=width, height=30*len(self.name_list),
                                x_offset=x_offset, y_offset=y_offset)

        self.info_list = list()
        self.check_for_attribute_updates()
        self.info_obj = [ListObj(info_bits, screen_size, width=100, height=30*len(info_bits), x_offset=x_offset + 120,
                                 y_offset=y_offset) for info_bits in self.info_list]

    def update_attributes_list(self):
        if self.check_for_attribute_updates():
            for x in range(len(self.info_list)):
                self.info_obj[x].update_text(self.info_list[x])

    def check_for_attribute_updates(self):
        """
        This function checks if any objects have updated attributes.
        If changes were detected, self.info_list is updated, the info_obj text is updated, and this function
            returns True
        Otherwise returns False
        :return:
        """
        current_info = [obj.get_info_attributes() for obj in self.network.objects]
        was_change = False
        for x in range(len(current_info)):
            if current_info[x] != self.info_list[x]:
                self.info_list[x] = current_info[x]
                was_change = True
        return was_change


class ErrorObj(PygameObj):
    def __init__(self, text, screen_size):
        center = [int(screen_size['width'] / 2), int(screen_size['height'] / 2)]
        PygameObj.__init__(self, center,
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
                           Font=pygame_font.Font('src/Cubellan.ttf', 20))


class TabObj(PygameObj):
    def __init__(self, name, center, font=None):
        """
        Constructor for Tab Object
        :param name: string name of the tab
        :param center: pixel center of the tab
        :param font: pygame font object
        """
        self.name = name
        self.is_active = False
        width = 100
        height = 28
        point_list = [[int(-width / 2), int(-height / 2)],
                      [int(width / 2), int(-height / 2)],
                      [int(width / 2 - 4), int(height / 2)],
                      [int(4 - width / 2), int(height / 2)]]
        PygameObj.__init__(self, center, width, height, [colors['NAVYBLUE'], colors['DARKGRAY']],
                           [{'type': 'point_list',
                             'point_list': point_list,
                             'color': None}],
                           text=name, Font=font)

    def handle_mouse_hover(self, mouse_pos):
        if self.in_hit_box(mouse_pos) or self.is_active:
            self.update_color(1)
        else:
            self.update_color(0)

    def activate(self):
        print('Activating {}'.format(self.name))
        self.is_active = True
        return copy(self.name)

    def deactivate(self):
        print('Deactivating {}'.format(self.name))
        self.is_active = False
        return None


class TabList:
    def __init__(self, font, initial_tabs=None):
        """
        Constructor for a list of tabs
        :param font: pygame font object
        :param initial_tabs: list of initial tabs
        """
        self.font = font
        self.tab_names = list()
        self.tabs = list()
        if initial_tabs is not None:
            for _ in initial_tabs:
                self.add_tab(_)

    def add_tab(self, name):
        print('Adding tab to tabs list: "{}"'.format(name))
        self.tab_names.append(name)
        center = self.calculate_center(self.tab_names.index(name))
        self.tabs.append(TabObj(name, center, self.font))
        for tab in self.tabs:
            tab.deactivate()
        return self.tabs[-1].activate()

    def get_tab_center(self, index):
        return copy(self.tabs[index].center)

    @staticmethod
    def calculate_center(index):
        return [int(150 + 100 * index), int(14)]

    def remove_tab(self, name):
        index = self.tab_names.index(name)
        self.tab_names.remove(name)
        del self.tabs[index]
        self.recreate_tabs()

    def recreate_tabs(self):
        self.tabs = list()
        if len(self.tab_names) > 0:
            for name in self.tab_names:
                return copy(self.add_tab(name))

    def draw(self, surface):
        for tab in self.tabs:
            tab.draw(surface)

    def handle_action(self, action_type, mouse_pos):
        # TODO: Tabs should not be de-focused when user clicks on something that is not a tab
        if action_type == 'MOUSE_HOVER':
            for tab in self.tabs:
                tab.handle_mouse_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            print('Got left click. How many tabs?: {0} should match {1}'.format(len(self.tabs), self.tab_names))
            activated_tab_name = None
            for tab in self.tabs:
                print('Checking {}'.format(self.tab_names[self.tabs.index(tab)]))
                if tab.in_hit_box(mouse_pos):
                    tab.activate()
                    activated_tab_name = copy(tab.name)
                else:
                    tab.deactivate()
            return activated_tab_name
        return None


class TextBox:
    def __init__(self, prompt, center, width=300, height=100, color_map=None, Font=None):
        """
        Constructor for the TextBox object
        :param prompt: string of prompt for user input
        :param center: list of length 2, [x, y] in pixels
        :param width: int of pixel width
        :param height: int of pixel height
        :param color_map: list of colors
        :param Font: pygame Font object for displaying text
        """
        pass
