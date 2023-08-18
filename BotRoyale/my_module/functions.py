"""A collection of functions for doing my project."""
import random
import string
import numpy as np
from time import sleep
from IPython.display import clear_output

def add_lists(list_1, list_2):
    #Adds the values of each corresponding entry of two inputted lists together into one list
    #Taken from A4
    output=[]
    for i1, i2 in zip(list_1, list_2):
        output.append(i1+i2)
    return output

def check_touching_wall(bot_position, grid, wall_char=45):
    #Checks to see if a bot's position is on top of a wall
    #NOTE: logically, this function is flipped in that it will return False if a bot is touching a wall and vice versa
    if ord(grid[bot_position[0], bot_position[1]])==wall_char:
        return False
    else:
        return True

def check_bounds(position, size):
    #Checks to see if a bot's position is out of bounds of a square playgrid of a certain size
    #Taken from A4
    for i in position:
        if i<0 or i>=size:
            return False
    return True

def check_touching_bots(bot, bots):
    #Checks to see if a bot is on top of any of the bots within a list
    for other_bot in bots:
        if bots.index(bot) != bots.index(other_bot):
            if bot.position == other_bot.position:
                return True
    return False

def clear_bots(bots):
    #Function to clear out any bots in a list that have died (see bot_royale) and
    #generate a new list of only bots that are alive
    living_bots=[]
    for bot in bots:
        if bot.alive==True:
            living_bots.append(bot)
    return living_bots



def generate_walls(grid_array, wall_char=45, rand=False, H=False, plus=False):
    '''Takes an array grid and returns a new array with walls generated based on which preset is selected.
    
    Parameters
    ----------
    grid_array : numpy array
        Original array to be modified
    wall_char : int, optional
        ASCII value for walls to have. Default = 45
        NOTE: changing this will interfere with the rest of the project's functionality
    rand, H, plus : bool, optional
        Change any one of these to true to generate walls in these respective formations
    '''
    new_array=grid_array
    
    #Randomly generates walls on all locations besides those on the edge
    if rand==True:
        for row in range(1,grid_array.shape[0]-1):
            for col in range(1,grid_array.shape[1]-1):
                if random.random() < 0.35:
                    new_array[row, col]=chr(wall_char)
    
    #Generates walls in an H formation, scaling to the size of the given grid
    #NOTE: to work properly, grid size must be greater than 5
    elif H==True:
        mag=round(grid_array.shape[0]/10)
        for row in range(0,round(grid_array.shape[0]/2+0.25)-mag):
            for col in range(round(mag*1.6),grid_array.shape[1]-round(mag*1.6)):
                new_array[row, col]=chr(wall_char)
        for row in range(round(grid_array.shape[0]/2-0.25)+mag, grid_array.shape[0]):
            for col in range(round(mag*1.6), grid_array.shape[1]-round(mag*1.6)):
                new_array[row, col]=chr(wall_char)
    
    #Generates walls in a + formation, scaling to the size of the given grid.  Also leave the outline free from walls
    #NOTE: to work properly, grid size must be greater than 4
    elif plus==True:
        mag=round(grid_array.shape[0]/10*1.35)
        for row in range(1,round(grid_array.shape[0]/2+0.25)-mag):
            for col in range(1,round(grid_array.shape[0]/2+0.25)-mag):
                new_array[row, col]=chr(wall_char)
            for col in range(round(grid_array.shape[0]/2-0.25)+mag, grid_array.shape[0]-1):
                new_array[row, col]=chr(wall_char)
        for row in range(round(grid_array.shape[0]/2-0.25)+mag, grid_array.shape[0]-1):
            for col in range(1,round(grid_array.shape[0]/2+0.25)-mag):
                new_array[row, col]=chr(wall_char)
            for col in range(round(grid_array.shape[0]/2-0.25)+mag, grid_array.shape[0]-1):
                new_array[row, col]=chr(wall_char)
                
    return new_array


def play_board_revised(bots, n_iter = 25, grid_size = 20, sleep_time = 0.3, walls=False):
    # A revised version of play_board from the artificial agents assignment (A4)
    # Added functionality with walls, updated the grid to be a numpy array for increased conveinience, and
    # updated it to accomodate for bots with different start positions
    
    """Runs a list of bots across a board.
    
    Parameters
    ----------
    bots : Bot() type or list of Bot() type
        One or more bots to be be played on the board
    n_iter : int, optional
        Number of turns to play on the board. default = 25
    grid_size : int, optional
        Board size. default = 20
    sleep_time : float, optional
        Amount of time to pause between turns. default = 0.3.
    walls : str, optional
        Choose whether the play grid is to have walls of not. default (IS A BOOL) = False.
        To generate walls, must set walls to one of the preset styles as a string.
        Current styles include: 'rand', 'H', and 'plus'
    """
    
    # If input is a single bot, put it in a list so that procedures work
    if not isinstance(bots, list):
        bots = [bots]
    # Raise value error if no bots in list
    if len(bots)==0:
        raise ValueError('Must include at least 1 bot!')
    
    #Generate the play grid as a numpy array and adds walls if a preset variation is inputted
    grid_array_old = np.char.array(['.']*grid_size**2).reshape((grid_size,grid_size))
    if walls!=False:
        if walls=='rand':
            grid_array_old = generate_walls(grid_array_old, rand=True)
        elif walls=='H':
            grid_array_old = generate_walls(grid_array_old, H=True)
        elif walls=='plus':
            grid_array_old = generate_walls(grid_array_old, plus=True)
        else:
            print('In order to generate walls, must choose a preset generation style.')
            print('Options currently include: \'rand\', \'H\', and \'plus\'')
            print('Will now run function with no walls.')
            sleep(3)
    
    # Update each bot to know about the grid_size they are on
    for bot in bots:
        bot.grid_size = grid_size

    # If any bots' start pos is out of bounds or in a wall, reset start pos to [0,0]
    for bot in bots:
        if not check_bounds(bot.position, grid_size):
            bot.position = [0,0]
        if not check_touching_wall(bot.position, grid_array_old):
            bot.position = [0,0]

    for it in range(n_iter):
        # Create the grid
        grid_array_new = np.char.array([])
        for row in range(0,grid_array_old.shape[0]):
            for col in range(0,grid_array_old.shape[1]):
                grid_array_new = np.append(grid_array_new, grid_array_old[row, col])
        grid_array_new = grid_array_new.reshape((grid_size, grid_size))
        
        # Add bot(s) to the grid
        for bot in bots:
            grid_array_new[bot.position[0],bot.position[1]] = bot.character    

        # Update bot grids to be the same as the current grid
        for bot in bots:
            bot.grid = grid_array_new
        
        # Clear the previous iteration, print the new grid (as a string), and wait
        clear_output(True)
        print('\n'.join([' '.join(row) for row in grid_array_new]))
        sleep(sleep_time)

        # Update bot position(s) for next turn
        for bot in bots:
            bot.move()


def bot_royale(bots, grid_size = 15, sleep_time = 0.2, walls=False):
    """Pits a list of at least 3 bots against each other in a battle royale type gamemode.
    Also adapted from play_board() in A4, but has been changed significantly to the point where
    I would consider it more original than not.
    
    Parameters
    ----------
    bots : Bot() type or list of Bot() type
        Three or more bots to be be played on the board.  Will raise an error if less than three bots provided.
        NOTE: works best with an odd number of bots so that a there is an individual winner
    grid_size : int, optional
        Board size. default = 10
        Be cautious with larger sizes as the games can get pretty long if the board is too big.
    sleep_time : float, optional
        Amount of time to pause between turns. default = 0.2
    walls : str, optional
        Choose whether the play grid is to have walls of not. default (IS A BOOL) = False.
        To generate walls, must set walls to one of the preset styles as a string.
        Current styles include: 'rand', 'H', and 'plus'
    """
    
    #In the instance of a single bot, puts it into a list so that the next statement works effectively
    if not isinstance(bots, list):
        bots = [bots]
    #Raises an error if there are too few bots to actually compete against each other
    if len(bots)<3:
        raise ValueError('Must have at least 3 bots to begin a battle royale.')
    
    
    #Generate the play grid as a numpy array and adds walls if a preset variation is inputted
    grid_array_old = np.char.array(['.']*grid_size**2).reshape((grid_size,grid_size))
    if walls!=False:
        if walls=='rand':
            grid_array_old = generate_walls(grid_array_old, rand=True)
        elif walls=='H':
            grid_array_old = generate_walls(grid_array_old, H=True)
        elif walls=='plus':
            grid_array_old = generate_walls(grid_array_old, plus=True)
        else:
            print('In order to generate walls, must choose a preset generation style.')
            print('Options currently include: \'rand\', \'H\', and \'plus\'')
            print('Will now run function with no walls.')
            sleep(3)
    
    # Update each bot to know about the grid_size they are on
    for bot in bots:
        bot.grid_size = grid_size
        
    #Assign a numeric name to the bots that don't have one
    for bot in bots:
        if bot.name==None:
            bot.name='Bot ' + str(bots.index(bot)+1)

    # Separates the bots' start positions before running the match so that they don't clash with each other immediatelly
    # NOTE: I couldn't get the separations perfect with the H preset, but while the bots aren't maximally separated, it still
    # splits them up relatively effectively.
    if walls=='H':
        separation = grid_size*2/len(bots)
        for bot in bots:
            pos_num = round(separation*(bots.index(bot)))
            if pos_num==0:
                bot.position=[0,0]
            elif pos_num<grid_size:
                bot.position = [pos_num, 0]
            elif pos_num<grid_size*2:
                bot.position = [pos_num-grid_size, grid_size-1]
            elif pos_num==grid_size*2:
                bot.position = [grid_size-1, grid_size-1]
    else:
        separation = grid_size*4/len(bots)
        for bot in bots:
            pos_num = round(separation*(bots.index(bot)))
            if pos_num==0:
                bot.position = [0,0]
            elif pos_num<grid_size:
                bot.position = [pos_num, 0]
            elif pos_num<grid_size*2:
                bot.position = [grid_size-1, pos_num-(grid_size)]
            elif pos_num<grid_size*3:
                bot.position = [(grid_size-1)-(pos_num-(grid_size*2)), grid_size-1]
            elif pos_num<grid_size*4:
                bot.position = [0, (grid_size-1)-(pos_num-(grid_size*3))]
            elif pos_num==grid_size*4:
                bot.position = [0, 1]
            
    #Play through the bot royale
    while True:

        # Create the grid
        grid_array_new = np.char.array([])
        for row in range(0,grid_array_old.shape[0]):
            for col in range(0,grid_array_old.shape[1]):
                grid_array_new = np.append(grid_array_new, grid_array_old[row, col])
        grid_array_new = grid_array_new.reshape((grid_size, grid_size))
        
        # Add bot(s) to the grid
        for bot in bots:
            grid_array_new[bot.position[0],bot.position[1]] = bot.character    

        # Update bot grids to be the same as the current grid
        for bot in bots:
            bot.grid = grid_array_new
        
        # Clear the previous iteration, print the new grid (as a string), and wait
        clear_output(True)
        print('\n'.join([' '.join(row) for row in grid_array_new]))
        sleep(sleep_time)
        
        #Account for a tie
        if len(bots)==0:
            print("It's a tie between "+' and '.join([bot.name for bot in old_bots])+'!')
            break
        #Announce the winner
        elif len(bots)==1:
            print(bots[0].name, 'won!')
            break
        
        # Update bot position(s) for next turn
        for bot in bots:
            bot.move()
        
        #Check to see if any bots are in contact with each other
        for bot in bots:
            if check_touching_bots(bot, bots):
                bot.alive = False
        
        #Kill off the dead bots
        old_bots=bots
        bots=clear_bots(bots)