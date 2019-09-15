"""
Created: August 3, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This class houses the GUI
"""
import pygame.draw
import pygame.font
# noinspection PyUnresolvedReferences
from Classes.map import obj_map
# noinspection PyUnresolvedReferences
from Classes.pygame_obj import PygameObj
# noinspection PyUnresolvedReferences
from OptionScreen import ListObj
from pygame import Rect
# noinspection PyUnresolvedReferences
from src.constants import colors


class ExtendedListObj:
    def __init__(self, list_of_entry_names, screen_size, width=300, height=50, x_offset=0, y_offset=0):
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


class TabObj(PygameObj):
    def __init__(self, name, center, font):
        """
        Constructor for Tab Object
        :param name: string name of the tab
        :param center: pixel center of the tab
        """
        self.name = name
        self.is_active = False
        width = 100
        height = 28
        point_list = [[int(4 - width / 2), int(-height / 2)],
                      [int(width / 2 - 4), int(-height / 2)],
                      [int(width / 2), int(height / 2)],
                      [int(-width / 2), int(height / 2)]]
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

    def deactivate(self):
        print('Deactivating {}'.format(self.name))
        self.is_active = False


class TabList:
    def __init__(self, font):
        self.font = font
        self.tab_names = list()
        self.tabs = list()

    def add_tab(self, name):
        print('Adding tab to tabs list: "{}"'.format(name))
        self.tab_names.append(name)
        center = self.calculate_center(self.tab_names.index(name))
        self.tabs.append(TabObj(name, center, self.font))
        return self.tabs[-1].activate()

    @staticmethod
    def calculate_center(index):
        return [int(60 + 100 * index), int(20)]

    def remove_tab(self, name):
        index = self.tab_names.index(name)
        self.tab_names.remove(name)
        del self.tabs[index]
        self.recreate_tabs()

    def recreate_tabs(self):
        self.tabs = list()
        if len(self.tab_names) > 0:
            for name in self.tab_names:
                return self.add_tab(name)

    def draw(self, surface):
        for tab in self.tabs:
            tab.draw(surface)

    def handle_action(self, action_type, mouse_pos):
        if action_type == 'MOUSE_HOVER':
            for tab in self.tabs:
                tab.handle_mouse_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            for tab in self.tabs:
                if tab.in_hit_box(mouse_pos):
                    tab.activate()
                    return tab.name
                else:
                    tab.deactivate()
        return None


class GUI:
    def __init__(self, display_settings):
        self.display_settings = display_settings
        self.center = [int(display_settings['width'] / 2),
                       int(display_settings['height'] / 2)]

        # SETTING UP FONT
        self.small_font = pygame.font.Font('src/Cubellan.ttf', 8)
        self.basic_font = pygame.font.Font('src/Cubellan.ttf', 12)
        self.large_font = pygame.font.Font('src/Cubellan.ttf', 18)

        # SETTING UP NETWORK BARS
        self.tab_list = TabList(self.basic_font)
        self.current_tab = None
        self.network_names = []

        # SETTING UP NETWORK SPECIFIC INFO
        self.position = [10, 35]
        self.width = 100
        self.height = int(display_settings['height'] / 2)
        self.color = (100, 100, 100)
        self.net_color_map = [self.color, colors['WHITE'], colors['WHITE']]
        self.net_width_map = [0, 1, 1]
        self.net_info = []
        self.net_info.append(Rect(self.position[0], self.position[1], self.width, self.height))
        self.net_info.append(Rect(self.position[0] + 2, self.position[1] + 2, self.width - 4, self.height - 4))
        self.net_info.append(Rect(self.position[0] + 4, self.position[1] + 4, self.width - 8, self.height - 8))

        # CREATING NETWORK STUFF
        self.creating_network = False
        self.create_step = 0
        self.create_steps = ['select_objects', 'modify_attributes', 'instantiate_network']
        self.select_objects_list = ExtendedListObj(list(obj_map.keys()), display_settings,
                                                   width=100, height=30, x_offset=-300, y_offset=-100)
        # TODO: add something for modify_attributes and instantiate_network to option_obj_map

    def add_network(self, name, network):
        print('Adding network "{}"'.format(name))
        self.current_tab = self.tab_list.add_tab(name)
        self.network_names.append(name)

    def remove_network(self, name):
        print('Removing network "{}"'.format(name))
        assert name in self.network_names, 'This network does not exist!'
        self.tab_list.remove_tab(name)
        self.network_names.remove(name)
        if self.current_tab == name:
            try:
                self.current_tab = self.network_names[0]
            except AttributeError:
                self.current_tab = None

    def draw_create_network(self, surface):
        # print('Network creation step: %s' % self.create_steps[self.create_step])
        text_render = self.large_font.render('Create a new network!', True, (255, 255, 255))
        text_rect = text_render.get_rect()
        text_rect.x = int(self.display_settings['width'] / 2 - text_rect.width / 2)
        text_rect.y = int(text_rect.height + 20)
        surface.blit(text_render, text_rect)
        if self.create_steps[self.create_step] == 'select_objects':
            self.select_objects_list.draw(surface)

    def draw(self, surface):
        for x in range(len(self.net_info)):
            pygame.draw.rect(surface, self.net_color_map[x], self.net_info[x], self.net_width_map[x])
        # TODO: display info from each object in a network!
        self.tab_list.draw(surface)

    def handle_action(self, action_type, mouse_pos=None):
        if action_type == 'ESCAPE':
            print('Exiting out of everything')
            self.creating_network = False
        elif self.creating_network:
            self.select_objects_list.handle_action(action_type, mouse_pos)
        else:
            if action_type == 'LEFT_MOUSE_DOWN':
                print('Got action type: {}'.format(action_type))
                response = self.tab_list.handle_action(action_type, mouse_pos)
                if response is not None:
                    print('Changed active tab to: "{}"'.format(response))
                    self.current_tab = response
                    return True
            else:
                self.tab_list.handle_action(action_type, mouse_pos)
            return None
