"""
Created: July 13, 2019
Last Updated: August 3, 2019

Author: StolenLight

=== DESCRIPTION ===
This class hosts all the objects within a network
"""

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
        for ob_set in obj_settings.keys():
            self.objects.append(obj_map[ob_set](obj_settings[ob_set]))

        for obj in self.objects:
            print('Created new object: %s with hitbox: %s' % (obj.name, obj.hit_box))

    def print(self):
        print("=== NETWORK INFORMATION ===\n"
              "Name: {0}\n"
              "Objects: {1}".format(self.name, [obj.name for obj in self.objects]))

        for obj in self.objects:
            obj.print()

    def handle_action(self, action_location, action_type=None):
        """
        This is the main function that will handle user actions done through pygame
        :param action_location: A list of x, y coords where user action occurred
        :param action_type: The type of action that the user requested
        """
        for obj in self.objects:
            if action_location[0] in range(obj.hit_box[0][0], obj.hit_box[0][1]) and \
                    action_location[1] in range(obj.hit_box[1][0], obj.hit_box[1][1]):
                obj.handle_action(action_type)

    def draw(self, surface):
        """
        This function is called to handle drawing all devices
        :param surface: Pygame Surface to draw everything on
        """
        for obj in self.objects:
            obj.draw(surface)

    def get_objects(self):
        return [_ for _ in self.objects]


# Unit test
if __name__ == "__main__":
    print("Running unit test for Network class...")
    Net = Network("Button_Light", {"Button": {'name': 'butt_name', "state": 2},
                                   "Lamp": {'name': 'lamp_name', "on": True}})
    Net.print()
