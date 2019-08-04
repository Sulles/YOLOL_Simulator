"""
Created: August 3, 2019
Last Updated: August 3, 2019

Author: StolenLight

=== DESCRIPTION ===
This class houses all the drawing components required for pygame
"""

from pygame import Rect


class PygameObj:
    def __init__(self, position, width, height, color_map):
        if isinstance(color_map, tuple):
            color_map = [color_map]

        # Drawing parameters
        self.position = position
        self.width = width
        self.height = height
        self.color_map = color_map
        self.color = color_map[0]
        self.rect = Rect(self.position[0], self.position[1],
                         self.width, self.height)
