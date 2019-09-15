"""
Created: July 13, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This class hosts all the objects within a network
"""

from copy import copy
from math import sqrt
from time import time
from .map import *


class Network:
    def __init__(self, name, obj_settings):
        """
        :param name: name of the network
        :param obj_settings: a dictionary of objects and their properties, also
            as dictionaries
        Example obj_settings dictionary:
            {"Button": {"name": 'butt_name', "state": 0}}
        This would create a Button with name 'butt_name' and ButtonState 0
        """
        self.name = name
        self.update_flag = False
        self.objects = []
        self.last_step_time = time()

        for obj_set in obj_settings.keys():
            self.objects.append(obj_map[obj_set](obj_settings[obj_set]))

        for obj in self.objects:
            print('Created new object: "%s" with hitbox: %s' % (obj.name, obj.hit_box))

    def print(self):
        print("=== NETWORK INFORMATION ===\n"
              "Name: {0}\n"
              "Objects: {1}".format(self.name, [obj.name for obj in self.objects]))

        for obj in self.objects:
            obj.print()

    def handle_action(self, action_type, action_location):
        """
        This is the main function that will handle user actions done through pygame
        :param action_location: A list of x, y coords where user action occurred
        :param action_type: The type of action that the user requested
        """
        response = None
        for obj in self.objects:
            if action_location[0] in range(obj.hit_box[0][0], obj.hit_box[0][1]) and \
                    action_location[1] in range(obj.hit_box[1][0], obj.hit_box[1][1]):
                response = obj.handle_action(action_type)
        if response is not None:
            # print('Got response from action: {}'.format(response))
            parsed_response = dict()
            for key, item in response.items():
                parsed_response[str('GLOBAL_' + key)] = item
            for obj in self.objects:
                if isinstance(obj, Chip):
                    # print('Updating chip "{0}" with data: {1}'.format(obj.name, parsed_response))
                    obj.update_kwargs(parsed_response)

    def get_closest_obj(self, action_location):
        distance = []
        obj_index = []
        for obj in self.objects:
            print('Got obj: "%s" with center: "%s"' % (obj.name, obj.center))
            distance.append(self.distance(obj.center, action_location))
            obj_index.append(self.objects.index(obj))
        return self.objects[obj_index[distance.index(min(distance))]]

    @staticmethod
    def distance(a, b):
        return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def draw(self, surface):
        """
        This function is called to handle drawing all devices
        :param surface: Pygame Surface to draw everything on
        """
        for obj in self.objects:
            obj.draw(surface)

    def get_objects(self):
        return [copy(_) for _ in self.objects]

    def step(self):
        """
        This function is for handling chip steps if a chip is in a network
        """
        attr_updates = None
        ms_time_dif = int(1000 * (time() - self.last_step_time))
        if ms_time_dif > 200:
            self.last_step_time = time()
            for obj in self.objects:
                if isinstance(obj, Chip):
                    attr_updates = obj.step()

        if attr_updates is not None:
            for key, value in attr_updates.items():
                if 'GLOBAL' in key:
                    attr_name = key[7:]
                    # print('finding object with attribute: "%s"' % attr_name)
                    for obj in self.objects:
                        if attr_name in obj.get_attributes():
                            # print('Updating "{0}" attribute "{1}" to value: {2}'.format(obj.name, attr_name, value))
                            obj.modify_attr(attr_name, value)
