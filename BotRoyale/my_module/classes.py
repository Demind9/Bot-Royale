"""
Classes to be used in the project - All of these classes have been adapted from A4

- Bot is the generic parent class that initializes all of the bot vars used throughout the program.
- WanderBot is a bot that has the ability to randomly wander. Upon wandering, it updates its position to the first
valid position that it wanders to
- ExploreBot has the same functionality as WanderBot, except that it preferences spaces that it has not yet wandered to
- TeleportBot is a WanderBot that also has the ability to randomly telepot every now and then.  Futhermore, if it teleports
to an enclosed space (as might happen with random wall generation), it immediately teleports to a new space.
"""
import random
from my_module.functions import check_bounds, add_lists, check_touching_wall

class Bot():
    def __init__(self, character=8982, startpos=[0,0], name=None):
        self.character = chr(character)
        self.position = startpos
        self.name = name
        self.moves = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        self.grid_size = None
        self.grid = None
        self.alive = True
        
class WanderBot(Bot):
    def __init__(self, character=8982, startpos=[0,0], name=None):
        super().__init__(character, startpos, name)
    def wander(self):
        has_new_pos=False
        while not has_new_pos:
            move=random.choice(self.moves)
            new_pos=add_lists(self.position, move)
            has_new_pos = check_bounds(new_pos, self.grid_size) and check_touching_wall(new_pos, self.grid)
        return new_pos
    def move(self):
        self.position=self.wander()
        
class ExploreBot(Bot):
    def __init__(self, character=8982, startpos=[0,0], name=None, move_prob=0.75):
        super().__init__(character, startpos, name)
        self.move_prob=move_prob
        self.last_move=None
    def biased_choice(self):
        move=None
        if self.last_move != None:
            if random.random()<self.move_prob:
                move=self.last_move
        if move == None:
            move=random.choice(self.moves)
        return move
    def explore(self):
        has_new_pos=False
        while not has_new_pos:
            move=self.biased_choice()
            new_pos=add_lists(self.position, move)
            has_new_pos = check_bounds(new_pos, self.grid_size) and check_touching_wall(new_pos, self.grid)
            self.last_move=move
        return new_pos
    def move(self):
        self.position=self.explore()
        
class TeleportBot(WanderBot):
    def __init__(self, character=8982, startpos=[0,0], name=None, tele_prob=0.2):
        super().__init__(character, startpos, name)
        self.tele_prob=tele_prob
    def teleport(self):
        has_new_pos=False
        while not has_new_pos:
            new_pos=[random.choice(range(0,self.grid_size)),random.choice(range(0,self.grid_size))]
            has_new_pos=check_touching_wall(new_pos, self.grid) and new_pos != self.position
        return new_pos
    def move(self):
        if random.random()<self.tele_prob:
            self.position=self.teleport()
        else:
            #in the case that it is blocked in by walls or the end of the grid, teleports immediatelly
            free_spaces=0
            for move in self.moves:
                if check_bounds(add_lists(self.position, move), self.grid_size):
                    if check_touching_wall(add_lists(self.position, move), self.grid):
                        free_spaces+=1
            if free_spaces==0:
                self.position = self.teleport()
            else:
                self.position=self.wander()