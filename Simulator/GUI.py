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


class GUI:
    def __init__(self, display_settings):
        self.display_settings = display_settings

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
        self.possible_objects = ListObj(list(obj_map.keys()), display_settings)
        self.option_obj_map = dict(select_objects=self.possible_objects)
        # TODO: add something for modify_attributes and instantiate_network to option_obj_map
        self.current_list_obj = None

    def add_network(self, name, network):
        self.network_names.append(name)
        # def __init__(self, center, width, height, color_map, shapes, text=None, Font=None):
        top_left = [int(200 + 240 * len(self.network_names)), 80]
        top_right = [int(top_left[0] + 200), 80]
        bottom_right = [int(top_right[0] - 20), 120]
        bottom_left = [int(bottom_right[0] - 160), 120]
        center = [int(200 + 120*len(self.network_names)),
                  int(80)]
        # def __init__(self, center, width, height, color_map, shapes, text=None, Font=None):
        self.tabs.append(PygameObj(center, 500, 500, [(100, 100, 100), (200, 200, 200)], [
            {'type': 'point_list',
             'color': None,
             'center': center,
             'point_list': [top_left, top_right, bottom_right, bottom_left]}]))

    def create_network(self):
        self.creating_network = True

    def draw_create_network(self, surface):
        print('Network creation step: %s' % self.create_steps[self.create_step])
        if self.create_steps[self.create_step] == 'select_objects':
            self.possible_objects.draw(surface)

    def draw(self, surface, network=None):
        for x in range(len(self.net_info)):
            pygame.draw.rect(surface, self.net_color_map[x], self.net_info[x], self.net_width_map[x])
        # for obj in network.get_objects():
        #     # Display all objects here
        #     pass
        for tab in self.tabs:
            tab.draw(surface)

    def handle_action(self, action_type, mouse_pos=None):
        if action_type == 'ESCAPE':
            self.creating_network = False
        elif action_type == 'MOUSE_HOVER':
            self.current_list_obj.handle_hover(mouse_pos)
        elif action_type == 'MOUSE_DOWN':
            self.selected_key = self.current_list_obj.handle_mouse_down(mouse_pos)
            return self.update_current_list()
        else:
            print('Unsupported action detected! Got: {}'.format(action_type))
            raise AttributeError
