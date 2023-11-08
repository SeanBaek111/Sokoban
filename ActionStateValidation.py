import math
from search import astar_graph_search as astar_graph
from PathfindingProblems import PathfindingProblems
from itertools import combinations
from Utility import Utility

class ActionStateValidation:
    @staticmethod
    def can_push_box(position, direction, walls, boxes):
        """
        Check if the box at the given position can be pushed in the specified direction.
        """
        # Define the movement in terms of x and y coordinates
        move_dict = {
            'Left': (-1, 0),
            'Right': (1, 0),
            'Up': (0, -1),
            'Down': (0, 1)
        }
        dx, dy = move_dict[direction]

        # Calculate the position behind the box in the direction of the push
        behind_box = (position[0] + 2*dx, position[1] + 2*dy)

        # Check if the position behind the box is a wall, another box, or outside the warehouse boundaries
        if behind_box in walls or behind_box in boxes:
            return False
        return True

    @staticmethod
    def check_can_push_box( walls, boxes):


        directions = ['Left', 'Right', 'Up', 'Down']
        for box in boxes:
            b_can = False
            for direction in directions:
                if can_push_box(box, direction, walls, boxes):
                   # pr(box,direction, walls, boxes, p="box,direction, walls, boxes")
                    b_can = True
                    break
            if b_can == False:
                return False
        return True


    @staticmethod
    def can_go_there(warehouse, dst):
        '''    
        Determine whether the worker can walk to the cell dst=(row,column) 
        without pushing any box.

        @param warehouse: a valid Warehouse object

        @return
          True if the worker can walk to cell dst=(row,column) without pushing any box
          False otherwise
        ''' 
        dst = (dst[1], dst[0])  

        def heuristic_cango(n):
            state = n.state
            return math.sqrt(((state[1] - dst[1]) ** 2) + ((state[0] - dst[0]) ** 2))

        nodes = astar_graph(WarehousePathfindingProblem(warehouse.worker, warehouse, dst), heuristic_cango)


        if nodes is not None:

            return True
        else:
            return False

    @staticmethod    
    def heuristic_canboxgo(n):
        """
        Calculates the heuristic distance between a box and its destination.

        Parameters:
        - n: A node containing the current state.

        Returns:
        - float: Heuristic distance between the box and its destination.
        """

    #     # Count the total number of elements in the state
    #     count = sum(1 for elem in n.state for __ in (elem if isinstance(elem, tuple) else (elem,)))

    #     # If there are only 2 elements, return infinity (indicating it's not feasible)
    #     if count == 2:
    #         return float('inf')

        # Extract box and destination coordinates from the state
        box, dst = n.state

        # Calculate and return the Euclidean distance between the box and its destination
        return math.sqrt(((box[1] - dst[1]) ** 2) + ((box[0] - dst[0]) ** 2))


    @staticmethod
    def check_box_can_go_target(walls, targets, boxes):
        """
        Checks if all boxes can potentially be moved to any target location.

        Parameters:
        - walls (list): List of wall coordinates.
        - targets (list): List of target coordinates where boxes need to be placed.
        - boxes (list): List of current box coordinates.

        Returns:
        - bool: True if all boxes can be moved to any target location, False otherwise.
        """

        # Loop through each box
        for box in boxes: 
            # Check if box is not already on a target
            if box not in targets:  
                b_can_not_go = True
                # Loop through each target
                for target in targets:
                    dst = (target[1], target[0]) 

                    # Check if the box can be moved to the current target using A* algorithm
                    nodes = astar_graph(PathfindingProblems.CanBoxGoTargetProblem(box, target, walls, boxes), ActionStateValidation.heuristic_canboxgo)

                    # If a path is found, set b_can_not_go to False and break
                    if nodes is not None:
                        b_can_not_go = False
                        break
                # If box cannot be moved to any target, return False
                if b_can_not_go:
                    return False

        # If all boxes can be moved to at least one target, return True
        return True
    
    @staticmethod
    def check_stucked_case_no_warehouse(puzzle, boxes):
        """
        Determine if any box becomes stuck when moved to a new position.

        Parameters:
        - boxes: List of positions of all boxes.

        Returns:
        - True if any box becomes stuck in a new position, otherwise False.
        """
       

        # Create an initial layout filled with spaces based on puzzle dimensions
        layout = [[' ' for _ in range(puzzle.x_size)] for _ in range(puzzle.y_size)]

        # Populate the layout with wall positions
        for (x, y) in puzzle.walls:
            layout[y][x] = '#'

        # Generate all possible pairs of boxes
        pairs = list(combinations(boxes, 2))

        n_pairs = len(pairs)

        stuck_count = 0
        for pair in pairs:
            # Temporarily treat one of the boxes in the pair as a wall
            layout[pair[0][1]][pair[0][0]] = '#' 

            # Check if the other box in the pair becomes stuck when the first one is a wall
            if ActionStateValidation.is_box_stuck(puzzle, layout, pair[1], puzzle.targets):
                # Swap the roles of the boxes and re-check
                layout[pair[0][1]][pair[0][0]] = ' ' 
                layout[pair[1][1]][pair[1][0]] = '#' 
                if ActionStateValidation.is_box_stuck(puzzle, layout, pair[0], puzzle.targets):
                    stuck_count += 1

            # Reset the boxes' positions back to their original state
            layout[pair[1][1]][pair[1][0]] = ' ' 
            layout[pair[0][1]][pair[0][0]] = ' ' 

        # If the count of instances where boxes are stuck is significant, conclude that the move is problematic
        if stuck_count >= 1:
            return True

        return False

    

    @staticmethod
    def is_box_stuck(puzzle, layout, position, targets):
        """
        Check if a box is stuck in a particular position within the layout.

        Parameters:
        - layout: The warehouse layout with walls and spaces.
        - position: Tuple indicating the position of the box.
        - targets: List of target positions in the warehouse.

        Returns:
        - True if the box is stuck in the given position, otherwise False.
        """
        temp_taboo_cells = Utility.get_temp_taboo_cells(puzzle, layout, targets)
        if position in temp_taboo_cells:
            return True
        return False 
 

