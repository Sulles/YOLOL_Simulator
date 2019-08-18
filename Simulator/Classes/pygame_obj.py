"""
Created: August 3, 2019
Last Updated: August 3, 2019

Author: StolenLight

=== DESCRIPTION ===
This class houses all the drawing components required for pygame

TODO: Add other pygame object shapes
"""

# from copy import deepcopy
from pygame import Rect as pygame_rect
from pygame import draw as pygame_draw


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
        self.center = [int(center[0] - width / 2), int(center[1] - height / 2)]
        self.width = int(width)
        self.height = int(height)
        self.hit_box = None
        self.update_hit_box()
        self.color_map = color_map
        self.color = color_map[0]
        self.shape_def = shapes
        self.text = text
        self.font = Font
        if text is not None and Font is not None:
            self.text_render = Font.render(text, True, (255, 255, 255))
            self.text_rect = self.text_render.get_rect()
            self.text_rect.center = self.center
        else:
            self.text_render = None

        self.drawable_shapes = []
        for shape_def in shapes:
            # print('Got new shape definition!: {}'.format(shape_def))

            if 'width' not in shape_def or shape_def['width'] is None:
                shape_def['width'] = 0
            if 'border' not in shape_def or shape_def['border'] is None:
                shape_def['border'] = 0

        self.update_shapes()

    def update_shapes(self):
        # clear all shapes
        self.drawable_shapes = []

        # re-create shapes
        for shape in self.shape_def:
            if shape['type'].lower() == 'rect':
                self.drawable_shapes.append(
                    dict(type='rect', color=shape['color'], rect=self.create_rect(shape['settings']),
                         width=shape['width']))
            elif shape['type'].lower() == 'circle':
                center = [self.center[0] + int(shape['settings']['center'][0] / 2),
                          self.center[1] + int(shape['settings']['center'][1] / 2)]
                self.drawable_shapes.append(
                    dict(type='circle', color=shape['color'], radius=int(shape['settings']['radius']),
                         center=center, width=shape['width']))

    def _update_color(self, map_index):
        self.color = self.color_map[map_index]
        # print('Current color: {}'.format(self.color))

    update_color = _update_color

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
                pygame_draw.circle(surface, color, shape['center'], shape['radius'], shape['width'])
        if self.text_render is not None:
            surface.blit(self.text_render, self.text_rect)

    draw = _draw

    def update_text(self, text=None, font=None):
        assert self.text is not None and text is not None, \
            'Cannot show text with no text passed as argument and no text in object!'
        assert self.font is not None and font is not None, \
            'Cannot create text with no font passed as argument and no font in object!'
        if text is not None:
            self.text = text
        if font is not None:
            self.text_render = font.render(text, True, (255, 255, 255))
        else:
            self.text_render = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_render.get_rect()
        self.text_rect.center = self.center

    def set_center(self, new_center):
        self.center = [new_center[0], new_center[1]]
        self.update_shapes()
        self.update_hit_box()

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
