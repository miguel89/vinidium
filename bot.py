from random import choice, shuffle
import time

from pprint import pprint, pformat
import logging
logger = logging.getLogger(__name__)
from game import Game, Hero


class Bot:
    pass

class NannanBot(Bot):
    def __init__(self):
        self.last_move = None
        self.last_move_reason = None
        self.printed = False
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
