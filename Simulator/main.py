"""
Created: July 14, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This is the main simulator code. From here, users can
"""


import pygame
import sys
from pygame.locals import *
# from time import time

# noinspection PyUnresolvedReferences
from src.constants import colors

# import os
# from pprint import pprint


def simulator():
    pygame.init()
    surface = pygame.display.set_mode((800, 500))
    FPS_CLOCK = pygame.time.Clock()
    FPS = 60
    # START_TIME = time()
    pygame.display.set_caption('Proving Ground')

    # Initialize Network here

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
                if event.button == 3:       # right click
                    print("Right click found!")
                    # engine.add_body(event.pos, (0, 0), (0, 0), 0, 1, randint(10, 50))
                elif event.button == 1:     # left click
                    print("Left click found!")
                    # if not selected_eid and engine.bm.len() > 0:
                    #     selected_eid = \
                    #         min([(abs(b[0][0] - event.pos[0]) + abs(b[0][1] - event.pos[1]), b[2]) for b in
                    #              engine.bodies()],
                    #             key=lambda x: x[0])[1]  # get eid of closest body
                    # else:
                    #     selected_eid = None

        surface.fill(colors['BGCOLOR'])

        # Draw everything here

        # Perform tick update here

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


''' RUN MAIN FUNCTION '''
if __name__ == "__main__":
    simulator()
