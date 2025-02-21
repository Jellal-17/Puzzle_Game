import random
from game_eval import *


# Implement a game version with a random controller
class RandGame(Game):
    def __init__(self):
        super().__init__()

    # Initialization: called only once when activating automated mode
    def initialize_controller(self):
        # Nothing to do in the random controller
        return

    # Control system, called at every iteration
    def controller(self):
        # Select a random agent id
        i = random.randrange(len(self.agents))
        # Select a random action
        d = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
        # Activate player 
        self.active_agent = i
        # Apply action. The function will check if the action is possible
        self.move_player(self.agents[i],d[0],d[1])


if __name__ == "__main__":
    mygame = RandGame()
    mygame.main()
