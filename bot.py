import random
import time
from collections import defaultdict

import logging
logger = logging.getLogger(__name__)
from game import Game, Hero


class Bot:
    """ abstract base class for bots, which may someday contain shared functionality?"""
    def move(self, state):
        raise NotImplementedError

class OutOfBoundsBot(Bot):
    def move(self, state):
        game = Game(state)
        return 'North'

class RandomBot(Bot):
    """ a bot that moves in a random direction every turn"""
    def move(self, state):
        return random.choice(['East','West','North','South'])


## the rest of these bots currently (11 Sept) suffer from the same bug: they don't know
#  not to try to move off the edge of the map.  Postponed the easy fix in order to contemplate
#  improvements to the world model.

class RandomBot2(Bot):
    """ a bot that moves in a random direction every turn, but doesn't try to
    move somewhere impassible """

    def move(self, state):
        moves = ['East', 'West', 'North', 'South']
        random.shuffle(moves)
        game = Game(state)
        while True:
            next_move = moves.pop()
            new_loc = game.board.to(game.my_intpos, next_move)
            if not game.board.is_wall(new_loc):
                return next_move

class RandomBot3(Bot):
    """ a bot that moves in a random direction every turn, but doesn't try to move
    somewhere impassible, and prefers not to immediately backtrack """
    def __init__(self):
        self.last_move = 'North'

    def move(self, state):
        moves = [i for i in ['East', 'West', 'North', 'South'] if i != self.last_move]
        random.shuffle(moves)
        moves = [self.last_move] + moves
        logger.debug("moves = %s" % str(moves))
        game = Game(state)
        while True:
            next_move = moves.pop()
            logger.debug("next move = %s" % next_move)
            new_loc = game.board.to(game.my_intpos, next_move)
            if not game.board.is_wall(new_loc):
                self.last_move = next_move
                return next_move

class RandomBot4(Bot):
    """ RandomBot3 but remember where you've been and prefer not to go there again. """
    def __init__(self):
        self.been_there = defaultdict(lambda: False)

    def move(self, state):
        game = Game(state)
        self.been_there[game.my_intpos] = True
        north = 'North', game.board.to(game.my_intpos, 'North')
        south = 'South', game.board.to(game.my_intpos, 'South')
        east =  'East', game.board.to(game.my_intpos, 'East')
        west = 'West', game.board.to(game.my_intpos, 'West')
        moves = [north, south, east, west]
        not_been = [i for i in moves if self.been_there[i[1]]]
        been = [i for i in moves if not self.been_there[i[1]]]

        random.shuffle(not_been)
        random.shuffle(been)
        moves = [x for x in been + not_been if  not game.board.is_wall(x[1]) ]
        logger.debug("moves: %s" % str(moves))
        while True:
            next_move = moves.pop()
            if not game.board.is_wall(next_move[1]):
                logger.debug("next move = %s" % str(next_move))
                return next_move[0]



class NannanBot(Bot):
    def __init__(self):
        self.last_move = None
        self.last_move_reason = None
        self.move_dirs = ['East','West','North','South']
        #stay = ['Stay']

    def move(self, state):
        self.last_move, self.last_move_reason = self._move(state)
        logger.info("moving %s because %s" % (self.last_move, self.last_move_reason))
        return self.last_move

    def _move(self, state):
        game = Game(state)

        def _can_move(my_pos, dir):
            """ if I'm in my_pos, can I move in dir?"""
            new_loc = game.board.to(my_pos, dir)
            return not game.board.is_wall(new_loc)


        me = game.me
        me.intpos = me.pos['x'], me.pos['y']
        possible_moves = [d for d in self.move_dirs if _can_move(me.intpos, d)]
        logger.info("can move from %s to %s" % (str(me.intpos), str(possible_moves)))

        for direction in possible_moves:
            next_coords = game.board.to(me.intpos, direction)
            if game.mines_locs.get(game.board.to(me.intpos, direction)) not in [str(me.heroId), None]:
                return direction, "mine"
            if self.last_move != direction and game.board.to(me.intpos, direction) in game.taverns_locs and me.life < 80:
                return direction, "tavern"


        next_dir = possible_moves.pop()

        while(1):
            next_move = game.board.to(me.intpos, next_dir)
            if game.board.passable(next_move):
                logger.info("turn %s/%s: %s -> %s" % (state['game']['turn'], state['game']['maxTurns'], str(me.intpos), str(next_dir)))
                self.last_move = next_dir
                return next_dir, ""
            else:
                next_dir = possible_moves.pop()
