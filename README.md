# YOLOL Simulator
This project strives to simulate the interaction between YOLOL code and all objects within its network. Please note that this project is still a work-in-progress and is not ready for 0.1 Release as of now. 0.1 Release will cover all the foundational code such that progress made for 1.0 should be as simple as adding more objects and touching up the GUIs. This means that all the hard work will need to be done before 0.1 and may take longer than expected.

Please see 'Current Work In Progress' to see what is being worked on, as well as to get a gauge of how much work is left to be done before the next release.

#### Controls:
- Left-click sends 'action' to object (on button down, and on button up supported)
- Right-click-DOWN snaps nearest object to cursor
- Right-click-UP releases selected object

### This project uses CYLON AST v0.3.0
- YOLOL AST Constructor provided by yoloxide: https://github.com/Jerald/yoloxide
- Current use of this program requires using Discord bot to get CYLON AST, will be automated for 0.1 Release

## Completed Work

### CYLON AST To Python Converter v0.1 (100% complete)
Could use better unit tests, see Known Issues below, needs to be fixed

### Integrate transpiled Python code generated from Cylon AST into Simulator through YOLOL Chips (100% complete of 100%)

## Current Work In Progress (Planned for 0.1 Release) 92% Complete

### GUI (35% complete of 40%)
It should be possible to create custom 'textures' for all components. Need to implement this with setup. (0% complete of 100%)

Need to create instructions screen page (80% complete of 100%)

##### GUI needs to show all objects in a network (100% complete of 100%)

##### Create UI to create Network with specific components (50% complete of 50%)

##### Create GUI for YOLOL Chip interaction (10% complete of 20%)

### Automate YOLOL to CYLON AST to Python (0% complete of 100%)

### Python Emulator Object Classes and Network (9.39% complete of 9.4%)
#### Planned devices for 0.1 Release 
- YOLOL Chip (99%)
- Button (99%)
- Lamp (99%)

#### Planned devices for 1.0 Release or sooner
- Cargo beam
- Carge crate
- Cargo lock frame
- Chip socket
- Fixed mount
- Generator
- Hinges
- Information screen
- Levers
- Memory chip
- Mining laser
- Modular crate
- Modular device rack
- Modular display
- Mounted weapons
- Mover
- Network relay
- Propellant aka gas canisters
- Radio transmitter/receiver
- Range finder
- Relay
- Robot arms
- Sensor strip
- Socket
- Tractor beam
- Thrusters
- Trigger
- Turntable

#### Not currently planning to support:
- Flight control unit
- Main flight computer

## Planned work for 0.2 Release
Dynamically create line methods as a part of each YOLOL chip object rather than having the interpreter create the functions and hard code the YOLOL Chip to import from the file the interpreter created

Improve network GUI by having a drop-down option to display information for each object in a network

## Want to Contribute?
This is an open source project and all contributions are welcome! Feel free to join the discord channel dedicated to CYLONS https://discord.gg/rmu6aCr and PM me (username=StolenLight) and I would be more than happy to discuss how you would like to help!

### What can you help with? 
Basically, every object right now needs a legit texture file (stored as JSON structure of a list of Pygame 'shapes'), and the YOLOL Chip needs a proper GUI to enter code.

The framework for basic objects has been created (i.e. Button and Lamp) and all other planned devices will need their proper class(es) to be created.

## What is YOLOL?
YOLOL is the in-game programming language for Starbase https://www.frozenbyte.com/games/starbase/

## Other Links:
For general information about YOLOL and AST: https://github.com/Jerald/yolol-is-cylons

Starbase wiki link for YOLOL: https://wiki.starbasegame.com/index.php/YOLOL


## Known Issues
### Does not properly interpret Cylon AST for:
a ++ -- b
