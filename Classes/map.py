"""
Created: July 13, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This file houses the map of expected functions for each device/machine

For Example: YOLOL code has line...
:ButtonState = 0

This function knows that a Button object is expected
"""

from Button import Button
from Chip import Chip
from Lamp import Lamp

obj_map = {
    "Button": Button,
    "Chip": Chip,
    "Lamp": Lamp
}

func_map = {
    "CargoBeam": ['CargoBeamOnState', 'CargoBeamSearchLength'],
    "FixedMount": ['CurrentState', 'OnState', 'OffState', 'ButtonStyle'],
    "Generator": ['FuelChamberFuel', 'FuelChamberMaxFuel',
        'FuelChamberUnitRateLimit', 'FuelChamberUnitRate',
        'GeneratorUnitRateLimit', 'GeneratorUnitRate', 'StoredCoolant',
        'MaxCoolant', 'CoolerUnitRateLimit', 'CoolerUnitRate',
        'SocketUnitRateLimit', 'SocketUnitRate'],
    "Button": ['ButtonState', 'ButtonOnStateValue', 'ButtonOffStateValue',
        'ButtonStyle'],
    "Chip": ['ChipWait'],
    "Lamp": ['LampOn', 'LampLumens', 'LampColorHue', 'LampColorSaturation',
        'LampColorValue', 'LampRange']
}


# Unit test
if __name__ == "__main__":
    print("Running unit test for maps...")
    for key in obj_map.keys():
        try:
            print("================")
            print("Got Object: {0}\n"
                  "Available functions: {1}".format(key,
                                                    [_ for _ in func_map[key]]))
        except Exception as e:
            print("Uh oh! Object {0} not found in map?".format(key))
            print(e)
            raise e
