"""
Tests for my functions.
"""

from my_module.functions import generate_walls, play_board_revised, check_touching_wall, check_touching_bots, clear_bots
from my_module.classes import Bot, WanderBot, ExploreBot, TeleportBot
import numpy as np
from time import sleep
from IPython.display import clear_output


#Tests the generation of walls and allows user to see how each variation turns out for a given size (default size=25)
#*Named tests before since it is not supposed to be tested with pytest.
#Instead to be tested in the notebook so user can see the outputs.
def tests_generate_walls(walls, grid_size=25):
    grid_array = np.char.array(['.']*grid_size**2).reshape((grid_size,grid_size))
    if walls=='rand':
        grid_array = generate_walls(grid_array, rand=True)
    elif walls=='H':
        grid_array = generate_walls(grid_array, H=True)
    elif walls=='plus':
        grid_array = generate_walls(grid_array, plus=True)
    else:
        raise ValueError('Please choose one of the wall presets')
    print('\n'.join([' '.join(row) for row in grid_array]))
    
#Creates a 3x3 grid with all enclosed spaces to test+show whether the teleport bot is properly teleporting when it is locked in
#Specifically tests the teleport+move functions within the TeleportBot class
#*Named tests before since it is not supposed to be tested with pytest.
#Instead to be tested in the notebook so user can see the outputs.
def tests_teleport_when_enclosed(n_iter=25, sleep_time=0.2):
    bot=TeleportBot(character=5782)
    grid_old=np.char.array([['.','-','.'], ['-','.','-'], ['.','-','.']])
    bot.grid_size=3
    bot.grid=grid_old
    for i in range (0,n_iter):
        grid_new = np.char.array([])
        for row in range(0,grid_old.shape[0]):
            for col in range(0,grid_old.shape[1]):
                grid_new = np.append(grid_new, grid_old[row, col])
        grid_new = grid_new.reshape((3, 3))
        
        grid_new[bot.position[0], bot.position[1]] = bot.character
        print('\n'.join([' '.join(row) for row in grid_new]))
        sleep(sleep_time)
        clear_output(True)
        bot.move()

#Method to test play_board_revised function
def test_play_board_revised():
    #Tests that start positions are set back to zero in the event of a list of bots with illegal start positions
    bots=[Bot(character=8982, startpos=[-1, 4]), WanderBot(character=1078, startpos=[0,10]), ExploreBot(character=1127,startpos=[40,40])]
    play_board_revised(bots, n_iter=0, walls='H')
    for bot in bots:
        assert bot.position == [0,0]
    
    #Tests that function won't work with an empty list for bots
    try:
        play_board_revised([], n_iter=0)
    except ValueError:
        assert True
        
#Tests if check_touching_wall works properly
def test_check_touching_wall():
    grid=np.char.array([['.','-','.'], ['-','.','-'], ['.','-','.']])
    bots=[Bot(startpos=[0,0]), Bot(startpos=[0,1])]
    assert check_touching_wall(bots[0].position, grid)
    assert not check_touching_wall(bots[1].position, grid)

#Tests if check_touching_bots works properly
def test_check_touching_bots():
    bots=[Bot(startpos=[0,0]), Bot(startpos=[0,1]), WanderBot(startpos=[0,0])]
    assert check_touching_bots(bots[0], bots)
    assert not check_touching_bots(bots[1], bots)
    assert check_touching_bots(bots[2], bots)
    
#Tests if the clear_bots function works properly
def test_clear_bots():
    bots=[Bot(name='Gonna die'), Bot(name='Lives'), WanderBot(name='Dead'), TeleportBot(name='Alive')]
    bots[0].alive=False
    bots[2].alive=False
    bots=clear_bots(bots)
    assert bots[0].name=='Lives'
    assert bots[1].name=='Alive'
    assert len(bots)==2