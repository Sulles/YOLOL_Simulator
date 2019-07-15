"""
Created: July 13, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This class simulates the funtionality of a Lamp in Starbase.
"""


class Lamp:
    def __init__(self, input_settings):
        """
        :param input_settings: dictionary of settings.
            Expected dictionary keys are: name, on, lumens, hue, saturation,
                value, and range.
        """
        settings = {'name': 0, 'on': False, 'lumens': 600, 'hue': 200,
                    'saturation': 0.5, 'value': 0.5, 'range': 10}

        for set in settings.keys():
            if set in input_settings:
                settings[set] = input_settings[set]

        self.name = settings['name']
        self.lampon = settings['on']
        self.lumens_list = [0, settings['lumens']]
        self.hue_list = [0, settings['hue']]
        self.saturation_list = [0, ['saturation']]
        self.value_list = [0, settings['value']]
        self.range_list = [0, settings['range']]

        self.lamplumens = self.lampcolorhue = self.lampcolorsaturation = \
            self.lampcolorvalue = self.lamprange = None
        self.enable_disable()

    def toggle_on_off(self):
        if self.lampon:
            self.lampon = False
        else:
            self.lampon = True
        self.enable_disable()

    def enable_disable(self):
        self.lamplumens = self.lumens_list[self.lampon]
        self.lampcolorhue = self.hue_list[self.lampon]
        self.lampcolorsaturation = self.saturation_list[self.lampon]
        self.lampcolorvalue = self.value_list[self.lampon]
        self.lamprange = self.range_list[self.lampon]

    def print(self):
        print("=== LAMP INFORMATION ===\n"
              "Name: {0}\n"
              "Is ON: {1}\n"
              "Current Lumens: {2}\n"
              "Current Hue: {3}\n"
              "Current Saturation: {4}\n"
              "Current Value: {5}\n"
              "Current Range: {6}".format(
                self.name, self.lampon, self.lamplumens, self.lampcolorhue,
                self.lampcolorsaturation, self.lampcolorvalue, self.lamprange))


# Unit test
if __name__ == "__main__":
    lamp = Lamp({"on": True, "lumens": 500, "hue": 150, "saturation": 0.8, "value": 0.2, "range": 8})
    lamp.print()
    lamp.toggle_on_off()
    lamp.print()
