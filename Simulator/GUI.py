"""
Created: August 3, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This class houses the GUI
"""
# noinspection PyUnresolvedReferences
from src.constants import colors
# noinspection PyUnresolvedReferences
from Classes.pygame_obj import PygameObj
# noinspection PyUnresolvedReferences
from Classes.map import obj_map
# noinspection PyUnresolvedReferences
from OptionScreen import ListObj
import pygame.font
import pygame.draw
from pygame import Rect


class ExtendedListObj:
    def __init__(self, list_of_entry_names, screen_size, width=300, height=50, x_offset=0, y_offset=0):
        self.entry_names = list_of_entry_names
        self.screen_size = screen_size
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.main_list = ListObj(list_of_entry_names, screen_size, width=width, height=height, x_offset=x_offset, y_offset=y_offset)
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


class TabList:
    def __init__(self, tab_names, display_settings):
        self.display_settings = display_settings
        # TODO: Do this next! ===========================================


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
        self.network_names = []
        self.tabs = []

        # SETTING UP NETWORK SPECIFIC INFO
        self.position = [10, 10]
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
        self.network_names.append(name)
        # def __init__(self, center, width, height, color_map, shapes, text=None, Font=None):
        top_left = [int(200 + 240 * len(self.network_names)), 80]
        top_right = [int(top_left[0] + 200), 80]
        bottom_right = [int(top_right[0] - 20), 120]
        bottom_left = [int(bottom_right[0] - 160), 120]
        center = [int(200 + 120*len(self.network_names)),
                  int(80)]
        # def __init__(self, center, width, height, color_map, shapes, text=None, Font=None):
        self.tabs.append(PygameObj(self.center, 500, 500, [(100, 100, 100), (200, 200, 200)], [
            {'type': 'point_list',
             'color': None,
             'center': center,
             'point_list': [top_left, top_right, bottom_right, bottom_left]}]))

    def remove_network(self, name):
        print('Removing network "{}"'.format(name))
        assert name in self.network_names, 'This network does not exist!'
        index = self.network_names.index(name)
        self.tabs.remove(index)
        self.network_names.remove(name)


    def verify_create_objects_bounds(self):
        for key, item in self.create_how_many_objects.items():
            if item < 0:
                self.create_how_many_objects[key] = 0
                self.how_many_objects.update_text(list([str(_) for _ in self.create_how_many_objects.values()]))

    def draw_create_network(self, surface):
        # print('Network creation step: %s' % self.create_steps[self.create_step])
        text_render = self.large_font.render('Create a new network!', True, (255, 255, 255))
        text_rect = text_render.get_rect()
        text_rect.x = int(self.display_settings['width']/2 - text_rect.width/2)
        text_rect.y = int(text_rect.height + 20)
        surface.blit(text_render, text_rect)
        if self.create_steps[self.create_step] == 'select_objects':
            self.select_objects_list.draw(surface)

    def draw(self, surface, network=None):
        for x in range(len(self.net_info)):
            pygame.draw.rect(surface, self.net_color_map[x], self.net_info[x], self.net_width_map[x])
        # for obj in network.get_objects():
        #     # Display all objects here
        #     pass
        for tab in self.tabs:
            print('Drawing tab?')
            tab.draw(surface)

    def handle_action(self, action_type, mouse_pos=None):
        if action_type == 'ESCAPE':
            print('Exiting out of everything')
            self.creating_network = False
        else:
            self.select_objects_list.handle_action(action_type, mouse_pos)
