"""
Created: July 14, 2019
Last Updated:

Author: StolenLight

=== DESCRIPTION ===
This script transpiles CYLON AST to Python
"""

import json


def __main__():
    file = open("CylonAST/.txt", 'r')
    ast = json.load(file)

    print_json(ast)


def print_json(jsn):
    print(json.dumps(jsn, indent=2, sort_keys=True))


if __name__ == "__main__":
    __main__()
