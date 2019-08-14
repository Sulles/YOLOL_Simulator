"""
Created August 13, 2019

Author: StolenLight

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

import pygame
from .Classes.pygame_obj import PygameObj


class ListObj(PygameObj):
    def __init__(self, list_of_entries):
        self.shapes = []

        top_of_list = 70 * len(list_of_entries) / 2

        for x in range(len(list_of_entries)):
            print('Generating %s entry' % list_of_entries[x])
            self.shapes.append({
                {'type': 'rect',
                 'color': [255, 255, 255],
                 'width': 2,
                 'settings': {
                     'center': [0, top_of_list - 70 * x],
                     'width': 200,
                     'height': 50
                 }},
                {'type': 'rect',
                 'color': None,
                 'settings': {
                     'center': [0, top_of_list - 70 * x],
                     'width': 180,
                     'height': 40
                 }}
            })

        PygameObj.__init__(self, [0, 0], 200, 50, [(0, 0, 0), (100, 100, 100), (0, 200, 0)], self.shapes)

    def draw(self, surface):
        self._draw(surface)
        # TODO: blit text to surface
        return


class OptionScreen(PygameObj):
    def __init__(self, screen_width, screen_height):
        self.background = [{
            'type': 'rect',
            'color': None,
            'settings': {
                'center': [0, 0],
                'width': screen_width,
                'height': screen_height
            }
        }]

        # Simple dictionary of all settings, with key as first layer text, and value as sub-layer text
        self.options_text = {
            'Edit networks': ['Add/remove objects from a network', 'Create a new network',
                              'Modify an existing network', 'Delete a network'],
            'Edit YOLOL code': None,
            'Edit simulator settings': ['Change screen size', 'Change FPS']
        }

        self.main_list = ListObj([_ for _ in self.options_text.keys()])
        self.network_list = ListObj(self.options_text['Edit networks'])
        self.yolol_list = ListObj(self.options_text['Edit YOLOL code'])
        self.simulator_list = ListObj(self.options_text['Edit simulator settings'])

        self.selected_key = None

        self.current_list = []
        self.update_current_list()

        PygameObj.__init__(self, [0, 0], screen_width, screen_height, [(0, 0, 0)], self.background)

    def update_current_list(self):
        if self.selected_key is None:
            self.current_list = self.main_list
        elif self.selected_key == 'Edit networks':
            self.current_list = self.network_list
        elif self.selected_key == 'Edit YOLOL code':
            self.current_list = self.yolol_list
        elif self.selected_key == 'Edit simulator settings':
            self.current_list = self.simulator_list
        else:
            print('what even is the selected key?: {}'.format(self.selected_key))
            raise AttributeError

    def get_obj_from_hitbox(self, pos):
        for obj in self.current_list:


    def draw(self, surface):
        self._draw(surface)
        for list_obj in self.current_list:
            list_obj.draw(surface)

    def handle_action(self, action_type, mouse_pos=None):
        if action_type == 'ESCAPE':
            self.selected_key = None
        elif action_type == 'MOUSE_HOVER':
            # Find which list object mouse is hovering over
            highlight_obj = get_obj_from_hitbox(mouse_pos)
            self._update_color(1)
        elif action_type == 'MOUSE_DOWN':
            # Find which list object mouse is hovering over
            self._update_color(2)
            # Update selected key to represent where mouse click occurred
            # self.selected_key =
        else:
            print('Unsupported action detected! Got: {}'.format(action_type))
            raise AttributeError
