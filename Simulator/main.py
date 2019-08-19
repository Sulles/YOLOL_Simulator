"""
Created: July 14, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This is the main simulator code. From here, users can

TODO: Make shift + right click = plane move?
"""

import pygame
import sys
import os
from pygame.locals import *
# from time import time
# from pprint import pprint

# noinspection PyUnresolvedReferences
from src.constants import colors
# noinspection PyUnresolvedReferences
from GUI import GUI
# noinspection PyUnresolvedReferences
from Classes.Network import Network
# noinspection PyUnresolvedReferences
from OptionScreen import OptionScreen


def simulator():
    pygame.init()
    global DISPLAY
    DISPLAY = dict(width=800, height=500)
    FPS_CLOCK = pygame.time.Clock()
    FPS = 60
    # START_TIME = time()

    surface = pygame.display.set_mode((DISPLAY['width'], DISPLAY['height']))
    pygame.display.set_caption('Proving Ground')
    gui = GUI(DISPLAY)
    option_screen = OptionScreen(DISPLAY)

    # Initialize Network here
    selected_network = 0
    all_networks = []
    network_settings = {'Lamp':
                            {'name': 'lamp_name',
                             'state': 1,
                             'center': [DISPLAY['width'] - 100, DISPLAY['height'] / 2]},
                        'Button0':
                            {'name': 'butt_name',
                             'state': 0,
                             'center': [DISPLAY['width'] / 2, DISPLAY['height'] / 2],
                             'color_map': [colors['RED'], colors['GREEN']]}
                        }
    all_networks.append(Network('test_network', network_settings))
    gui.add_network('test network', all_networks[0])

    print("Initialization complete, running playground...")

    selected_obj = None

    # MAIN LOOP
    while True:
        for event in pygame.event.get():
            # EXIT CONDITION
            if event.type == QUIT:
                terminate()

            # KEY INPUT CONDITION
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # Show main screen
                    option_screen.handle_action('ESCAPE')

            # MOUSE BUTTON DOWN
            elif event.type == MOUSEBUTTONDOWN:
                # RIGHT CLICK
                if event.button == 3:
                    print('Right click found: {}'.format(event.pos))
                    if not option_screen.is_active:
                        selected_obj = all_networks[selected_network].get_closest_obj(event.pos)
                        print('Got closest obj with name: "%s"' % selected_obj.name)
                # LEFT CLICK
                elif event.button == 1:
                    if option_screen.is_active:
                        response = option_screen.handle_action('MOUSE_DOWN', event.pos)
                        if response is not None:
                            if response['type'] == 'terminate':
                                terminate()
                            elif response['type'] == 'add network':
                                # TODO Handle passing new network information from OptionScreen to all_networks here!
                                #  Maybe to the instantiation of the network in main as well?
                                # all_networks.append(create_new_network())
                                option_screen.show_incomplete_feature()
                            else:
                                option_screen.show_incomplete_feature()
                    else:
                        print('Left click found: {}'.format(event.pos))
                        for network in all_networks:
                            network.handle_action(event.pos, action_type='LEFT_MOUSE_DOWN')

            # MOUSE BUTTON UP
            elif event.type == MOUSEBUTTONUP:
                # RIGHT CLICK
                if event.button == 3:
                    if not option_screen.is_active:
                        print('Right mouse up found?')
                        selected_obj = None
                # LEFT CLICK
                if event.button == 1:
                    if not option_screen.is_active:
                        all_networks[selected_network].handle_action(event.pos, action_type='LEFT_MOUSE_UP')

        if selected_obj:
            selected_obj.set_center(pygame.mouse.get_pos())

        # Perform tick update here for YOLOL chips

        # Re-draw background
        surface.fill(colors['BGCOLOR'])

        # Drawing objects
        if option_screen.is_active:
            option_screen.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
            option_screen.draw(surface)
        else:
            for network in all_networks:
                network.draw(surface)
            gui.draw(surface)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


''' RUN MAIN FUNCTION '''
if __name__ == "__main__":
    simulator()
