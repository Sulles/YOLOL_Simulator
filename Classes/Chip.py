"""
Created: July 13, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This class simulates the functionality of a YOLOL Chip in Starbase. As there are
three types of chips, all chips will have a subclass to inherit all common
features and checks to verify only valid commands are passed

for root, dirs, files in os.walk("/mydir"):
    for file in files:
        if file.endswith(".txt"):
             print(os.path.join(root, file))
"""

import os

# This is the sub-class
class _chip():
    def __init__(self, yolol_code, wait=0):
        self.name = yolol_code
        self.ChipWait = wait
        self.create_yolol_code(yolol_code)

    def _print(self):
        print("=== CHIP INFORMATION ===")
        print("Chip Name: {0}\n"
              "Chip Wait: {1}".format(self.name, self.ChipWait))

    def create_yolol_code(self, yolol_code):
        # TODO: Add assert for file existance
        self.parse_yolol(yolol_code)

    def parse_yolol(self, yolol_code):
        try:
            yolol = open(os.path.join("../YOLOLCode/{}.txt".format(yolol_code)), "r")
            # for line in yolol:

        except Exception as e:
            print("Could not open {0} because:\n{1}".format(
                yolol_code, e))
            raise e

        finally:
            yolol.close()


# This is the main chip class
# TODO: Add chip-specific functionality and verify code compatability for each chip type
class Chip(_chip):
    def __init__(self, yolol_code=""):
        assert isinstance(yolol_code, str), "Invalid YOLOL Code name"
        _chip.__init__(self, yolol_code)


# Unit test
if __name__ == "__main__":
    print("Running unit test for Chip class...")
    chip1 = Chip("chip_1")
