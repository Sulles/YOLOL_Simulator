"""
Created November 1, 2019

Author: Sulles

=== DESCRIPTION ===
This is the main function where pygame is called and handles all user input

TODO: Make shift + right click = plane move?
"""


import os
import sys

import pygame
# noinspection PyUnresolvedReferences
from Classes.Network import Network
# noinspection PyUnresolvedReferences
from Classes.pygame_obj import PygameObj
# noinspection PyUnresolvedReferences
from GUI2 import GUI2
# noinspection PyUnresolvedReferences
from OptionScreen import OptionScreen
from pygame.locals import *
# noinspection PyUnresolvedReferences
from src.constants import colors

# from time import time
# from pprint import pprint

sys.path.append('Classes')
os.path.join('Classes')


def simulator():
    pygame.init()

    # OBJECTS AND VARIABLES
    DISPLAY = dict(width=800, height=500)
    FPS_CLOCK = pygame.time.Clock()
    FPS = 60
    GUI = GUI2(DISPLAY)

    # PYGAME SETUP
    surface = pygame.display.set_mode((DISPLAY['width'], DISPLAY['height']))
    pygame.display.set_caption('GUI REVAMPER')

    # SIMULATOR SETUP
    # Create Test Network 1
    network_settings = {'Lamp':
                            {'name': 'lamp_1',
                             'state': 1,
                             'center': [DISPLAY['width'] / 2 - 80, DISPLAY['height'] / 2]},
                        'Button0':
                            {'name': 'button_1',
                             'state': 0,
                             'center': [DISPLAY['width'] / 2 - 100, DISPLAY['height'] / 2 + 50],
                             'color_map': [colors['RED'], colors['GREEN']]},
                        'Chip':
                            {'name': 'test_chip',
                             'state': 0,
                             'center': [DISPLAY['width'] / 2 - 120, DISPLAY['height'] / 2 + 100]}
                        }
    GUI.add_network(Network('test_network_1', network_settings))

    # # Create Test Network 2
    # network_settings = {'Lamp':
    #                         {'name': 'lamp_2',
    #                          'state': 1,
    #                          'center': [DISPLAY['width'] / 2 + 80, DISPLAY['height'] / 2]},
    #                     'Button0':
    #                         {'name': 'button_2',
    #                          'state': 0,
    #                          'center': [DISPLAY['width'] / 2 + 100, DISPLAY['height'] / 2 + 50],
    #                          'color_map': [colors['RED'], colors['GREEN']]},
    #                     'Chip':
    #                         {'name': 'test_chip',
    #                          'state': 0,
    #                          'center': [DISPLAY['width'] / 2 + 120, DISPLAY['height'] / 2 + 100]}
    #                     }
    # GUI.add_network(Network('test_network_2', network_settings))

    # Moving selected objects around
    selected_obj = None

    # MAIN LOOP
    while True:

        # EVENT HANDLING
        for event in pygame.event.get():
            response = None

            # EXIT CONDITION
            if event.type == QUIT:
                terminate()

            # KEY INPUT CONDITION
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    GUI.handle_action('ESCAPE')
                else:
                    print('Got key input: {}'.format(event.key))
                    GUI.handle_action('KEY_DOWN', None, event.key)

            # MOUSE BUTTON DOWN
            elif event.type == MOUSEBUTTONDOWN:
                # RIGHT CLICK
                if event.button == 3:
                    print('Got RIGHT mouse DOWN')
                    response = GUI.handle_action('RIGHT_MOUSE_DOWN', event.pos)
                    print('Got closest obj with name: {}'.format(response))
                # LEFT CLICK
                elif event.button == 1:
                    print('Got LEFT mouse DOWN')
                    response = GUI.handle_action('LEFT_MOUSE_DOWN', event.pos)

            # MOUSE BUTTON UP
            elif event.type == MOUSEBUTTONUP:
                # RIGHT CLICK
                if event.button == 3:
                    print('Got RIGHT mouse UP')
                    response = dict(type='deselect')
                # LEFT CLICK
                if event.button == 1:
                    print('Got LEFT mouse UP')
                    response = GUI.handle_action('LEFT_MOUSE_UP', event.pos)

            # HANDLE RESPONSES
            if type(response) is dict:
                print('Got action response: {}'.format(response))
                if 'type' in response.keys():
                    if response['type'] == 'terminate':
                        terminate()
                    elif response['type'] == 'new_selection':
                        print('Got new selection...')
                        selected_obj = response['object']
                    elif response['type'] == 'deselect':
                        print('Deselecting current object...')
                        selected_obj = None
            elif response is not None:
                print('Got unknown response: {}'.format(response))

        # Follow mouse
        if isinstance(selected_obj, PygameObj):
            selected_obj.set_center(pygame.mouse.get_pos())

        # DRAWING
        # Re-draw background
        surface.fill(colors['BGCOLOR'])

        # GUI handling
        GUI.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
        GUI.step()
        GUI.draw(surface)

        # PYGAME SETTINGS
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


''' RUN MAIN FUNCTION '''
if __name__ == "__main__":
    simulator()
