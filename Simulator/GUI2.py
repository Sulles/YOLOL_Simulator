"""
Created: October 12, 2019

Author: Sulles

=== DESCRIPTION ===
This class houses the revamped GUI object and all associated objects
"""
from gui_lib import *
# from .gui_lib import *
from pygame import font as pygame_font


class Menu:
    def __init__(self, name, options, screen_size):
        """
        Constructor for the Menu object, will handle basic comparison, string, and drawing functionality of all menus
        :param name: String name of the Menu object
        :param options: List of strings of all menu options
        :param screen_size: dictionary with key, value pairs:
            - 'width': int (pixel width of screen)
            - 'height': int (pixel height of screen)
        """
        self.name = name
        self.options = options
        self.menu = ListObj(self.options, screen_size)

    def __cmp__(self, other):
        """ Only use name for comparison """
        return self.name == other

    def __str__(self):
        """ Only use name for string """
        return self.name

    def draw(self, surface):
        """ Pass drawing to the list object """
        return self.menu.draw(surface)


class MainMenu(Menu):
    def __init__(self, screen_size):
        """
        Constructor for the Main Menu object
        :param screen_size: dictionary with key, value pairs:
            - 'width': int (pixel width of screen)
            - 'height': int (pixel height of screen)
        """
        Menu.__init__(self, 'MainMenu', ['Edit Networks', 'Edit Settings', 'Exit'], screen_size)
        self.menu_to_state_map = {'Edit Networks': 'edit_network', 'Edit Settings': 'edit_settings'}

    def handle_action(self, action_type, mouse_pos=None):
        """
        This method will handle all user actions for the Main Menu
        :param action_type: String which describes the type of action that needs to be handled
        :param mouse_pos: [x, y] pixel position of the mouse
        :return: None, will raise error if fails
        """
        if action_type == 'LEFT_MOUSE_DOWN':
            response = self.menu.handle_left_mouse_down(mouse_pos)
            if response == 'Exit':
                return dict(type='terminate')
            elif response != "":
                return dict(type='transition_state', new_state=self.menu_to_state_map[response])
        elif action_type == 'MOUSE_HOVER':
            self.menu.handle_hover(mouse_pos)
        else:
            print('{} does not support: {}'.format(self.name, action_type))


class EditNetwork(Menu):
    def __init__(self, screen_size):
        """
        Constructor for the Edit Network object
        :param screen_size: dictionary with key, value pairs:
            - 'width': int (pixel width of screen)
            - 'height': int (pixel height of screen)
        """
        Menu.__init__(self, 'EditNetwork', ['Create a New Network', 'Edit Objects in a Network', 'Delete a Network'],
                      screen_size)

    def handle_action(self, action_type, mouse_pos=None):
        """
        This method will handle all user actions for the Main Menu
        :param action_type: String which describes the type of action that needs to be handled
        :param mouse_pos: [x, y] pixel position of the mouse
        :return: None, will raise error if fails
        """
        if action_type == 'MOUSE_HOVER':
            self.menu.handle_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            self.menu.handle_left_mouse_down(mouse_pos)
        else:
            print('{} does not support: {}'.format(self.name, action_type))


class EditSettings(Menu):
    def __init__(self, screen_size):
        """
        Constructor for the Edit Network object
        :param screen_size: dictionary with key, value pairs:
            - 'width': int (pixel width of screen)
            - 'height': int (pixel height of screen)
        """
        Menu.__init__(self, 'EditSettings', ['Change screen size', 'Change FPS'], screen_size)

    def handle_action(self, action_type, mouse_pos=None):
        """
        This method will handle all user actions for the Main Menu
        :param action_type: String which describes the type of action that needs to be handled
        :param mouse_pos: [x, y] pixel position of the mouse
        :return: None, will raise error if fails
        """
        if action_type == 'MOUSE_HOVER':
            self.menu.handle_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            self.menu.handle_left_mouse_down(mouse_pos)
        else:
            print('{} does not support: {}'.format(self.name, action_type))


class Normal:
    def __init__(self):
        """
        Constructor for all normal operation for the GUI. This handles:
            - Network info
            - Network tabs
            - Network links
            - All objects in all networks
        """
        self.name = 'Normal'
        self.all_networks = list()

        # self.small_font = pygame_font.Font('src/Cubellan.ttf', 8)
        self.basic_font = pygame_font.Font('src/Cubellan.ttf', 12)
        # self.large_font = pygame_font.Font('src/Cubellan.ttf', 18)

        self.network_tabs = TabList(self.basic_font, list())

    def add_network(self, network):
        self.all_networks.append(network)
        self.network_tabs.add_tab(network.name)

    def step(self):
        """ Step all networks by one tick """
        for network in self.all_networks:
            network.step()

    def draw(self, surface):
        """
        This method handles drawing everything under normal circumstances
        :param surface: PyGame surface object
        :return: None, will raise error if fails
        """
        self.draw_network_info(surface)
        self.network_tabs.draw(surface)
        self.draw_network_link(surface)
        for network in self.all_networks:
            network.draw(surface)

    def draw_network_info(self, surface):
        """
        This method will display all objects within the active network
        :param surface: PyGame surface object
        :return: None, will raise error if fails
        """
        pass

    def draw_network_link(self, surface):
        """
        This method will draw a link between all objects in a network and the corresponding network tab
        :param surface: PyGame surface object
        :return: None, will raise error if fails
        """
        pass

    def handle_action(self, action_type, mouse_pos=None):
        """
        This method passes action handling to all networks
        :param action_type: String which describes the type of action that needs to be handled
        :param mouse_pos: [x, y] pixel position of the mouse
        :return: None, will raise error if fails
        """
        self.network_tabs.handle_action(action_type, mouse_pos)
        for network in self.all_networks:
            network.handle_action(action_type, mouse_pos)


class GUI2:
    def __init__(self, screen_size):
        """
        Constructor for the entire GUI
        """
        self.name = 'GUI2'

        # Misc
        self.screen_size = screen_size

        # Creating all Menus/States
        self.all_states = dict(normal=Normal(),
                               main_menu=MainMenu(screen_size),
                               edit_network=EditNetwork(screen_size),
                               edit_settings=EditSettings(screen_size))
        self.name_to_state_map = dict(Normal='normal', MainMenu='main_menu', EditNetwork='edit_network',
                                      EditSettings='edit_settings')
        self.state = self.all_states['normal']

    def __cmp__(self, other):
        """ Only use name for comparison """
        return self.name == other

    def __str__(self):
        """ Only use name for string """
        return self.name

    def transition_state(self, new_state_name):
        if new_state_name not in self.all_states.keys():
            print('INVALID GUI2 STATE: {}'.format(new_state_name))
        print('GUI2 transitioning state to: {}'.format(new_state_name))
        self.state = self.all_states[new_state_name]

    def add_network(self, network):
        """
        This method properly handles the GUI adding a new network
        :param network: Network object to be added to GUI handling
        :return: None, will raise error if fails
        """
        start_state = self.state.name
        # Get to Normal state if not in it
        if start_state != 'Normal':
            self.transition_state('normal')
        # Handle adding a network
        self.state.add_network(network)
        # Return to previous state if not already in Normal state
        if start_state != 'Normal':
            self.transition_state(self.name_to_state_map[start_state])

    def draw(self, surface):
        """
        Main draw handler
        :param surface: PyGame surface object
        :return: None, will raise error if fails
        """
        try:
            self.state.draw(surface)
        except Exception:
            print('GUI2 is in state: {}, a state without proper drawing handling'.format(self.state.name))

    def step(self):
        """
        The main stepper for all networks
        :return: None, will raise error if fails
        """
        # We only care about stepping for the Normal use case
        if self.state.name == 'Normal':
            self.state.step()

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """
        Main action handler
        :param action_type: String which describes the type of action that needs to be handled
        :param mouse_pos: [x, y] pixel position of the mouse
        :param key: PyGame event.key object for user input
        :return: None, will raise error if fails
        """
        response = None
        if action_type == 'ESCAPE':
            self.handle_escape()
        elif self.state is not None:
            response = self.state.handle_action(action_type, mouse_pos)
        else:
            raise (AttributeError, 'GUI2 state is None, how???')

        # Handle responses
        if response is not None:
            if response['type'] == 'transition_state':
                print('Got GUI2 transition state request from: {}'.format(self.state.name))
                self.transition_state(response['new_state'])
                return None
        return response

    def handle_escape(self):
        """ This method is responsible for handling the transition between states for the GUI2 object """
        if self.state == self.all_states['normal']:
            self.transition_state('main_menu')
        elif self.state == self.all_states['main_menu']:
            self.transition_state('normal')
        elif self.state == self.all_states['edit_network']:
            self.transition_state('main_menu')
        elif self.state == self.all_states['edit_settings']:
            self.transition_state('main_menu')
        else:
            print('This should not be happening... GUI2 is in state: {} and all possible states are: {}'.format(
                self.state, self.all_states))
            self.state = self.all_states['main_menu']
