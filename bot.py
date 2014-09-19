import random
import time
from game import Game

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

class Bot:
    pass

class RandomBot(Bot):
    def move(self, state):
        game = Game(state)
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return random.choice(dirs)

class RandomBot2(Bot):
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

class FighterBot(Bot):
    def move(self, state):
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)



class SlowBot(Bot):
    def move(self, state):
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        time.sleep(2)
        return choice(dirs)
