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

sys.path.append('Classes')
os.path.join('Classes')


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
                             'color_map': [colors['RED'], colors['GREEN']]},
                        'Chip':
                            {'name': 'test_chip',
                             'center': [200, 200]}
                        }
    all_networks.append(Network('test_network', network_settings))
    # TODO: add another network to gui and verify network tabs work as expected
    gui.add_network('test network', [network for network in all_networks])

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
                    print('Got escape!')
                    if gui.creating_network:
                        print('currently creating a network')
                        gui.handle_action('ESCAPE')
                    else:
                        print('option screen is handling escape now')
                        option_screen.handle_action('ESCAPE')
                        # option_screen.print()

            # MOUSE BUTTON DOWN
            elif event.type == MOUSEBUTTONDOWN:
                # RIGHT CLICK
                if event.button == 3:
                    # print('Right click found: {}'.format(event.pos))
                    if option_screen.is_active:
                        if gui.creating_network:
                            gui.handle_action('RIGHT_MOUSE_DOWN', event.pos)
                        else:
                            option_screen.handle_action('RIGHT_MOUSE_DOWN', event.pos)
                    else:
                        selected_obj = all_networks[selected_network].get_closest_obj(event.pos)
                        print('Got closest obj with name: "%s"' % selected_obj.name)

                # LEFT CLICK
                elif event.button == 1:
                    # print('Left click found: {}'.format(event.pos))
                    if option_screen.is_active:
                        response = None
                        if gui.creating_network:
                            gui.handle_action('LEFT_MOUSE_DOWN', event.pos)
                        else:
                            response = option_screen.handle_action('LEFT_MOUSE_DOWN', event.pos)

                        if response is not None:
                            if response['type'] == 'terminate':
                                terminate()
                            elif response['type'] == 'add network':
                                gui.creating_network = True
                                # TODO: wrap up here
                                # all_networks.append(create_new_network())
                            else:
                                option_screen.show_incomplete_feature()
                    # not option screen, interact with all objects as normal
                    else:
                        print('Left click found: {}'.format(event.pos))
                        for network in all_networks:
                            network.handle_action(event.pos, action_type='LEFT_MOUSE_DOWN')

            # MOUSE BUTTON UP
            elif event.type == MOUSEBUTTONUP:
                # RIGHT CLICK
                if event.button == 3:
                    if not option_screen.is_active and not gui.creating_network:
                        print('Right mouse up found?')
                        selected_obj = None
                # LEFT CLICK
                if event.button == 1:
                    if not option_screen.is_active and not gui.creating_network:
                        # TODO: investigate if it is worth it to make Network.handle_action consistent with all other
                        #   handle actions where action_type comes first and event locations comes second
                        all_networks[selected_network].handle_action(event.pos, action_type='LEFT_MOUSE_UP')

        # Follow mouse
        if selected_obj:
            selected_obj.set_center(pygame.mouse.get_pos())

        # Re-draw background
        surface.fill(colors['BGCOLOR'])

        # Drawing objects
        if gui.creating_network:
            gui.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
            gui.draw_create_network(surface)
        elif option_screen.is_active:
            option_screen.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
            option_screen.draw(surface)
        else:
            for network in all_networks:
                network.step()
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
