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
from Classes.pygame_obj import PygameObj
from math import sqrt


class ListObj:
    def __init__(self, list_of_entries, screen_size):
        if list_of_entries is None or len(list_of_entries) == 0:
            print('Found no entries! Skipping...')
            return

        self.entries = list_of_entries
        self.objects = []
        self.closest_object = 0

        # print('Instantiating new List Object. List of entries: {}'.format(
        #     list_of_entries))

        top_of_list = int(70 * len(list_of_entries))

        for x in range(0, len(list_of_entries)):
            # print('Creating shape for list entry "%s"' % list_of_entries[x])
            shapes = []
            shapes.append(
                {'type': 'rect',
                 'color': (255, 255, 255),
                 'width': 2,
                 'settings': {
                     'center': [0, 0],
                     'width': 200,
                     'height': 50}})
            shapes.append(
                {'type': 'rect',
                 'color': None,
                 'settings': {
                     'center': [0, 0],
                     'width': 180,
                     'height': 40}})
            # TODO: Blit text here?

            self.objects.append(
                PygameObj([int(screen_size['width'] / 2) + 100,
                    int(screen_size['height'] / 2 - (top_of_list / 20) - (70 * x))],
                    200, 50, [(0, 0, 0), (100, 100, 100), (0, 200, 0)], shapes))
        print('List objects: {}'.format(self.objects))

    def draw(self, surface):
        for obj in self.objects:
            obj._draw(surface)
        # TODO: blit text to surface here?

    def handle_hover(self, mouse_pos):
        # print('got mouse pos: {}'.format(mouse_pos))
        distance = []
        obj_index = []
        for obj in self.objects:
            # print('Got obj with center: "%s"' % obj.center)
            distance.append(self.distance(obj.center, mouse_pos))
            obj_index.append(self.objects.index(obj))
        # print('distance: {}'.format(distance))
        # print('min distance: {}'.format(min(distance)))
        # print(self.objects[obj_index[distance.index(min(distance))]])
        closest_object = obj_index[distance.index(min(distance))]
        if self.closest_object != closest_object:
            self.objects[self.closest_object]._update_color(0)
            self.closest_object = closest_object
            self.objects[self.closest_object]._update_color(1)

    @staticmethod
    def distance(a, b):
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def handle_mouse_down(self, mouse_pos):
        if self.objects[self.closest_object].in_hit_box(mouse_pos):
            print('Got left click in "%s"' % self.entries[self.closest_object])
            # TODO: change level and options display here


class OptionScreen:
    def __init__(self, screen_size):
        self.is_active = True

        # Simple dictionary of all settings, with key as first layer text, and value as sub-layer text
        self.options_text = {
            'Edit networks': ['Add/remove objects from a network', 'Create a new network',
                              'Modify an existing network', 'Delete a network'],
            'Edit YOLOL code': None,
            'Edit simulator settings': ['Change screen size', 'Change FPS']
        }

        self.main_list = ListObj([_ for _ in self.options_text.keys()], screen_size)
        self.network_list = ListObj(self.options_text['Edit networks'], screen_size)
        self.yolol_list = ListObj(self.options_text['Edit YOLOL code'], screen_size)
        self.simulator_list = ListObj(self.options_text['Edit simulator settings'], screen_size)

        self.selected_key = None

        self.current_list = []
        self.update_current_list()

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

    def toggle_activate(self):
        if self.is_active:
            self.deactivate()
        else:
            self.activate()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def draw(self, surface):
        self.current_list.draw(surface)

    def handle_action(self, action_type, mouse_pos=None):
        if action_type == 'ESCAPE' and self.selected_key is not None:
            self.selected_key = None
        elif action_type == 'ESCAPE':
            self.toggle_activate()
        elif action_type == 'MOUSE_HOVER':
            self.current_list.handle_hover(mouse_pos)
        elif action_type == 'MOUSE_DOWN':
            # Find which list object mouse is hovering over
            print(self.current_list.handle_mouse_down(mouse_pos))
            # Update selected key to represent where mouse click occurred
            # self.selected_key =
        else:
            print('Unsupported action detected! Got: {}'.format(action_type))
            raise AttributeError
