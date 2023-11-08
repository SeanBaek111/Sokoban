import search

class PathfindingProblems:
    class WarehousePathfindingProblem(search.Problem):
        def __init__(self, initial, warehouse, goal):
            """ 
            Initialize the pathfinding problem.

            Parameters:
            - initial (tuple): Starting position as a tuple (row, col).
            - warehouse (Warehouse object): Represents the warehouse's state and layout.
            - goal (tuple): Target position to reach as a tuple (row, col).
            """
            super().__init__(initial, goal)
            self.warehouse = warehouse

        def actions(self, state):
            """ 
            Return possible movement directions from the current state.

            Parameters:
            - state (tuple): Current position as a tuple (row, col).

            Returns:
            - list: A list of valid movement directions as (dx, dy) tuples.
            """
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # UP, DOWN, LEFT, RIGHT
            result = []
            for dx, dy in directions:
                next_pos = (state[0] + dx, state[1] + dy)
                if self.is_walkable(next_pos):
                    result.append((dx, dy))
            return result

        def result(self, state, action):
            """ 
            Compute the resulting state after taking an action.

            Parameters:
            - state (tuple): Current position as a tuple (row, col).
            - action (tuple): Movement direction as a (dx, dy) tuple.

            Returns:
            - tuple: New position after taking the action.
            """
            return (state[0] + action[0], state[1] + action[1])

        def goal_test(self, state):
            """ 
            Determine if the current state matches the goal state.

            Parameters:
            - state (tuple): Current position as a tuple (row, col).

            Returns:
            - bool: True if the current state matches the goal, otherwise False.
            """
            return state == self.goal

        def path_cost(self, c, state1, action, state2):
            """ 
            Compute the cost of the path; each step costs 1.

            Parameters:
            - c (int): Current cost.
            - state1 (tuple): Starting position of this step.
            - action (tuple): Movement direction taken.
            - state2 (tuple): Ending position after taking the action.

            Returns:
            - int: Updated cost after taking the action.
            """
            return c + 1

        def is_walkable(self, pos):
            """ 
            Check if the position is walkable (i.e., not a wall or box).

            Parameters:
            - pos (tuple): Position to check.

            Returns:
            - bool: True if the position is walkable, otherwise False.
            """
            return pos not in self.warehouse.walls and pos not in self.warehouse.boxes


    class WarehouseLookupTableProblem(search.Problem):
        def __init__(self, initial, warehouse, goal):
            """ 
            Initialize the lookup table problem.

            Parameters:
            - initial (tuple): Starting position as a tuple (row, col).
            - warehouse (Warehouse object): Represents the warehouse's state and layout.
            - goal (tuple): Target position to reach as a tuple (row, col).
            """
            super().__init__(initial, goal)
            self.warehouse = warehouse

        def actions(self, state):
            """Return possible movement directions."""
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            result = []
            for dx, dy in directions:
                next_pos = (state[0] + dx, state[1] + dy)
                if self.is_walkable(next_pos):
                    result.append((dx, dy))
            return result

        def result(self, state, action):
            """Compute the resulting state after taking an action."""
            return (state[0] + action[0], state[1] + action[1])

        def goal_test(self, state):
            """Determine if the current state matches the goal state."""
            return state == self.goal

        def path_cost(self, c, state1, action, state2):
            """Compute the cost of the path; each step costs 1."""
            return c + 1

        def is_walkable(self, pos):
            """Check if the position is walkable (i.e., not a wall)."""
            return pos not in self.warehouse.walls 

    class CanBoxGoTargetProblem(search.Problem):
        def __init__(self, initial, goal, walls, boxes):
            """
            Initialize the problem to determine if a box can reach a target.

            Parameters:
            - initial (tuple): Starting position of the box.
            - goal (tuple): Target position for the box to reach.
            - walls (set of tuples): Positions representing walls.
            - boxes (set of tuples): Positions representing other boxes.
            """

            self.initial = (initial, goal)  # Combining the box's initial position and goal into a state.
            self.goal = goal
            self.walls = walls 
            self.boxes = ()
            for box in boxes:
                if box != initial:  # Avoid adding the moving box to the boxes set.
                    self.boxes += (box,)

        def actions(self, state):
            """Return possible movement directions for the box."""

            box, _ = state

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            result = []
            for dx, dy in directions:
                next_pos = (box[0] + dx, box[1] + dy)
                if self.is_walkable(next_pos):
                    result.append((dx, dy))

            return result

        def result(self, state, action): 
            box, target = state

            new_pos = ( box[0] + action[0], box[1] + action[1])

            return new_pos, target

        def goal_test(self, state):
            """Determine if the box is at the target location."""
            box, target = state
            return box == self.goal

        def path_cost(self, c, state1, action, state2):
            """Compute the cost of the path; each move costs 1."""
            return c + 1

        def is_walkable(self, pos):
            """Check if the position is walkable (i.e., not a wall or another box)."""
            b_in_walls = pos in self.walls
            b_in_boxes = pos in self.boxes
            if b_in_walls or b_in_boxes: 
                return False 
            return True 
