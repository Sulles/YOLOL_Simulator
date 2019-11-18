"""
Created: October 12, 2019

Author: Sulles

=== DESCRIPTION ===
This library file houses all the objects required for the GUI. It currently has:
- ListObj
- InputExtendedListObj
- ErrorObj
- TabObj
- TabList
TODO: create new TextBox
"""

from copy import copy
from math import sqrt

# noinspection PyUnresolvedReferences
from Classes.pygame_obj import PygameObj
from pygame import font as pygame_font
from pygame import draw as pygame_draw
# noinspection PyUnresolvedReferences
from src.constants import colors, FONT_TO_PIXEL_FACTOR


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
                self.entry_value_map[active_entry] += 1
                self.update_values()
        elif action_type == 'RIGHT_MOUSE_DOWN':
            active_entry = self.main_list.handle_right_mouse_down(mouse_pos)
            if active_entry is not None:
                self.entry_value_map[active_entry] -= 1
                self.update_values()
        elif action_type == 'MOUSE_HOVER':
            self.main_list.handle_hover(mouse_pos)
        else:
            return None


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

    def get_tab_center(self, tab_info):
        return copy(self.tabs[tab_info['index']].center)

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
        if action_type == 'MOUSE_HOVER':
            for tab in self.tabs:
                tab.handle_mouse_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            print('Got left click. How many tabs?: {0} should match {1}'.format(len(self.tabs), self.tab_names))
            activated_tab_name = None
            for tab in self.tabs:
                print('Checking {}'.format(self.tab_names[self.tabs.index(tab)]))
                if tab.in_hit_box(mouse_pos):
                    self.deactivate_all_tabs()
                    tab.activate()
                    activated_tab_name = copy(tab.name)
            return activated_tab_name
        return None

    def deactivate_all_tabs(self):
        for tab in self.tabs:
            tab.deactivate()

    def get_active_tab(self):
        for tab in self.tabs:
            if tab.is_active:
                return dict(name=tab.name, index=self.tabs.index(tab))
        return None


class DisplayBox(PygameObj):
    def __init__(self, text, middle_left, width=None, height=20, center=None, border=True, font=None):
        """
        Constructor for basic display box of text
        :param text: string of text to be displayed
        :param middle_left: list [x, y] in pixels that corresponds to the 'middle left', aka start, position of the box
        :param width: default to None and will automatically be adjusted to wrap around entire text
        :param height: default to 30 pixels
        :param center: if you want to pass center instead of middle_left... 'cause
        """
        self.name = text
        self.is_selected = False
        text = text.upper()

        # Handle auto-width
        if width is None:
            width = int((len(text) ** 0.8) * FONT_TO_PIXEL_FACTOR)

        # Handle auto-center
        if center is None:
            center = [middle_left[0] + int(0.5 * width), middle_left[1]]

        # Handle border vs background for default color_map
        shape = {'type': 'rect',
                 'color': None,
                 'settings': {
                     'center': [0, 0],
                     'width': width,
                     'height': height
                 }}
        if border:
            shape['width'] = 1
            self.color_map = [colors['WHITE']]
        else:
            self.color_map = [colors['BGCOLOR'], colors['BLUE'], colors['DARKGREEN']]

        # Handle font, WARNING: this will mess with auto-width calculations
        if font is None:
            font = pygame_font.Font('src/Cubellan.ttf', 10)

        PygameObj.__init__(self, center, width, height, self.color_map, [shape], text=text, Font=font)

    def select(self):
        self.is_selected = True
        self.update_color(2)

    def deselect(self):
        self.is_selected = False
        self.update_color(0)

    def handle_action(self, action_type, mouse_pos, key=None):
        if action_type == 'LEFT_MOUSE_DOWN':
            if self.in_hit_box(mouse_pos) and len(self.color_map) > 1:
                print('"{}" was selected!'.format(self.name))
                self.select()
                return 'selected'
            else:
                self.deselect()
        elif action_type == 'MOUSE_HOVER' and len(self.color_map) > 1:
            if self.in_hit_box(mouse_pos):
                self.update_color(1)
            elif not self.is_selected:
                self.update_color(0)
        return None


class CheckBox(PygameObj):
    def __init__(self, center, text, color_map=None, width=None, height=50, font=None):
        """
        Constructor for a generic check box to all the user to 'submit' something
        :param text: String to display
        :param center: list [x, y] pixel location of check_box
        :param width: pixel width of check_box
        :param height: pixel height of check_box
        """
        self.name = text
        if color_map is None:
            color_map = [colors['BGCOLOR'], colors['DARKGREEN']]
        if font is None:
            font = pygame_font.Font('src/Cubellan.ttf', 16)
        if width is None:
            width = int((len(text) ** 0.8) * FONT_TO_PIXEL_FACTOR * 1.5)
        PygameObj.__init__(self, center, width, height, color_map,
                           [{'type': 'rect',
                             'color': None,
                             'settings': {
                                 'center': [0, 0],
                                 'width': width,
                                 'height': height}}],
                           text, Font=font)

    def handle_action(self, action_type, mouse_pos, key=None):
        if action_type == 'LEFT_MOUSE_DOWN':
            if self.in_hit_box(mouse_pos):
                print('"{}" was selected!'.format(self.name))
                return 'selected'
        elif action_type == 'MOUSE_HOVER':
            if self.in_hit_box(mouse_pos):
                self.update_color(1)
            else:
                self.update_color(0)
        return None


class InputBox(PygameObj):
    def __init__(self, center, width=30, height=30, color_map=None, font=None, font_to_pixel=None):
        """
        Constructor for the TextBox object
        :param center: list of length 2, [x, y] in pixels
        :param width: int of pixel width, default to None and will adjust to length of prompt
        :param height: int of pixel height
        :param color_map: list of colors
        :param font: Pygame font for displaying text
        :param font_to_pixel: text-to-pixel offset
        """
        color_map = [colors['BGCOLOR'], colors['DARKGRAY']] if color_map is None else color_map
        self.font = pygame_font.Font('src/Cubellan.ttf', 16) if font is None else font
        PygameObj.__init__(self, center, width, height, color_map,
                           [{'type': 'rect',
                             'color': None,
                             'settings': {
                                 'center': [0, 0],
                                 'width': width,
                                 'height': height}}],
                           text="", Font=font)
        self.is_active = False
        self.text = ""
        self.font_to_pixel = 6.5 if font_to_pixel is None else font_to_pixel

    def activate(self):
        self.is_active = True
        self.update_color(1)
        return dict(type='activated')

    def deactivate(self):
        self.is_active = False
        self.update_color(0)
        return dict(type='deactivated')

    def add_key(self, key):
        if key == 8:  # if delete, remove last character
            self.text = self.text[:-1]
        elif (65 <= key <= 90) or (97 <= key <= 122):
            key = chr(key)
            self.text += key
        else:
            print('Unsupported character: {}'.format(chr(key)))
            return
        new_width = int(len(self.text) * self.font_to_pixel) + 30
        half_width_diff = int((new_width - self.width) / 2)
        print('Current text: {}'.format(self.text))
        self.update_text(self.text, self.font)
        self.widen(half_width_diff * 2)
        self.shift_center([half_width_diff, 0])
        return dict(type='shift_center', shift=[half_width_diff * 2, 0])

    def handle_action(self, action_type, mouse_pos, key=None):
        if action_type == 'MOUSE_HOVER':
            if self.in_hit_box(mouse_pos):
                self.update_color(1)
            elif not self.is_active:
                self.update_color(0)
        elif action_type == 'LEFT_MOUSE_DOWN':
            if self.in_hit_box(mouse_pos):
                return self.activate()
            else:
                return self.deactivate()
        elif action_type == 'KEY_DOWN' and self.is_active:
            print('got key: {}'.format(chr(key)))
            return self.add_key(key)
        return None


class ModifyTextBox:
    def __init__(self, prompt, center, width=None, height=50, font=None):
        """
        Constructor for the TextBox object
        :param prompt: string of prompt for user input
        :param center: list of length 2, [x, y] in pixels
        :param width: int of pixel width, default to None and will adjust to length of prompt
        :param height: int of pixel height
        """
        self.height = height

        print('center: {}'.format(center))
        if font is None:
            font = pygame_font.Font('src/Cubellan.ttf', 14)

        # Display current text
        self.objects = list()
        if width is None:
            width = int((len(prompt) ** 0.8) * FONT_TO_PIXEL_FACTOR * 1.2)
        self.objects.append(DisplayBox(prompt, None, width, height, center, border=False, font=font))

        # Setup input box
        center[0] += int(width / 2) + 25
        print('center: {}'.format(center))
        self.objects.append(InputBox(center, font=font))

        # Build check box
        self.submit_width = int((len('Submit') ** 0.8) * FONT_TO_PIXEL_FACTOR * 1.2)
        center[0] += 30 + int(self.submit_width / 2)
        print('center: {}'.format(center))
        self.objects.append(CheckBox(center, 'Submit', height=30, font=font))

        self.font_to_pixel = 6.5

    def draw(self, surface):
        self.draw_rect(surface)
        for obj in self.objects:
            obj.draw(surface)

    def draw_rect(self, surface):
        top_left = [self.objects[0].center[0] - int(self.objects[0].width / 2) - 1,
                    self.objects[0].center[1] + int(self.height / 2) + 1]
        top_right = [self.objects[2].center[0] + int(self.objects[2].width / 2) + 2,
                     self.objects[2].center[1] + int(self.height / 2) + 1]
        bottom_right = [top_right[0], top_right[1] - self.height - 2]
        bottom_left = [top_left[0], top_left[1] - self.height - 2]
        pygame_draw.lines(surface, colors['WHITE'], True, [top_left, top_right, bottom_right, bottom_left])

    def handle_submission(self):
        # get new text
        text = copy(self.objects[1].text)

        # clear old text and shift back input & submit boxes
        self.objects[1].update_text("", text_to_width_factor=self.font_to_pixel)
        self.objects[1].shift_center([int(-self.font_to_pixel / 2 * len(text)), 0])
        self.objects[2].shift_center([int(-self.font_to_pixel * len(text)), 0])

        # git diff of display text width
        old_display_width = self.objects[0].width
        new_display_width = int(self.font_to_pixel * len(text) + 30)
        width_diff = new_display_width - old_display_width

        # Pass text to display box
        self.objects[0].update_text(text, text_to_width_factor=self.font_to_pixel)

        # shift input & submit boxes based off of new width diff / 2
        self.objects[1].shift_center([int(width_diff / 2), 0])
        self.objects[2].shift_center([int(width_diff / 2), 0])

    def handle_action(self, action_type, mouse_pos, key=None):
        for obj in self.objects:
            response = obj.handle_action(action_type, mouse_pos, key)
            if type(response) is dict and 'type' in response.keys():
                if response['type'] == 'shift_center':
                    self.objects[-1].shift_center(response['shift'])
                elif response['type'] == 'activated':
                    self.objects[0].select()
                elif response['type'] == 'deactivated':
                    self.objects[0].deselect()
            elif response == 'selected':
                if obj.name == 'Submit':
                    self.handle_submission()
