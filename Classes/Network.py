"""
Created: July 13, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This class hosts all the objects within a network
"""

from .map import *


class Network():
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
        self.objects = []
        for obj in obj_settings.keys():
            self.objects.append(obj_map[obj](obj_settings[obj]))

    def _print(self):
        print("=== NETWORK INFORMATION ===\n"
              "Name: {0}\n"
              "Objects: {1}".format(self.name, [obj.name for obj in self.objects]))

        for obj in self.objects:
            obj._print()


# Unit test
if __name__ == "__main__":
    print("Running unit test for Network class...")
    Net = Network("Button_Light", {"Button": {'name': 'butt_name', "state": 2},
                                   "Lamp": {'name': 'lamp_name', "on": True}})
    Net._print()
