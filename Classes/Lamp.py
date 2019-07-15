"""
Created: July 13, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This class simulates the funtionality of a Lamp in Starbase.
"""


class Lamp():
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
        self.LampOn = settings['on']
        self.lumens_list = [0, settings['lumens']]
        self.hue_list = [0, settings['hue']]
        self.saturation_list = [0, ['saturation']]
        self.value_list = [0, settings['value']]
        self.range_list = [0, settings['range']]

        self.LampLumens = self.LampColorHue = self.LampColorSaturation = \
            self.LampColorValue = self.LampRange = None
        self.enable_disable()

    def toggle_on_off(self):
        if self.LampOn:
            self.LampOn = False
        else:
            self.LampOn = True
        self.enable_disable()

    def enable_disable(self):
        self.LampLumens = self.lumens_list[self.LampOn]
        self.LampColorHue = self.hue_list[self.LampOn]
        self.LampColorSaturation = self.saturation_list[self.LampOn]
        self.LampColorValue = self.value_list[self.LampOn]
        self.LampRange = self.range_list[self.LampOn]

    def _print(self):
        print("=== LAMP INFORMATION ===\n"
              "Name: {0}\n"
              "Is ON: {1}\n"
              "Current Lumens: {2}\n"
              "Current Hue: {3}\n"
              "Current Saturation: {4}\n"
              "Current Value: {5}\n"
              "Current Range: {6}".format(
            self.name, self.LampOn, self.LampLumens, self.LampColorHue,
            self.LampColorSaturation, self.LampColorValue, self.LampRange))


# Unit test
if __name__ == "__main__":
    lamp = Lamp(on=True)
    lamp._print()
    lamp.toggle_on_off()
    lamp._print()
