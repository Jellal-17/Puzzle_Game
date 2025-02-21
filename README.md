# Grid Optimization Puzzle Game

A grid-based puzzle game implemented in Python using Pygame. In this game, multiple agents navigate a 5x5 grid, overcome obstacles, and perform actions (such as acquiring colors and opening doors) to reach designated target positions. The project demonstrates the use of classical search and planning algorithms—BFS, DFS, and A*—to automatically solve the puzzle, as well as a random controller for baseline testing.

## Project Overview

The game simulates a grid environment where three agents must:
- **Acquire Target Colors:** Each agent starts without its target color. Stepping on a designated color tile changes the agent's color to its target.
- **Activate a Door:** Agents can trigger a door switch to open a blocked passage.
- **Reach Target Positions:** Once the agents have the correct colors, they must navigate to their respective target positions.

The game offers both manual play and automated control:
- **Manual Mode:** Use keyboard controls to move agents.
- **Automated Mode:** Run the solution that employs search algorithms (BFS, DFS, or A*) to compute the optimal path.
- **Random Controller:** Moves agents randomly for testing or demonstration purposes.

## File Structure

- **`game_eval.py`**  
  Contains the core game logic, environment setup, and rendering using Pygame. It defines the grid, obstacles, door switch, color tiles, and agents.

- **`solution.py`**  
  Implements an automated controller that uses search algorithms (BFS, DFS, A*) to plan a sequence of moves leading to the goal state. This file extends the game logic from `game_eval.py` to enable algorithm-based control.

- **`sol_random.py`**  
  Provides a simple random controller that moves agents randomly within the grid. This serves as a baseline for comparing against the more strategic planning algorithms.

## Requirements

- **Python 3.x**
- **Pygame**

Install Pygame via pip:

```bash
pip install pygame
```
## How to Run
### Manual Mode
Run the game manually to control the agents with the keyboard:

```bash
python game_eval.py
```

### Controls:
- **Arrow Keys**: Move the active agent.

- **Tab**: Switch between agents.

- **Escape**: Quit the game.

- **A**: Toggle automatic mnode.

## Automated Mode(Planned Algorithms)
To run the game using an automated controller with planning:

```bash
python solution.py
```

You can choose the algorithm by modifying the parameter in the ```Solution``` constructor. Options include:
- **```'BFS'```**
- **```'DFS'```**
- **```'A-star'```**

When automatic mode is enabled (press ```A``` during the game), the selected algorithm will plan the sequence of moves to solve the puzzle.

### Random Controller
To run the game with a random movement controller:

```bash
python sol_random.py
```
This version moves agents randomly and can be used for testing or demonstration.

## Game Mechanics
- **Grid Layout:**

  The game is set on a 5x5 grid where each cell represents a position. Some cells contain obstacles (impassable), a color tile (to acquire the target color), or a door switch (to open a blocked path).

- **Agents:**

  There are three agents starting at the left side of the grid. Their goals are to acquire specific colors and reach designated target positions on the right side.

- **Obstacles and Special Tiles:**

  - **Obstacles:** Represented by impassable cells.
  - **Color Tile (Value 2):** Stepping on these changes an agent’s color to its target color.
  - **Door Switch (Value 3):** Activating this opens a door in the grid, allowing agents to pass through previously blocked cells.

- **Objective:**

  The game is completed when all agents have acquired their target colors and reached their target positions.

## Project Description
  This project is an exploration of pathfinding and planning algorithms applied to a grid-based puzzle game. By integrating classical algorithms such as BFS, DFS, and A*, the project not only provides an engaging game but also serves as an educational example of how AI planning techniques can be used to solve complex navigation problems. Whether played manually or through automated controllers, the game offers insights into both algorithmic problem solving and game development with Pygame.

## License
 MIT License

## Acknowledgements
This project was developed as a learning tool to explore search algorithms and AI planning in a grid environment.

Built using [Pygame](https://www.pygame.org/news).
