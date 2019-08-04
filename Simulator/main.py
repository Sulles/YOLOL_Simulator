"""
Created: July 14, 2019
Last Updated: August 3, 2019

Author: StolenLight

=== DESCRIPTION ===
This is the main simulator code. From here, users can
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
from src.GUI import GUI
# noinspection PyUnresolvedReferences
from Classes.Network import Network


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

    # Initialize Network here
    network_settings = {'Button0':
                            {'name': 'butt_name',
                             'state': 0,
                             'position': [DISPLAY['width'] / 2, DISPLAY['height'] / 2],
                             'color_map': [colors['RED'], colors['GREEN']]},
                        'Lamp':
                            {'name': 'lamp_name',
                             'state': 1,
                             'position': [DISPLAY['width'] - 100, DISPLAY['height'] / 2]}}
    network = Network('test_network', network_settings)

    print("Initialization complete, running playground...")

    # MAIN LOOP
    while True:

        for event in pygame.event.get():
            # EXIT CONDITION
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()

                # OBJECT SELECTION
                # elif selected_eid:
                #     if event.key == K_r:
                #         print("Mark receivers")
                #         engine.mark_receiver(selected_eid, True)
                #     elif event.key == K_BACKSPACE:
                #         engine.remove_body(selected_eid)
                #         selected_eid = None

            elif event.type == MOUSEBUTTONDOWN:
                # pprint(vars(event))
                if event.button == 3:  # right click
                    print('Right click found: {}'.format(event.pos))
                    # engine.add_body(event.pos, (0, 0), (0, 0), 0, 1, randint(10, 50))
                elif event.button == 1:  # left click
                    print('Left click found: {}'.format(event.pos))
                    network.handle_action(event.pos, action_type='LEFT_MOUSE_DOWN')

        surface.fill(colors['BGCOLOR'])

        # Drawing objects
        network.draw(surface)
        # for obj in network.get_objects():
        #     pygame.draw.rect(surface, obj.color, obj.rect)

        # Drawing GUI
        gui.draw(surface)

        # Perform tick update here

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


''' RUN MAIN FUNCTION '''
if __name__ == "__main__":
    simulator()
