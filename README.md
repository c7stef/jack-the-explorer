# Jack the Explorer

## Intro

Jack the Explorer is a 2D platformer game about an adventurer seeking to gather the jewels scattered across dangerous realms.

This readme file outlines installation and usage instructions, as well as details of development and implementation.

## Usage

The following packages must be installed:

- python (version >3.10.12)
- virtualenv (or python3-venv)
- GNU make

First install the required libraries:

```
make install
```

Run the game from the terminal with the command:

```
make run
```

To build an executable for windows run the *exec.bat* script.

To build an executable for linux run the *run.bash* script.

Building the static linked executable requires Python and the required libraries to be already installed on the machine.

## Technologies used

The game is written in Python using several libraries:

* Pygame
* Pymunk
* PyTMX
* ParticlePy

In addition, the open source program Tiled was used to design the maps which are imported in the game using PyTMX.

