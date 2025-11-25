# Topcap

## Project goal

Goal of this project is to create a virtual Topcap game, that was played once by Léo in the Z10 with some random guy.

This game is similar to chess in a sense that it is very simple but it has many many possibilities, making it hard to master. Still being much simpler than chess, this is the perfect environment to test Bots!

We will be able to implement Rule-based AIs, statistical approaches, and even Reinforcement learning agents to play and master this game. The goal is to compare them against each other and see who can build the best AI and if we can build an AI that beats us humans (probably yes)

## Code Structure

This package is tried to be held as maintainable as possible, to get used to write clean code and to be able to work with multiple people on this project and to facilitate entry.

This is my first time, but this python code is now a **module** called "topcap". It's basically a custom pip library that can be imported like any other with for example:

```python
import topcap.core.common as common
from topcap.agents import HumanAgent
from topcap import Game
```

The pip package is defined in the setup.py script at the root of the project and can be installed using `pip install -e .` in the root folder. Carrybots does this, so i guess it's good practice.

## How to?

### Install

Navigate to the root folder (the same where this readme is located)

Then install the package:

```bash
pip install -e .
```

The -e installs it in "editable" mode, perfect for development, because it automatically updates the package upon change. Without it, we would need to run pip install each time we changed some code.
