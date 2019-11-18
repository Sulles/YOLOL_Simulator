"""
Created: August 3, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This class houses all the drawing components required for pygame

TODO: Add other pygame object shapes
"""

from copy import copy

from pygame import Rect as pygame_rect
from pygame import draw as pygame_draw
from pygame import font


class PygameObj:
    def __init__(self, center, width, height, color_map, shapes, text=None, Font=None):
        """
        The initializer for the main Pygame object
        :param center: list of length two: is the center of the object, using pixel coordinates
        :param width: int
        :param height: int
        :param color_map: list
        :param shapes: list of dictionaries of dictionaries, i.e.
            shapes = [{'type': 'rect', 'color': colors['WHITE'], 'settings': {'center': [0, 0], 'width': 10, 'height': 10}},
                      {'type': 'circle', 'color': None, 'settings: {'center': [20, 20], 'radius': 5}}]
        :param text: text to be shown, used for options screen, maybe object names in the future?
        :param Font: pygame.font.Font to use for creating text
        """
        if isinstance(color_map, tuple):
            color_map = [color_map]

        # Object parameters
        self.center = [int(center[0]), int(center[1])]
        self.width = int(width)
        self.height = int(height)
        self.hit_box = None
        self.update_hit_box()
        self.color_map = color_map
        self.color = color_map[0]
        self.shape_def = shapes
        self.text = text
        self.font = Font
        if text is not None:
            if self.font is None:
                self.font = font.Font('src/Cubellan.ttf', 20)
            self.text_render = self.font.render(text, True, (255, 255, 255))
            self.text_rect = self.text_render.get_rect()
            self.text_rect.center = self.center
        else:
            self.text_rect = None
            self.text_render = None

        # Define all shapes as dictionaries. Each shape 'type' has different fields, i.e. a shape type of 'circle' has
        #   radius, whereas a shape type of 'rect' has width and height
        self.drawable_shapes = []
        for shape_def in shapes:
            # print('Got new shape definition!: {}'.format(shape_def))
            if 'width' not in shape_def or shape_def['width'] is None:
                shape_def['width'] = 0

        self.update_shapes()

    def get_name(self):
        if self.text is not None:
            return copy(self.text)
        else:
            return ""

    def update_shapes(self):
        # clear all shapes
        self.drawable_shapes = []

        # re-create shapes
        for shape in self.shape_def:
            if shape['type'] == 'rect':
                self.drawable_shapes.append(
                    dict(type='rect', color=shape['color'], rect=self.create_rect(shape['settings']),
                         width=shape['width']))
            elif shape['type'] == 'circle':
                center = [self.center[0] + int(shape['settings']['center'][0] / 2),
                          self.center[1] + int(shape['settings']['center'][1] / 2)]
                self.drawable_shapes.append(
                    dict(type='circle', color=shape['color'], radius=int(shape['settings']['radius']),
                         center=center, width=shape['width']))
            elif shape['type'] == 'point_list':
                self.drawable_shapes.append(
                    dict(type='shape', color=shape['color'],
                         point_list=self.convert_point_list_to_abs(shape['point_list']),
                         width=shape['width']))

    def convert_point_list_to_abs(self, point_list):
        for point in point_list:
            point[0] += self.center[0]
            point[1] += self.center[1]
        return point_list

    def _update_color(self, map_index):
        self.color = self.color_map[map_index]
        # print('Current color: {}'.format(self.color))

    update_color = _update_color

    def _draw(self, surface):
        for shape in self.drawable_shapes:
            # print('shape width: {} type: {}'.format(shape['width'], type(shape['width'])))
            # Get variable colors
            if shape['color'] is None:
                color = self.color
            else:
                color = shape['color']

            # Don't draw shape if color is None
            if color is not None:
                if shape['type'] == 'rect':
                    pygame_draw.rect(surface, color, shape['rect'], shape['width'])
                elif shape['type'] == 'circle':
                    pygame_draw.circle(surface, color, shape['center'], shape['radius'], shape['width'])
                elif shape['type'] == 'shape':
                    pygame_draw.polygon(surface, color, shape['point_list'], shape['width'])
        if self.text_render is not None:
            surface.blit(self.text_render, self.text_rect)

    draw = _draw

    def update_text(self, text=None, font=None, text_to_width_factor=None):
        assert self.text is not None or text is not None, \
            'Cannot show text with no text passed as argument and no text in object!'
        assert self.font is not None or font is not None, \
            'Cannot create text with no font passed as argument and no font in object!'
        if text is not None:
            self.text = text
        if font is not None:
            self.font = font
            self.text_render = font.render(text, True, (255, 255, 255))
        else:
            self.text_render = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.center
        if text_to_width_factor is not None:
            expected_width = int(text_to_width_factor * len(self.text) + 30)
            width_diff = expected_width - copy(self.width)
            self.widen(width_diff)
            self.update_shapes()

    def widen(self, additional_width):
        print('Widening "{}" all shapes by: {}'.format(self.text, additional_width))
        self.width += additional_width
        for shape in self.shape_def:
            shape['settings']['width'] += additional_width

    def shift_center(self, center_offset):
        new_center = [self.center[0] + center_offset[0], self.center[1], + center_offset[1]]
        self.set_center(new_center)
        print('New object center: {}'.format(self.center))

    def set_center(self, new_center):
        print('{} current center: {}, new center: {}'.format(self.text, self.center, new_center))
        self.center = [new_center[0], new_center[1]]
        self.update_shapes()
        self.update_hit_box()
        if self.text_rect is not None:
            self.text_rect.center = self.center
            try:
                self.update_text()
            except AssertionError:
                pass

    def update_hit_box(self):
        self.hit_box = [[self.center[0] - int(self.width / 2), self.center[0] + int(self.width / 2)],
                        [self.center[1] - int(self.height / 2), self.center[1] + int(self.height / 2)]]

    def in_hit_box(self, pos):
        if pos[0] in range(self.hit_box[0][0], self.hit_box[0][1]) and \
                pos[1] in range(self.hit_box[1][0], self.hit_box[1][1]):
            return True
        else:
            return False

    def create_rect(self, rect_settings):
        """
        This function creates the pygame.Rect object for a rectangle
        :param rect_settings: dictionary
            Required fields:
                - center
                - width
                - height
            Optional fields:
                - border
        :return: returns dictionary (rect=pygame.Rect object, width=border width)
        """
        top_left = [self.center[0] + rect_settings['center'][0] - int(rect_settings['width'] / 2),
                    self.center[1] + rect_settings['center'][1] - int(rect_settings['height'] / 2)]
        return pygame_rect(top_left[0], top_left[1],
                           rect_settings['width'], rect_settings['height'])
