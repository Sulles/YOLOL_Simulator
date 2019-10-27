import os
import sys

import pygame
# noinspection PyUnresolvedReferences
from Classes.Network import Network
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

            # MOUSE BUTTON DOWN
            elif event.type == MOUSEBUTTONDOWN:
                # RIGHT CLICK
                if event.button == 3:
                    response = GUI.handle_action('RIGHT_MOUSE_DOWN', event.pos)
                # LEFT CLICK
                elif event.button == 1:
                    response = GUI.handle_action('LEFT_MOUSE_DOWN', event.pos)

            # MOUSE BUTTON UP
            elif event.type == MOUSEBUTTONUP:
                # RIGHT CLICK
                if event.button == 3:
                    response = GUI.handle_action('RIGHT_MOUSE_UP', event.pos)
                # LEFT CLICK
                if event.button == 1:
                    response = GUI.handle_action('LEFT_MOUSE_UP', event.pos)

            # HANDLE RESPONSES
            if response is not None:
                print('Got action response: {}'.format(response))
                if response['type'] == 'terminate':
                    terminate()

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
