import search
import time
from Utility import *
from IPython.display import clear_output
 
class SokobanPuzzle(search.Problem): 
    
    # Constructor for the SokobanPuzzle class.
    def __init__(self, warehouse, allow_taboo_push=False, macro=False, show_wh=False, show_taboo_cells=False, observer_mode=False):     
        # Defining the goal state.
        self.goal = tuple(warehouse.targets)
        # Defining the initial state.
        self.initial = (warehouse.worker, tuple(warehouse.boxes))
        # Storing the wall locations.
        self.walls = warehouse.walls
        
        # Other class attributes and configurations.
        self.allow_taboo_push = allow_taboo_push
        self.macro = macro
        self.targets = warehouse.targets
        self.worker = warehouse.worker
        self.boxes = warehouse.boxes
        self.taboo_map, self.x_size, self.y_size, self.inside_cells = Utility.taboo_cells(warehouse, get_additional_values=True)
    
        self.taboo_cells = Utility.find_taboo_cells(self.taboo_map)
        self.cost = 0
        
         
        self.prev_heur = None
        self.possible_actions = ['Left', 'Right', 'Up', 'Down']
        self.wh = Utility.build_wh(self.walls, self.targets, self.boxes, self.worker)
        self.heuristic_count = 0
        self.stop = False
        self.stucked_case_count = 0
        self.box_can_not_go_target_count = 0
         
        self.observer_mode = observer_mode
        # Displaying the initial state if 'show_wh' is true.
        if show_wh :
            print("-------initial---------")
           # print(self.x_size, self.y_size)
            print(self.wh)
        
        # Displaying the taboo cells if 'show_taboo_cells' is true.
        if show_taboo_cells :
            print("-------taboo_cells---------")
            print(self.taboo_map)
            print(self.taboo_cells)
            print("---------------------------")
    
      
        # Creating a lookup table.
        self.lookup_table = self.create_lookup_table(warehouse) 
        
      
    def create_lookup_table(self, warehouse):
        """
        Creates a lookup table to store moving costs between various cells inside the warehouse.

        Parameters:
        - warehouse (list[list[int]]): A 2D list representing the warehouse where each cell's value indicates its type.

        Returns:
        - dict: A dictionary where keys are tuples of start and target positions, and values are the corresponding moving costs.
        """
        # Initialize a dictionary to store the moving costs between cells.
        lookup_table = {} 

        # Extract all valid start positions from inside_cells and swap their coordinates.
        swapped_start_positions = [Utility.swap_coordinates(pos) for pos in self.inside_cells]

        for start_pos in swapped_start_positions:
            # For each start position, calculate costs to all other target positions.
            for target_pos in swapped_start_positions:
                # Skip if start and target positions are the same.
                if start_pos == target_pos:
                    continue

                # Sort positions to ensure we don't compute cost twice for two symmetric positions.
                sorted_positions = tuple(sorted([start_pos, target_pos]))

                # If the cost for the sorted positions is already computed, skip.
                if sorted_positions in lookup_table:
                    continue

                # Calculate moving cost between start and target positions.
                cost = Utility.calc_moving_cost(warehouse, start_pos, target_pos)

                # If there's a valid cost, update the lookup table.
                if cost is not None:
                    lookup_table[sorted_positions] = cost

        return lookup_table 

    def actions(self, state):   
        """
        Determine the valid actions that can be taken from the given state.

        Args:
        - state (tuple): Current state, containing worker's position and positions of boxes.

        Returns:
        - list: A list of valid actions ('Left', 'Right', 'Up', 'Down') that can be taken from the current state.
        """

        # Extracting worker's position and positions of boxes from the current state.
        worker, boxes = state 

        # List to store valid actions.
        valid_actions = []

        # Loop over possible actions ('Left', 'Right', 'Up', 'Down').
        for action in self.possible_actions:
            dx, dy = 0, 0

            # Determine movement direction based on the action.
            if action == 'Left':
                dx = -1
            elif action == 'Right':
                dx = 1
            elif action == 'Up':
                dy = -1
            elif action == 'Down':
                dy = 1

            # Compute the new position of the worker after the move.
            new_worker = (worker[0] + dx, worker[1] + dy)

            # If the new worker's position is a wall, skip this action.
            if new_worker in self.walls:
                continue

            new_box_pos = None
            # If the new worker's position is occupied by a box.
            if new_worker in boxes:
                # Compute the new position for the box if it's pushed.
                new_box_pos = (new_worker[0] + dx, new_worker[1] + dy)

                # If the new box position is valid (i.e., it's not a wall or another box).
                if new_box_pos not in self.walls and new_box_pos not in boxes:
                    # If taboo pushes are not allowed, check if the new box position is a taboo cell.
                    if self.allow_taboo_push == False:
                        if new_box_pos in self.taboo_cells:
                            continue
                else:
                    continue

            # If all checks passed, the action is valid.
            valid_actions.append(action) 

        return valid_actions

 

    def result(self, state, action):
        """
        Compute the result of the given action from the given state.

        Args:
        - state (tuple): The current state, consisting of the worker's position and positions of boxes.
        - action (str): The action to be taken ('Left', 'Right', 'Up', 'Down').

        Returns:
        - tuple: The new state after the action is taken, consisting of the worker's new position and new positions of boxes.
        """

        # Extract the worker's position and positions of boxes from the current state.
        worker, boxes = state

        # Initialize movement direction.
        dx, dy = 0, 0

        # Determine movement direction based on the action.
        if action == 'Left':
            dx = -1
        elif action == 'Right':
            dx = 1
        elif action == 'Up':
            dy = -1
        elif action == 'Down':
            dy = 1

        # Calculate the new position of the worker after taking the action.
        new_worker = (worker[0] + dx, worker[1] + dy)

        # If the new worker's position is a wall, return the original state as the move is invalid.
        if new_worker in self.walls:
            return state

        # Check if the new worker's position will be on a box.
        if new_worker in boxes:
            # Calculate where the box would be moved to if pushed by the worker.
            new_box_pos = (new_worker[0] + dx, new_worker[1] + dy)

            # Check if the new box position is valid (i.e., not on a wall or another box).
            if self.walls not in new_box_pos and new_box_pos not in boxes:
                # If taboo pushes are not allowed, check if the new box position would be on a taboo cell.
                if self.allow_taboo_push == False:
                    if new_box_pos in self.taboo_cells:
                        # If it is, the move is invalid. Return the original state.
                        return state

                # Update the box position.
                new_boxes = tuple(box if box != new_worker else new_box_pos for box in boxes)
            else:
                # If the box's new position is invalid, return the original state.
                return state
        else:
            # If the worker doesn't push a box, the box positions remain unchanged.
            new_boxes = boxes

        # Update the worker's position.
        worker = new_worker
        boxes = new_boxes
        self.boxes = boxes
        self.worker = worker

        # If in observer mode, show updates in the environment.
        if self.observer_mode:
            if self.stop:
                input("Press Enter to continue...")
                self.stop = False
            wh = Utility.build_wh(self.walls, self.targets, self.boxes, self.worker)
            time.sleep(0.01)
            clear_output(wait=True)
            print("prev_heur:", self.prev_heur, ", self.cost:", self.cost, ", stucked:", self.stucked_case_count, ", box_can_not_go_target:", self.box_can_not_go_target_count)
            print(wh)

        # Return the new state.
        return new_worker, new_boxes



    # Method to check if the goal state is achieved.
    def goal_test(self, state):
        _, boxes = state
        return set(boxes) == set(self.goal)
    
    # Method to calculate the path cost.
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1."""
        self.cost = c
        return c + 1
    
    
   

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    def is_wall(pos):
        return pos in warehouse.walls

    # Helper function to check if a given position is a box
    def is_box(pos):
        return pos in warehouse.boxes

    # Dictionary to map action to coordinates change
    move_dict = {
        'Left': (-1, 0),
        'Right': (1, 0),
        'Up': (0, -1),
        'Down': (0, 1)
    }
   
    # Iterate through each action in the action sequence
    for action in action_seq:
        dx, dy = move_dict[action]
        worker_next_pos = (warehouse.worker[0] + dx, warehouse.worker[1] + dy)
        box_pushed_pos = (worker_next_pos[0] + dx, worker_next_pos[1] + dy)

        # Check for illegal moves
        if is_wall(worker_next_pos):
            return 'Failure'
        elif is_box(worker_next_pos):
            if is_wall(box_pushed_pos) or is_box(box_pushed_pos):
                return 'Failure'
            else:
                # Update box's position after being pushed
                warehouse.boxes.remove(worker_next_pos)
                warehouse.boxes.append(box_pushed_pos)

        # Update worker's position
        warehouse.worker = worker_next_pos

    # Return the final state of the warehouse
    return str(warehouse)
    