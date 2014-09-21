import random
import time
from collections import defaultdict
import itertools
import pdb

import logging
logger = logging.getLogger(__name__)
from game import Game, Hero
import ai

__all__ = ["RandomBot", "AStarBot"]

stay = 'Stay'
north = 'North'
south = 'South'
east = 'East'
west = 'West'

opposite = {
    north: south,
    south: north,
    west: east,
    east: west
}


AIM = {'North': (-1, 0),
       'East': (0, 1),
       'South': (1, 0),
       'West': (0, -1),
       'Stay': (0, 0)
       }


class Bot:
    """abstract base class for bots"""
    def __init__(self, gamestate):
        logger.debug("Creating bot: {0}".format(self.__class__.__name__))
        self.game = Game(gamestate)
        self.board = self.game.board
        self.me = Hero(gamestate['hero'])
        self.pos = self.me.pos['x'], self.me.pos['y']

        self.possible_moves = [m for m in [stay, north, south, east, west]
                               if self.board.can_step_to(self._move_to(m))]
        logger.debug("possible moves: {0}".format(str(self.possible_moves)))


    def update_state(self, gamestate):  # duplicates constructor for now, but this can likely be made more efficient
        logger.debug("updating with new game state")
        self.game = Game(gamestate)
        self.board = self.game.board
        self.me = Hero(gamestate['hero'])
        self.pos = self.me.pos['x'], self.me.pos['y']

        self.possible_moves = [m for m in [stay, north, south, east, west]
                               if self.board.can_step_to(self._move_to(m))]
        logger.debug("possible moves: {0}".format(str(self.possible_moves)))


    def _move_to(self, direction):
        dir_coords = AIM[direction]
        return (self.pos[0] + dir_coords[0], self.pos[1] + dir_coords[1])

    def move(self, state):
        raise NotImplementedError

    ### Functions to locate interesting things on the board

    def nearest_mine_location(self):
        return sorted([i for i in self.game.mines_locs.keys()], key=(lambda x: ai.manhattan(self.pos, x)))[0]

    def nearest_others_mine_location(self):
        mines = [i for i in self.game.mines_locs.keys() if self.game.mines_locs[i] != str(self.me.heroId)] # heroId stored as int, mine owner as string
        return sorted(mines, key=(lambda x: ai.manhattan(self.pos, x)))[0]


    def nearest_tavern_location(self):
        return sorted(self.game.taverns_locs, key=(lambda x: ai.manhattan(self.pos, x)))[0]

class RandomBot(Bot):
    def move(self, state):
        game = Game(state)
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return random.choice(dirs)

class NewRandomBot(Bot):
    """ moves in a random direction each turn, but it doesn't try to move
        somewhere impossible
    """
    def move(self, state):
        moves = [east, west, north, south]
        random.shuffle(moves)
        game = Game(state)
        while True:
            next_move = moves.pop()
            new_loc = game.board.to(game.my_intpos, next_move)
            if not game.board.is_wall(new_loc):
                return next_move

class AStarBot(Bot):
    def __init__(self, gamestate):
        Bot.__init__(self, gamestate)
        self.goals = itertools.cycle([self.nearest_others_mine_location,
                                      self.nearest_tavern_location])
        self.path = []
    def move(self, state):
        if self.path == []: # no current path
            next_goal = next(self.goals)
            self.path = ai.astar(self.pos, next_goal(), self.game.board.is_passable)
        logger.debug("Path: %s" % str(self.path))
        return self.path.pop(0)
