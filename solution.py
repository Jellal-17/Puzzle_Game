# State can be defined as following
# 1. Positions of each agent: [(x1, y1), (x2, y2), (x3, y3)]
# 2. Colors acquired: track for each agent whether it has reached its target color yet (True/False).
# 3. Door status: whether the door is open or closed (True/False).

# So, (positions, color_states, door_state) is the state representation.

import time
import collections
import heapq
from game_eval import Game


class Solution(Game):
    def __init__(self, algorithm=None):
        super().__init__()
        self.plan = []
        self.initialized = False
        self.algorithm = algorithm

    def initialize_controller(self):
        """
        Called once when we activate automated mode using 'a'.
        This is where we plan our path using BFS.
        """

        if not self.initialized:
            self.initialized = True

            start_time = time.time()

            if self.algorithm == 'DFS':
                self.plan = self.dfs_plan()
            elif self.algorithm == 'A-star':
                self.plan = self.astar_plan()
            elif self.algorithm == 'BFS':
                self.plan = self.bfs_plan()

            end_time = time.time()
            elapsed_time = end_time - start_time

            print(f"{self.algorithm} planning took {elapsed_time:.4f} seconds")

    def controller(self):
        """
        Called at every iteration of the loop.
        """

        if self.plan:
            agent_id, dx, dy = self.plan.pop(0)
            self.active_agent = agent_id
            self.move_player(self.agents[agent_id], dx, dy)

        # If self.plan is empty, we do nothing; eventually the game should end.

    def bfs_plan(self):
        """
        Perform a BFS in the state space and return a list of moves
        (agent_id, dx, dy) that lead to the goal.
        """

        # 1. Construct the initial BFS state from the current environment
        start_positions = tuple(p.pos for p in self.agents)
        start_colors = tuple(self.has_correct_color(i) for i in range(len(self.agents)))
        door_open = self.is_door_open()
        start_state = (start_positions, start_colors, door_open)

        # 2. If the start_state is already a goal, no moves needed
        if self.is_goal_state(start_positions, start_colors):
            return []

        # 3. Initialize the BFS containers
        queue = collections.deque([start_state])
        visited = set([start_state])
        parent = dict()
        parent[start_state] = None  # No predecessor

        # 4. Standard BFS loop
        while queue:
            current_state = queue.popleft()
            current_positions, current_colors, current_door = current_state

            # generate the next states by moving one agent at a time
            for agent_id in range(len(self.agents)):
                for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_state = self.next_state(
                                    current_positions,
                                    current_colors,
                                    current_door,
                                    agent_id,
                                    dx, dy)

                    if next_state is None:
                        # Move not valid or no change
                        continue

                    if next_state not in visited:
                        visited.add(next_state)
                        parent[next_state] = (current_state, agent_id, dx, dy)

                        # check if we've reached the goal
                        next_positions, next_colors, next_door = next_state
                        if self.is_goal_state(next_positions, next_colors):
                            # Reconstruct the path and return it

                            return self.reconstruct_path(parent, next_state)

                        queue.append(next_state)

        # No path found
        return []

    def dfs_plan(self):
        """
        Depth-first search for a valid sequence of moves
        to get all agents to their target position & color.
        """
        start_positions = tuple(p.pos for p in self.agents)
        start_colors = tuple(self.has_correct_color(i) for i in range(len(self.agents)))
        start_door = self.is_door_open()
        start_state = (start_positions, start_colors, start_door)

        # Quick check if already at goal
        if self.is_goal_state(start_positions, start_colors):
            return []

        stack = [start_state]
        visited = set([start_state])
        parent = {start_state: None}  # For path reconstruction

        # Classic DFS loop using a stack
        while stack:
            current_state = stack.pop()
            positions, colors, door_open = current_state

            # Generate successors by moving one agent in one of four directions
            for agent_id in range(len(positions)):
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_state = self.next_state(positions, colors, door_open, agent_id, dx, dy)
                    if not next_state:
                        continue  # Invalid or same as current

                    if next_state not in visited:
                        visited.add(next_state)
                        parent[next_state] = (current_state, agent_id, dx, dy)

                        (next_positions, next_colors, next_door) = next_state
                        # Check for goal
                        if self.is_goal_state(next_positions, next_colors):
                            return self.reconstruct_path(parent, next_state)
                        stack.append(next_state)

        # No path found
        return []

    def astar_plan(self):
        start_positions = tuple(p.pos for p in self.agents)
        start_colors = tuple(self.has_correct_color(i) for i in range(len(self.agents)))
        start_door = self.is_door_open()
        start_state = (start_positions, start_colors, start_door)

        if self.is_goal_state(start_positions, start_colors):
            return []

        # Priority queue items are (f_score, g_score, state)
        # and a parent dict for reconstruction
        open_list = []
        heapq.heappush(open_list, (0, 0, start_state))

        came_from = {start_state: None}  # For path reconstruction
        g_score = {start_state: 0}     # g-score

        while open_list:
            # Pop the state with the lowest f = g + h
            _, g, current_state = heapq.heappop(open_list)
            (positions, colors, door_open) = current_state

            # If goal, reconstruct path
            if self.is_goal_state(positions, colors):
                return self.reconstruct_path(came_from, current_state)

            # Explore neighbors
            for agent_id in range(len(self.agents)):
                for (dx, dy) in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    next_state = self.next_state(positions, colors, door_open,
                                                 agent_id, dx, dy)
                    if not next_state:
                        continue

                    new_g = g + 1  # cost of one step
                    if next_state not in g_score or new_g < g_score[next_state]:
                        # We found a better path to next_s
                        g_score[next_state] = new_g
                        came_from[next_state] = (current_state, agent_id, dx, dy)

                        h = self.heuristic(next_state)
                        f = new_g + h
                        heapq.heappush(open_list, (f, new_g, next_state))

        return []

    def next_state(self, positions, colors, door, agent_id, dx, dy):
        """
        Attempt to move the specified agent by (dx, dy)
        Return the resulting next state (positions, colors, door)
        or None if the move is invalid
        """

        # Convert to lists for easy manipulation
        pos_list = list(positions)
        col_list = list(colors)

        # Current position of the agent
        x, y = pos_list[agent_id]

        # check of movement is allowed
        allowed, newx, newy = self.test_move((x, y), dx, dy, self.world_with_door(door))
        if not allowed:
            return None

        # If we can move, update the agent's position
        pos_list[agent_id] = (newx, newy)

        # Update the color if we stepped on cell with value 2
        if self.world[newy][newx] == 2:
            # Now the agent is of the right color
            col_list[agent_id] = True

        # check if we stepped on cell with value 3
        new_door = door
        if self.world[newy][newx] == 3:
            new_door = True

        # construct the new state
        new_positions = tuple(pos_list)
        new_colors = tuple(col_list)
        new_state = (new_positions, new_colors, new_door)

        # if nothing changed, return None
        if new_state == (positions, colors, door):
            return None

        return new_state

    def heuristic(self, state):
        """
        A simple (not necessarily perfect) heuristic:
        sum of Manhattan distances for each agent
        from either:
          - current pos -> color tile -> target
          - or if color acquired: current pos -> target
        ignoring the door obstacle for simplicity.
        """
        (positions, colors, door) = state
        hval = 0
        for i, has_col in enumerate(colors):
            (x, y) = positions[i]
            target_pos = self.target_position[i]
            # We'll guess a single color tile is at index (1,2) or so,
            # but actually the code uses '2' in multiple spots.
            # let's pick a fixed cell for color, e.g. (2,1) from default world
            color_tile = self.find_color_tile()

            if has_col:
                # distance from current pos to target
                hval += self.manhattan((x, y), target_pos)
            else:
                # distance from current pos -> color tile -> target
                hval += (self.manhattan((x, y), color_tile)
                         + self.manhattan(color_tile, target_pos))
        return hval

    def find_color_tile(self):
        """
        Scan self.world for the cell that has '2' (the color acquisition tile).
        In the default puzzle, there's only one color tile at (2,1).
        We'll just return that. Can be used if the tile is changed dynamically
        """
        for yy in range(len(self.world)):
            for xx in range(len(self.world[0])):
                if self.world[yy][xx] == 2:
                    return (xx, yy)

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, parent, goal_state):
        """
        Once we find the goal_state, trace back through 'parent' dict
        to get the sequence of moves (agent-id, dx, dy)
        """

        path = []
        state = goal_state

        while parent[state] is not None:
            prev_state, agent_id, dx, dy = parent[state]
            path.append((agent_id, dx, dy))

            state = prev_state

        path.reverse()
        return path

    def is_goal_state(self, positions, color):
        """
        Check if all the agents are in their target positions and colors
        """

        # check positions
        correct_positions = all(pos == target for pos, target in zip(positions, self.target_position))

        # check colors
        correct_colors = all(color)

        return correct_positions and correct_colors

    def has_correct_color(self, agent_id):
        """
        Check if the agent has acquired the target color
        """

        return (self.agents[agent_id].color == self.target_color[agent_id])

    def is_door_open(self):
        """
        Check if the door is open
        """
        # By default, self.door is (3, 2),
        # if world[y=2][x=3] == 0, door is open,
        # if world[y=2][x=3] == 1, door is closed

        return (self.world[self.door[1]][self.door[0]] == 0)

    def world_with_door(self, door_open):
        """
        Return a copy of the world grid that shows the correct state of door
        """

        wcopy = [row[:] for row in self.world]  # shallow copy of each row

        (dx, dy) = self.door

        if door_open:
            wcopy[dy][dx] = 0  # Door cell is open

        return wcopy


if __name__ == "__main__":
    mygame = Solution(algorithm='BFS')  # 'BFS', 'DFS', 'A-star'
    mygame.main()
