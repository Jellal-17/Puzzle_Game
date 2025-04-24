# MIT License

# Copyright (c) 2025 Sathvik Kadimisetty

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import pygame as pg

TITLE = "Grid"
TILES_HORIZONTAL = 5
TILES_VERTICAL = 5
TILE_SIZE = 80
WINDOW_WIDTH = TILES_HORIZONTAL * TILE_SIZE
WINDOW_HEIGHT = TILES_VERTICAL * TILE_SIZE


# Generic class implementing an agent in our game. 
# An agent is defined by its position (x,y) in the 5x5 grid and its color.
# An agent can also be active, but this is mostly for display when controlling with the keyboard.
class Player:
    def __init__(self, surface, x = 0, y = 0):
        self.surface = surface
        self.pos = (x, y)
        self.active = False
        self.color = (255,255,255)

    def draw(self):
        pg.draw.circle(self.surface, self.color, 
                (self.pos[0]*TILE_SIZE+TILE_SIZE//2,self.pos[1]*TILE_SIZE+TILE_SIZE//2), 40)
        if self.active:
            pg.draw.circle(self.surface, (0,0,0), 
                    (self.pos[0]*TILE_SIZE+TILE_SIZE//2,self.pos[1]*TILE_SIZE+TILE_SIZE//2), 5)

    # Move the agent to a target position defined by a mouse click in the window
    def move(self, target):
        # x = (80 * (target[0] // 80)) + 40
        # y = (80 * (target[1] // 80)) + 40
        x = target[0] // 80
        y = target[1] // 80

        self.pos = (x, y)

    # Move the agent to a cell in the grid cell=(2,2) is the center cell of the 5x5 grid. 
    def moveto(self, cell):
        self.pos = cell

    # Set the agent color, as a tuple, for instance (255,255,255) for white
    def set_color(self, c):
        self.color = c


# Definition of a "Game" environment.
# The game includes 3 agents stored in the self.agents list and a world definition.
# The world is a 5x5 grid, with obstacles marked as 1, and two special cells marked as 2 and 3. 
# When an agent passes on the cell marked with a 2, its color is set to its target color. 
# When an agent passed on the cell marked with a 3, it opens a door in the obstacle wall. 
# The door position is stored in self.door.
# Agents can only move up, down, left or right. 
# The game is complete when all agents have reached their target position after having acquired their target color. 
class Game:
    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.surface = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.loop = True
        self.agents = [Player(self.surface,0,0),Player(self.surface,0,2),Player(self.surface,0,4)]
        self.auto = False
        self.active_agent = 0
        self.target_color = [(255,0,0),(0,255,0),(0,0,255)]
        self.target_position = [(4,0),(4,2),(4,4)]
        self.door = (3,2)
        self.world=[
                [0,0,0,1,0],
                [0,0,2,1,0],
                [0,0,0,1,0],
                [0,0,3,1,0],
                [0,0,0,1,0]]


    # Main loop
    def main(self):
        while self.loop:
            self.grid_loop()
        pg.quit()


    # Draw a square tile
    def draw_tile(self,x,y, color):
        pg.draw.rect( self.surface, color,
                (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Implement the game logic: apply the door switch and the color switch and make sure the 
    # active agent is marked active. 
    def game_logic(self):
        print([p.pos for p in self.agents])
        for i,p in enumerate(self.agents):
            p.active = False
            if self.world[p.pos[1]][p.pos[0]] == 3: # Door switch
                self.world[self.door[1]][self.door[0]] = 0
            elif self.world[p.pos[1]][p.pos[0]] == 2: # Color switch
                p.set_color(self.target_color[i])
        self.agents[self.active_agent].active = True

    # Test is the game is terminated, i.e. all agents have reached their target position and have 
    # acquired their target color
    def game_complete(self):
        all_pos = all([p.pos==t for p,t in zip(self.agents,self.target_position)])
        all_color = all([p.color==c for p,c in zip(self.agents,self.target_color)])
        return all_pos and all_color


    # Test if a move (dx,dy) from position s is possible with the current world configuration.
    # Returns (authorized, newx, newy) where authorized is true if the movement is feasible (i.e. 
    # stays in the grid and does not collide with an obstacle) given the provided world.
    # (newx,newy) is the new position resulting from the action (dx,dy).
    def test_move(self,s,dx,dy,world):
        if s[0]+dx < 0:
            return (False,s[0],s[1])
        if s[0]+dx >= TILES_HORIZONTAL:
            return (False,s[0],s[1])
        if s[1]+dy < 0:
            return (False,s[0],s[1])
        if s[1]+dy >= TILES_VERTICAL:
            return (False,s[0],s[1])
        if world[s[1]+dy][s[0]+dx]==1:
            return (False,s[0],s[1])
        return (True,s[0]+dx,s[1]+dy)

    # Move the player p by (dx,dy) if possible
    def move_player(self,p,dx,dy):
        (authorized,newx,newy) = self.test_move(p.pos,dx,dy,self.world)
        if authorized:
            p.moveto((newx,newy))


    # Function called once when automatic control is activated. This would be the right place 
    # to run a planner for instance
    def initialize_controller(self):
        return

    # Function called at every step of the loop once automatic control is activated
    def controller(self):
        return


    # Main loop for display and game logic 
    def grid_loop(self):
        # Apply the controller if we are in automatic mode
        if self.auto:
            self.controller()
        # Apply the game logic
        self.game_logic()
        # Check if the game is finished
        if self.game_complete():
            print("COMPLETED. YOU WIN !!!")
            self.loop = False

        # Display the world state
        self.surface.fill((0, 0, 0))
        for x in range(TILES_HORIZONTAL):
            for y in range(TILES_VERTICAL):
                if self.world[y][x]==1:
                    self.draw_tile(x,y,(128,128,128))
                elif self.world[y][x]==2:
                    self.draw_tile(x,y,(128,128,0))
                elif self.world[y][x]==3:
                    self.draw_tile(x,y,(128,0,128))
                elif ((x+y)&1):
                    self.draw_tile(x,y,(0,0,0))
                else:
                    self.draw_tile(x,y,(40,40,40))

        # Draw all the agents
        for p in self.agents:
            p.draw()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.loop = False
                if event.key == pg.K_a:
                    # When pressing the key 'A', the game switches to/from automatic mode.
                    # When entering automatic mode, the function initialize_controller is called, once. 
                    self.auto = not self.auto
                    print("Auto mode: " +str(self.auto))
                    if self.auto:
                        self.initialize_controller()
                # Key management in manual mode
                elif event.key == pg.K_UP:
                    self.move_player(self.agents[self.active_agent],0,-1)
                elif event.key == pg.K_DOWN:
                    self.move_player(self.agents[self.active_agent],0,+1)
                elif event.key == pg.K_LEFT:
                    self.move_player(self.agents[self.active_agent],-1,0)
                elif event.key == pg.K_RIGHT:
                    self.move_player(self.agents[self.active_agent],+1,0)
                elif event.key == pg.K_TAB:
                    self.active_agent = (self.active_agent+1)%len(self.agents)
            # elif event.type == pg.MOUSEBUTTONUP:
            #     pos = pg.mouse.get_pos()
            #     self.agents[self.active_agent].move(pos)
        pg.display.update()
        pg.time.wait(100)


if __name__ == "__main__":
    mygame = Game()
    mygame.main()
