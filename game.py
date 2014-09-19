import re

import logging
logger = logging.getLogger(__name__)

import util

TAVERN = 0
AIR = -1
WALL = -2

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

class HeroTile(object):
    def __init__(self, id):
        self.id = id

class MineTile(object):
    def __init__(self, heroId = None):
        self.heroId = heroId

class Game(object):
    """A model of the entire game state.  This is instantiated once per game.
    """
    def __init__(self, state):
        self.state = state
        self.board = Board(state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]
        self.me = Hero(state['hero'])
        self.my_intpos = self.me.pos['x'], self.me.pos['y']
        self.mines_locs = {}
        self.heroes_locs = {}
        self.taverns_locs = set([])
        self.me = Hero(state['hero'])
        self.my_intpos = self.me.pos['x'], self.me.pos['y']
        for row in range(len(self.board.tiles)):
            for col in range(len(self.board.tiles[row])):
                obj = self.board.tiles[row][col]
                if isinstance(obj, MineTile):
                    self.mines_locs[(row, col)] = obj.heroId
                elif isinstance(obj, HeroTile):
                    self.heroes_locs[(row, col)] = obj.id
                elif (obj == TAVERN):
                    self.taverns_locs.add((row, col))

class Board(object):
    def __parseTile(self, str):
        if (str == '  '):
            return AIR
        if (str == '##'):
            return WALL
        if (str == '[]'):
            return TAVERN
        match = re.match('\$([-0-9])', str)
        if (match):
            return MineTile(match.group(1))
        match = re.match('\@([0-9])', str)
        if (match):
            return HeroTile(match.group(1))

    def __parseTiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]

        return [[self.__parseTile(x) for x in xs] for xs in matrix]

    def __init__(self, board):
        self.size = board['size']
        self.tiles = self.__parseTiles(board['tiles'])

    def is_passable(self, loc):
        'true if can walk through'
        x, y = loc
        if (x > self.size-1 or x < 0 or
            y > self.size-1 or y < 0): return False
        pos = self.tiles[x][y]
        return (pos != WALL) or (pos != TAVERN) or not isinstance(pos, MineTile)

    def is_wall(self, loc):
        'true if loc is wall'
        x, y = loc
        pos = self.tiles[x][y]
        return pos == WALL

    def is_tavern(self, loc):
        'true if loc is tavern'
        x, y = loc
        pos = self.tiles[x][y]
        return pos == TAVERN

    def is_mine(self, loc):
        'true if loc is mine'
        x, y = loc
        pos = self.tiles[x][y]
        return isinstance(pos, MineTile)

    def can_step_to(self, loc):
        """" true if can move in this direction

        This differs from is_passable because it returns True for taverns and mines,
        because stepping to these is legal, even though the hero doesn't move.
        """
        x, y = loc
        return self.is_passable(loc) or self.is_tavern(loc) or self.is_mine(loc)

    def is_wall(self, loc):
        'true if loc is wall'
        x, y = loc
        pos = self.tiles[x][y]
        return pos == WALL

    def is_tavern(self, loc):
        'true if loc is tavern'
        x, y = loc
        pos = self.tiles[x][y]
        return pos == TAVERN

    def is_mine(self, loc):
        'true if loc is mine'
        x, y = loc
        pos = self.tiles[x][y]
        return isinstance(pos, MineTile)


class Hero(object):
    def __init__(self, hero):
        if hero['crashed'] == 'true':
            logger.fatal("Hero crashed.")
        self.heroId = hero['id']
        self.name = hero['name']
        self.pos = hero['pos']
        self.life = hero['life']
        self.gold = hero['gold']
