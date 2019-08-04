"""
Created: August 3, 2019
Last Updated: August 3, 2019

Author: StolenLight

=== DESCRIPTION ===
This class houses all the drawing components required for pygame
"""

from pygame import Rect as pygame_rect
from pygame import draw as pygame_draw


class PygameObj:
    def __init__(self, position, width, height, color_map, shapes):
        """
        The initializer for the main Pygame object
        :param position: list of length two: is the top left position of the object, using pixel coordinates
        :param width: int
        :param height: int
        :param color_map: list
        :param shapes: list of dictionaries of dictionaries, i.e.
            shapes = [{'type': 'rect', 'color': colors['WHITE'], 'settings': {'position': [0, 0], 'width': 10, 'height': 10}},
                      {'type': 'circle', 'color': None, 'settings: {'position': [20, 20], 'radius': 5}}]
        """
        if isinstance(color_map, tuple):
            color_map = [color_map]

        # Drawing parameters
        self.position = [int(position[0]), int(position[1])]
        self.width = int(width)
        self.height = int(height)
        self.hit_box = [[self.position[0], self.position[0] + self.width],
                        [self.position[1], self.position[1] + self.height]]
        self.color_map = color_map
        self.color = color_map[0]

        self.drawable_shapes = []
        for shape_def in shapes:
            print('Got new shape definition!')

            if 'width' not in shape_def or shape_def['width'] is None:
                shape_def['width'] = 0
            if 'border' not in shape_def or shape_def['border'] is None:
                shape_def['border'] = 0

            if shape_def['type'].lower() == 'rect':
                self.drawable_shapes.append(
                    dict(type='rect', color=shape_def['color'], rect=self.create_rect(shape_def['settings']),
                         width=shape_def['width']))
            elif shape_def['type'].lower() == 'circle':
                self.drawable_shapes.append(
                    dict(type='circle', color=shape_def['color'], radius=int(shape_def['settings']['radius']),
                         position=[int(_) for _ in shape_def['settings']['position']], width=shape_def['width']))

    def _update_color(self, map_index):
        self.color = self.color_map[map_index]
        print('Current color: {}'.format(self.color))

    def _draw(self, surface):
        for shape in self.drawable_shapes:
            # print('shape width: {} type: {}'.format(shape['width'], type(shape['width'])))
            if shape['color'] is None:
                color = self.color
            else:
                color = shape['color']

            if shape['type'] == 'rect':
                pygame_draw.rect(surface, color, shape['rect'], shape['width'])
            elif shape['type'] == 'circle':
                pygame_draw.circle(surface, color, shape['position'], shape['radius'], shape['width'])

    @staticmethod
    def create_rect(rect_settings):
        """
        This function creates the pygame.Rect object for a rectangle
        :param rect_settings: dictionary
            Required fields:
                - position
                - width
                - height
            Optional fields:
                - border
        :return: returns dictionary (rect=pygame.Rect object, width=border width)
        """
        return pygame_rect(rect_settings['position'][0], rect_settings['position'][1],
                           rect_settings['width'], rect_settings['height'])
