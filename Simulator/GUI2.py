"""
Created: October 12, 2019

Author: Sulles

=== DESCRIPTION ===
This class houses the revamped GUI object and all associated objects
"""
# noinspection PyUnresolvedReferences
from Classes.map import obj_map
# noinspection PyUnresolvedReferences
from gui_lib import ListObj, TabList, DisplayBox, InputExtendedListObj, CheckBox, ModifyTextBox
from pygame import font as pygame_font, draw as pygame_draw
# noinspection PyUnresolvedReferences
from src.constants import colors


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
        """ Constructor for the Main Menu object """
        Menu.__init__(self, 'MainMenu', ['Edit Networks', 'Edit Settings', 'Exit'], screen_size)
        self.menu_to_state_map = {'Edit Networks': 'edit_network', 'Edit Settings': 'edit_settings'}

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """ This method will handle all user actions for the Main Menu """
        if action_type == 'LEFT_MOUSE_DOWN':
            response = self.menu.handle_left_mouse_down(mouse_pos)
            if response == 'Exit':
                return dict(type='terminate')
            elif response in self.menu_to_state_map.keys():
                return dict(type='transition_state', new_state=self.menu_to_state_map[response])
        elif action_type == 'MOUSE_HOVER':
            self.menu.handle_hover(mouse_pos)
        else:
            print('{} does not support: {}'.format(self.name, action_type))

    def handle_escape(self):
        """ transition to normal state when escape is pressed """
        self.clean_up()
        return 'normal'

    def clean_up(self):
        pass


class EditNetwork(Menu):
    def __init__(self, screen_size):
        """ Constructor for the Edit Network object """
        Menu.__init__(self, 'EditNetwork', ['Create a New Network', 'Edit Objects in a Network', 'Delete a Network'],
                      screen_size)
        self.menu_to_state_map = {'Create a New Network': 'create_network', 'Edit Objects in a Network': 'edit_objects',
                                  'Delete a Network': 'delete_network'}

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """ This method will handle all user actions for the Main Menu """
        if action_type == 'MOUSE_HOVER':
            self.menu.handle_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            response = self.menu.handle_left_mouse_down(mouse_pos)
            if response in self.menu_to_state_map.keys():
                return dict(type='transition_state', new_state=self.menu_to_state_map[response])
        else:
            print('{} does not support: {}'.format(self.name, action_type))

    def handle_escape(self):
        """ transition to main_menu state when escape is pressed """
        self.clean_up()
        return 'main_menu'

    def clean_up(self):
        pass


class CreateNetwork:
    def __init__(self, screen_size):
        """ Constructor for creating a new network """
        self.name = 'CreateNetwork'
        self.screen_size = screen_size
        self.all_states = dict(select_objects=CreateNetworkSelectObjects(screen_size),
                               edit_objects=CreateNetworkEditObjects(screen_size))
        self.state = self.all_states['select_objects']

    def draw(self, surface):
        """ This method passes the drawing responsibility to the states """
        self.state.draw(surface)

    def transition_state(self, new_state):
        if new_state not in self.all_states.keys():
            print('{} IS AN INVALID {} STATE, only states available are: {}'.format(
                new_state, self.name, self.all_states.keys()))
            return
        print('{} Transitioning to state: {}'.format(self.name, new_state))
        self.state = self.all_states[new_state]

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """ This method will handle all user actions for creating a new network """
        response = self.state.handle_action(action_type, mouse_pos, key)
        if type(response) is dict:
            if 'type' in response.keys() and response['type'] == 'transition_state':
                if response['new_state'] in self.all_states.keys():
                    self.transition_state(response['new_state'])
                    self.state.add_objects(response['data'])

    def handle_escape(self):
        """ transition to edit_network state when escape is pressed """
        self.clean_up()
        return 'edit_network'

    def clean_up(self):
        self.state = self.all_states['select_objects']


class CreateNetworkSelectObjects:
    def __init__(self, screen_size):
        """ Constructor for selecting objects to add to a new network """
        self.screen_size = screen_size
        self.all_objects = InputExtendedListObj(list(obj_map.keys()), screen_size,
                                                x_offset=-int(screen_size['width'] / 2) + 80,
                                                y_offset=-int(screen_size['height'] / 4) + 60)
        # def __init__(self, center, text=None, color_map=None, width=50, height=50):
        self.submit = CheckBox([int(screen_size['width'] / 2), int(3 * screen_size['height'] / 4 + 50)],
                               text='Continue?')

    def draw(self, surface):
        """ This method handles drawing all possible objects to be added to a new network """
        self.all_objects.draw(surface)
        self.submit.draw(surface)

    def handle_action(self, action_type, mouse_pos, key):
        """ This method handles all actions while selecting objects to add to a new network """
        response = self.all_objects.handle_action(action_type, mouse_pos)
        if response is None:
            if self.submit.handle_action(action_type, mouse_pos) == 'selected':
                return dict(type='transition_state', new_state='edit_objects', data=self.all_objects.get_network())
        return response


class CreateNetworkEditObjects:
    def __init__(self, screen_size):
        """ Constructor for editing objects in a new network """
        self.screen_size = screen_size
        self.network_settings = list()
        self.object_options = list()
        self.selected_object = None

    def add_objects(self, add_obj_dict):
        print('Adding: {} to {}'.format(add_obj_dict, 'CreateNetworkEditObjects'))
        assert len(add_obj_dict) is not None, 'No objects selected for a new network...'
        for object_type, num in add_obj_dict.items():
            if num != 0:
                for x in range(num):
                    # Build default settings for each object
                    self.network_settings.append({object_type: dict(name='default',
                                                                    center=[int(self.screen_size['width'] / 2),
                                                                            int(self.screen_size['height'] / 2)])})
        print('Updated objects: {}'.format(self.network_settings))
        self.create_all_objects()

    def create_all_objects(self):
        center = [150, 20]
        self.object_options = list()
        count = 0
        for obj in self.network_settings:
            for object_type, settings in obj.items():
                count += 1
                center[1] += 30
                # def __init__(self, prompt, center, width=None, height=50):
                self.object_options.append(ModifyTextBox(object_type, center, height=30))
                # If filled up all left column, start next one
                if count >= 15:
                    count = 0
                    center = [300, 20]
                else:
                    center[0] = 150

    def draw(self, surface):
        """ This method handles drawing all editing options for all objects in a new network """
        for obj in self.object_options:
            obj.draw(surface)

    def handle_action(self, action_type, mouse_pos, key=None):
        """ This method handles all actions while editing object properties for a new network """
        for obj in self.object_options:
            obj.handle_action(action_type, mouse_pos, key)


class EditObjects:
    def __init__(self, screen_size):
        """ Constructor for editing objects in a network """
        self.name = 'EditObjects'
        self.screen_size = screen_size

    def draw(self, surface):
        pass

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """ This method will handle all user actions for editing objects in a network """
        pass

    def handle_escape(self):
        """ transition to edit_network state when escape is pressed """
        self.clean_up()
        return 'edit_network'

    def clean_up(self):
        pass


class DeleteNetwork:
    def __init__(self, screen_size):
        """ Constructor for deleting a network """
        self.name = 'DeleteNetwork'
        self.screen_size = screen_size

    def draw(self, surface):
        pass

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """ This method will handle all user actions for deleting a network """
        pass

    def handle_escape(self):
        """ transition to edit_network state when escape is pressed """
        self.clean_up()
        return 'edit_network'

    def clean_up(self):
        pass


class EditSettings(Menu):
    def __init__(self, screen_size):
        """ Constructor for the Edit Network object """
        Menu.__init__(self, 'EditSettings', ['Change screen size', 'Change FPS'], screen_size)
        self.menu_to_state_map = {'Change screen size': 'change_screen_size', 'Change FPS': 'change_fps'}

    def draw(self, surface):
        pass

    def handle_escape(self):
        """ transition to main_menu state when escape is pressed """
        self.clean_up()
        return 'main_menu'

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """ This method will handle all user actions for the Edit Settings option """
        if action_type == 'MOUSE_HOVER':
            self.menu.handle_hover(mouse_pos)
        elif action_type == 'LEFT_MOUSE_DOWN':
            response = self.menu.handle_left_mouse_down(mouse_pos)
            if response in self.menu_to_state_map.keys():
                print('So you want to {}?'.format(response))
        else:
            print('{} does not support: {}'.format(self.name, action_type))

    def clean_up(self):
        pass


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
        self.active_tab = self.network_tabs.get_active_tab()
        self.all_network_tree_objects = dict()

    def add_network(self, network):
        """
        This method adds a network to the Normal GUI state
        :param network: Network object with all objects associated with it
        """
        self.all_networks.append(network)
        self.network_tabs.add_tab(network.name)
        self.build_network_tree_objects(network)

    def build_network_tree_objects(self, network):
        """ This method builds all the info tree objects for a Network object """
        point = [10, 50]
        info_tree = network.get_info_tree()
        self.all_network_tree_objects[network.name] = list()
        self.all_network_tree_objects[network.name].append(DisplayBox(text=network.name, middle_left=point))
        point[0] += 15
        for obj_name, obj_stats in info_tree.items():
            # print('object name? {}'.format(obj_name))
            point[1] += 22
            self.all_network_tree_objects[network.name].append(DisplayBox(text=obj_name, middle_left=point))
            point[0] += 15
            for stats in obj_stats:
                # print('stats? {}'.format(stats))
                point[1] += 22
                self.all_network_tree_objects[network.name].append(DisplayBox(text=stats, middle_left=point))
            point[0] -= 15
        self.all_network_tree_objects[network.name].append(info_tree)

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
        self.active_tab = self.network_tabs.get_active_tab()
        self.network_tabs.draw(surface)
        self.draw_network_link(surface)
        for network in self.all_networks:
            network.draw(surface)
        self.draw_network_info_tree(surface)

    def draw_network_info_tree(self, surface):
        """
        This method draws the active network's info tree
        :param surface: PyGame surface object
        """
        # first check for info tree changes
        current_network_info_tree = self.all_networks[self.active_tab['index']].get_info_tree()
        if current_network_info_tree != self.all_network_tree_objects[self.active_tab['name']][-1]:
            # print('info trees do not match!')
            self.resolve_info_tree_mismatch()
        for x in range(len(self.all_network_tree_objects[self.active_tab['name']]) - 1):
            self.all_network_tree_objects[self.active_tab['name']][x].draw(surface)

    def draw_network_link(self, surface):
        """ This method will draw a link between all objects in a network and the corresponding network tab """
        first_point = list(self.network_tabs.get_tab_center(self.active_tab))
        first_point[1] += 20
        second_point = [first_point[0], first_point[1] + 20]
        for obj in self.all_networks[self.active_tab['index']].objects:
            third_point = [obj.center[0], second_point[1]]
            fourth_point = [obj.center[0], int(obj.center[1] - obj.height / 2)]
            pygame_draw.lines(surface, colors['LIGHTGRAY'], False,
                              [first_point, second_point, third_point, fourth_point])

    def resolve_info_tree_mismatch(self):
        """ This method resolves any info tree data mismatch """
        # TODO: This can be optimized to use update_text() instead of deleting and recreating the objects
        del self.all_network_tree_objects[self.active_tab['name']]
        self.build_network_tree_objects(self.all_networks[self.active_tab['index']])

    def handle_action(self, action_type, mouse_pos=None, key=None):
        """
        This method passes action handling to everything that is necessary. This method is responsible for:
            - Network tab action handling
            - All object action handling for all networks
            - **TBD** Network info tab action handling?
        """
        # handle select nearest object first
        if action_type == 'RIGHT_MOUSE_DOWN':
            return dict(type='new_selection',
                        object=self.all_networks[self.active_tab['index']].get_closest_obj(mouse_pos))

        response = None
        for network in self.all_networks:
            response = network.handle_action(action_type, mouse_pos)
        if response is None:
            response = self.network_tabs.handle_action(action_type, mouse_pos)
        return response

    @staticmethod
    def handle_escape():
        """ transition to main_menu state on when escape is pressed """
        return 'main_menu'


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
                               edit_settings=EditSettings(screen_size),
                               create_network=CreateNetwork(screen_size),
                               edit_objects=EditObjects(screen_size),
                               delete_network=DeleteNetwork(screen_size))
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
        except Exception as e:
            print('GUI2 is in state: "{}" when the following error was created: {}'.format(self.state.name, e))
            raise

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
            response = self.state.handle_action(action_type, mouse_pos, key)
        else:
            raise (AttributeError, 'GUI2 state is None, how???')

        # Handle responses
        if type(response) is dict:
            if 'type' in response.keys() and response['type'] == 'transition_state':
                print('Got GUI2 transition state request from: {}'.format(self.state.name))
                self.transition_state(response['new_state'])
                return None
            # print('GUI got action response: {}'.format(response))
        return response

    def handle_escape(self):
        """ This method is responsible for handling the transition between states for the GUI2 object """
        self.transition_state(self.state.handle_escape())
