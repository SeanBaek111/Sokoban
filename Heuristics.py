import math
import Solver
from ActionStateValidation import ActionStateValidation

class Heuristics:
    @staticmethod
    def heur_manhattan_distance(puzzle, n):
        '''admissible sokoban heuristic: Manhattan distance'''
        '''INPUT: a sokoban state'''
        '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
        
        sum_distance = 0  # Initialize the sum of distances

        for box in puzzle.boxes:  # Iterate through each box
            closest = float('inf')  # Initialize the closest distance with infinity

            for target in puzzle.targets:  # Iterate through each target
                distance = abs(box[0] - target[0]) + abs(box[1] - target[1])  # Compute Manhattan distance
                if distance < closest:  # Update the closest distance if a shorter distance is found
                    closest = distance

            sum_distance += closest  # Accumulate the sum of distances
        global prev_heur
        prev_heur = sum_distance
       # print(prev_heur)
        return sum_distance  # Return the sum of distances as the heuristic value
    
    @staticmethod
    def heuristic_83_1m(puzzle, n):
       
        """Heuristic for the Sokoban problem: sum of Manhattan distances between each box and the nearest target."""

        total_distance = 0
        total_worker_box_dist = 0
        penalty_distance = 0

        for box in puzzle.boxes:
            # Find the nearest target for this box
            distances = [manhattan_distance(box, target) for target in puzzle.targets]
            nearest_distance = min(distances) if distances else 0
            total_distance += nearest_distance

            # Apply penalty based on the distance to the nearest target
            penalty_distance += nearest_distance * nearest_distance  # Using square of the distance as penalty

            # Distance from worker to the box
            worker_box_dist = manhattan_distance(box, puzzle.worker)
            total_worker_box_dist += worker_box_dist
        total_worker_box_dist *= 3
        total_distance *= total_distance
       # penalty_distance *= 0.4
        puzzle.prev_heur = sum_h = total_distance + penalty_distance - total_worker_box_dist 
        return sum_h  

    @staticmethod
    def heuristic83Lookup(puzzle, n):
      
        """Heuristic for the Sokoban problem: sum of Manhattan distances between each box and the nearest target."""

        total_distance = 0
        total_worker_box_dist = 0
        penalty_distance = 0

        for box in puzzle.boxes:
            distances_list = []  # List to hold distances for each target

            # Find the nearest target for this box
            for target in puzzle.targets:
                sorted_positions = tuple(sorted([box, target])) 
                distances = puzzle.lookup_table.get(sorted_positions)

                if isinstance(distances, int):
                    distances = [distances]

                # Instead of getting the minimum distance here, just append it to distances_list
                distances_list.append(min(distances) if distances else 0)

            nearest_distance = min(distances_list)  # Get the nearest distance after considering all targets
            total_distance += nearest_distance

            # Apply penalty based on the distance to the nearest target
            penalty_distance += nearest_distance * nearest_distance  # Using square of the distance as penalty

            # Distance from worker to the box
            sorted_positions = tuple(sorted([box, puzzle.worker])) 
            worker_box_dist = puzzle.lookup_table.get(sorted_positions)

            total_worker_box_dist += worker_box_dist

        total_worker_box_dist *= 3
        total_distance *= total_distance

        puzzle.prev_heur = sum_h = total_distance + penalty_distance - total_worker_box_dist 
        return sum_h


    @staticmethod
    def modified_distance(puzzle, point1, point2):
        '''Compute the modified distance based on the given formula.'''
        x_distance = abs(point1[0] - point2[0])
        y_distance = abs(point1[1] - point2[1])

        # Apply the formula for x and y distances separately
        if x_distance == 0:
            x_val = 0
        else:
            x_val = x_distance**3 * math.log(x_distance, 2 + x_distance/4)

        if y_distance == 0:
            y_val = 0
        else:
            y_val = y_distance**3 * math.log(y_distance, 2 + y_distance/4)

        return x_val + y_val  # Return the sum of modified distances

    @staticmethod
    def combined_heuristic(puzzle, n):  
       
        '''admissible sokoban heuristic: Manhattan distance'''
        '''INPUT: a sokoban state'''
        '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''

        if puzzle.prev_heur is None:
            puzzle.prev_heur = float("inf")
            return puzzle.prev_heur
        #print("heuris")
       # state = n.state

        worker, boxes = n.state

        # Initial distances
        sum_distance = 0
        total_worker_box_dist = 0 
        modified_sum_distance = 0

        # Calculate distances for each box
        for box in boxes:
            manhattan_closest = float('inf')
            modified_closest = float('inf')

            for target in puzzle.targets:
                # Manhattan distance
               # manhattan_dist = abs(box[0] - target[0]) + abs(box[1] - target[1])

    #             if manhattan_dist < manhattan_closest:
    #                 manhattan_closest = manhattan_dist

                # Modified distance
                mod_dist = modified_distance(box, target)
                if mod_dist < modified_closest:
                    modified_closest = mod_dist

            sum_distance += manhattan_closest
            modified_sum_distance += modified_closest

            # Consider distance between worker and box if the box is not on target
            if box not in puzzle.targets:
                worker_box_dist = manhattan_distance(box, worker)
                total_worker_box_dist += worker_box_dist

        # Combine the heuristics
        combined_value =   modified_sum_distance + total_worker_box_dist

        return combined_value

    @staticmethod
    def heuristic_estimate(puzzle, n):
        '''
        This heuristic calculates an estimate for the Sokoban problem based on the modified Manhattan distance. 
        It takes into consideration the distance of boxes to their respective targets and also penalizes 
        certain conditions to make the heuristic more informative. 

        Additionally, the heuristic periodically checks if any box is in a "stuck" or "deadlock" state, 
        meaning it cannot reach its target due to other obstructions or boxes. If a box is identified in 
        such a state, the heuristic returns an infinite cost, indicating that the current state is undesirable.

        INPUT: A Sokoban state 'n'
        OUTPUT: A numeric value estimating the distance of the state to the goal.
        '''
        ... 
        # If there is no previous heuristic value, set it to infinity
        if puzzle.prev_heur is None:
            puzzle.prev_heur = float("inf")
            return puzzle.prev_heur

        state = n.state
        worker, boxes = state

        sum_distance = 0  # Initialize the sum of distances
        total_worker_box_dist = 0

        sum_benefit = 0
        penalty_distance = 0
        for box in puzzle.boxes:
            closest = float('inf')
            for target in puzzle.targets:
                # If the box is already on a target, skip the calculations
                if box == target:
                    continue
                sorted_positions = tuple(sorted([box, target])) 

                # Retrieve the distance from the lookup table
                distance = puzzle.lookup_table.get(sorted_positions)

                # If the distance isn't in the lookup table, compute using the Manhattan distance
                if distance is None:
                    distance = manhattan_distance(box, target)

                if distance < closest:
                    closest = distance
            sum_distance += closest * 2

            if box not in puzzle.targets: 
                sorted_positions = tuple(sorted([box, puzzle.worker]))  

                # Retrieve the distance between the worker and the box from the lookup table
                worker_box_dist = puzzle.lookup_table.get(sorted_positions)

                # If the distance isn't in the lookup table, compute using the Manhattan distance
                if worker_box_dist is None:
                    worker_box_dist = manhattan_distance(box, puzzle.worker)

                total_worker_box_dist += worker_box_dist

        puzzle.heuristic_count += 1
        stucked_box = 0

        # If heuristic count exceeds 10,000, reset it and check certain conditions
        if puzzle.heuristic_count >= 10000:
            puzzle.heuristic_count = 0

            # Check if a box cannot reach any target. If true, set the heuristic to infinity
            if ActionStateValidation.check_box_can_go_target(puzzle.walls, puzzle.targets, boxes) == False: 
                puzzle.prev_heur = stucked_box =  float('inf')
                puzzle.box_can_not_go_target_count += 1
                return stucked_box

            # Check if boxes are in a stuck configuration outside of a warehouse. If true, set heuristic to infinity
            if ActionStateValidation.check_stucked_case_no_warehouse(puzzle, boxes): 
                puzzle.stucked_case_count += 1
                puzzle.prev_heur = stucked_box =  float('inf')
                return stucked_box

        # Sum the computed distances and penalties to get the final heuristic value
        puzzle.prev_heur = sum_h = sum_distance + total_worker_box_dist  + penalty_distance

        # For debugging: If the heuristic is negative, print the components
        if sum_h < 0:
            print(sum_distance, total_worker_box_dist,stucked_box,"sum_distance + total_worker_box_dist  + stucked_box" )

        return sum_h


    @staticmethod
    def manhattan_distance(point1, point2):
        """Compute the Manhattan distance between two points."""
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

     


    


    

    
