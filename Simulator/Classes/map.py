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

from .Button import *
from .Chip import *
from .Lamp import *

obj_map = {
    'Button': Button,
    'Button0': Button0,
    'Chip': Chip,
    'Lamp': Lamp
}

func_map = {
    'CargoBeam': ['cargobeamonstate', 'cargobeamsearchlength'],
    'FixedMount': ['currentstate', 'onstate', 'offstate', 'buttonstyle'],
    'Generator': ['fuelchamberfuel', 'fuelchambermaxfuel',
                  'fuelchamberunitratelimit', 'fuelchamberunitrate',
                  'generatorunitratelimit', 'generatorunitrate', 'storedcoolant',
                  'maxcoolant', 'coolerunitratelimit', 'coolerunitrate',
                  'socketunitratelimit', 'socketunitrate'],
    'Button': ['buttonstate', 'buttononstatevalue', 'buttonoffstatevalue',
               'buttonstyle'],
    'Chip': ['chipwait'],
    'Lamp': ['lampon', 'lamplumens', 'lampcolorhue', 'lampcolorsaturation',
             'lampcolorvalue', 'lamprange']
}

# Unit test
if __name__ == '__main__':
    print('Running unit test for maps...')
    for key in obj_map.keys():
        try:
            print('================')
            print('Got Object: {0}\n'
                  'Available functions: {1}'.format(key,
                                                    [_ for _ in func_map[key]]))
        except Exception as e:
            print('Uh oh! Object {0} not found in map?'.format(key))
            print(e)
            raise e
