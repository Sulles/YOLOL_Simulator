"""
Created: July 14, 2019
Last Updated: August 3, 2019

Author: Sulles

=== DESCRIPTION ===
This is the main simulator code. From here, users can

TODO: Make shift + right click = plane move?
"""

import os
import sys

import pygame
# noinspection PyUnresolvedReferences
from Classes.Network import Network
# noinspection PyUnresolvedReferences
from GUI import GUI
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
    all_networks.append(Network('test_network_1', network_settings))

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
    # all_networks.append(Network('test_network_2', network_settings))
    for network in all_networks:
        selected_network = gui.add_network(network)

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
                    if gui.creating_network or gui.deleting_network:
                        print('currently creating a network')
                        gui.handle_action('ESCAPE')
                    else:
                        print('option screen is handling escape now')
                        option_screen.handle_action('ESCAPE')
                        # option_screen.print()
                elif gui.creating_network:
                    gui.handle_action('KEYDOWN', key=event.key)

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
                        print('Got closest obj with name: {}'.format(selected_obj.name))

                # LEFT CLICK
                elif event.button == 1:
                    # print('Left click found: {}'.format(event.pos))
                    if option_screen.is_active:
                        response = None
                        if gui.creating_network:
                            response = gui.handle_action('LEFT_MOUSE_DOWN', event.pos)
                        else:
                            response = option_screen.handle_action('LEFT_MOUSE_DOWN', event.pos)

                        if response is not None:
                            if response['type'] == 'terminate':
                                terminate()
                            elif response['type'] == 'add_network':
                                gui.start_create_network()
                                print('turning on gui.creating_network')
                            elif response['type'] == 'new_network':
                                option_screen.is_active = False
                                all_networks.append(Network(response['network_name'], response['network_settings']))
                                gui.add_network(all_networks[-1])
                                selected_network = len(all_networks) - 1
                            elif response['type'] == 'start_delete_network':
                                option_screen.is_active = False
                                gui.start_delete_network()
                                print('Starting delete network process...')
                            else:
                                option_screen.show_incomplete_feature()
                    # not option screen, interact with all objects as normal
                    else:
                        print('Left click found: {}'.format(event.pos))
                        response = gui.handle_action('LEFT_MOUSE_DOWN', event.pos)
                        if response is None:
                            for network in all_networks:
                                network.handle_action('LEFT_MOUSE_DOWN', event.pos)
                        elif response['type'] == 'active_tab':
                            selected_network = response['active_tab_index']
                        elif response['type'] == 'deleted_network':
                            for network in all_networks:
                                if network.name == response['network_name']:
                                    all_networks.remove(network)
                            print('Removed network: {}'.format(response['network_name']))


            # MOUSE BUTTON UP
            elif event.type == MOUSEBUTTONUP:
                # RIGHT CLICK
                if event.button == 3:
                    if not option_screen.is_active and not gui.creating_network:
                        selected_obj = None
                # LEFT CLICK
                if event.button == 1:
                    if not option_screen.is_active and not gui.creating_network:
                        for network in all_networks:
                            network.handle_action('LEFT_MOUSE_UP', event.pos)

        # Follow mouse
        if selected_obj:
            selected_obj.set_center(pygame.mouse.get_pos())

        # Re-draw background
        surface.fill(colors['BGCOLOR'])

        # Drawing objects
        if gui.creating_network:
            gui.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
            gui.draw_create_network(surface)
        elif gui.deleting_network:
            gui.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
            gui.draw_delete_network(surface)
        elif option_screen.is_active:
            option_screen.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
            option_screen.draw(surface)
        else:
            gui.handle_action('MOUSE_HOVER', pygame.mouse.get_pos())
            gui.draw(surface)
            for network in all_networks:
                network.step()
                network.draw(surface)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


''' RUN MAIN FUNCTION '''
if __name__ == "__main__":
    simulator()
