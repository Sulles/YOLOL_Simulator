"""
Created: August 3, 2019
Last Updated: August 3, 2019

Author: StolenLight

=== DESCRIPTION ===
This class houses the GUI
"""
from .constants import colors
import pygame.font
import pygame.draw
from pygame import Rect


class GUI:
    def __init__(self, display_settings):
        # SETTING UP FONT
        self.small_font = pygame.font.Font('src/Cubellan.ttf', 8)
        self.basic_font = pygame.font.Font('src/Cubellan.ttf', 12)
        self.large_font = pygame.font.Font('src/Cubellan.ttf', 18)

        # SETTING UP LOCATION
        self.position = [10, 10]
        self.width = 100
        self.height = int(display_settings['height'] / 2)
        self.color = (100, 100, 100)
        self.rect1 = Rect(self.position[0], self.position[1], self.width, self.height)
        self.rect2 = Rect(self.position[0] + 2, self.position[1] + 2, self.width - 4, self.height - 4)
        self.rect3 = Rect(self.position[0] + 4, self.position[1] + 4, self.width - 8, self.height - 8)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect1)
        pygame.draw.rect(surface, colors['WHITE'], self.rect2, 1)
        pygame.draw.rect(surface, colors['WHITE'], self.rect3, 1)
