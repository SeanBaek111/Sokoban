import search
from search import astar_graph_search as astar_graph 
from sokoban import Warehouse
from PathfindingProblems import PathfindingProblems

class Utility: 
   
    @staticmethod
    def swap_coordinates(coord):
        """
        Swaps the x and y coordinates of a given coordinate tuple.

        Parameters:
        - coord (tuple): A tuple containing the x and y coordinates.

        Returns:
        - tuple: A new tuple with the y and x coordinates swapped.
        """
        x, y = coord    
        return (y, x)

    @staticmethod
    def bfs_inside(start_r, start_c, layout):
        ''' 
        Perform BFS (Breadth First Search) to find all inside cells of a warehouse that are accessible.

        Parameters:
        - start_r (int): Starting row for BFS.
        - start_c (int): Starting column for BFS.
        - layout (list of lists): Represents the warehouse layout. "#" indicates a blocked cell.

        Returns:
        - set: Set containing all inside cells that can be reached from the starting cell.
        '''

        # Get the dimensions of the layout
        rows = len(layout)
        cols = len(layout[0])

        # Initialize a FIFO (First In First Out) queue to store cells to be visited
        queue = search.FIFOQueue()

        # Check if the start point itself is not blocked
        if layout[start_r][start_c] != '#':
            queue.append((start_r, start_c))
        else:
            # If the start point is blocked, look for the nearest unblocked point among its neighbors
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_r, new_c = start_r + dr, start_c + dc
                if 0 <= new_r < rows and 0 <= new_c < cols and layout[new_r][new_c] != '#':
                    queue.append((new_r, new_c))
                    break

        # Initialize visited matrix and a set to keep track of inside cells
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        inside_cells = set()

        # BFS traversal
        while queue:
            r, c = queue.pop()
            if not visited[r][c] and layout[r][c] != '#':
                visited[r][c] = True
                inside_cells.add((r, c))
                # Check neighboring cells and add them to the queue if they haven't been visited
                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_r, new_c = r + dr, c + dc
                    if 0 <= new_r < rows and 0 <= new_c < cols and not visited[new_r][new_c]:
                        queue.append((new_r, new_c))

        return inside_cells
   
    @staticmethod
    def process_taboo_horizontal(r, c, rows, cols, taboo, targets, direction):
        """
        Process horizontal walls to identify taboo cells.

        Parameters:
        - r (int): Current row index.
        - c (int): Current column index.
        - rows (int): Total number of rows.
        - cols (int): Total number of columns.
        - taboo (list of lists): A grid indicating the state of each cell.
                                'X' represents taboo, '#' represents walls, and ' ' represents an empty space.
        - targets (set of tuples): Set of target positions.
        - direction (int): Represents the direction to move (usually -1 or 1).
        """

        while r < rows - 1:  # While we haven't processed all the rows
            c = 1  # Reset the column index
            while c < cols - 1:  # While we haven't processed all the columns
                if taboo[r][c] == 'X':  # If current cell is taboo

                    # Identify the start of the corridor
                    start = c
                    end = start + 1
                    b_find = False
                    # Search for another taboo or wall to the right
                    while end < cols:
                        if taboo[r][end] == '#':  # Wall encountered
                            break
                        if taboo[r][end] == 'X':  # Another taboo encountered
                            b_find = True
                            break
                        else:
                            end += 1 

                    # Check if there's a clear space between the two taboos or wall
                    if b_find and end - start > 1:
                        b_find_space_or_wall = False
                        for x in range(start+1, end):
                            if taboo[r+direction][x] in [' ', 'X'] or (x, r) in targets:
                                b_find_space_or_wall = True
                                break
                        # If there is no clear space or wall between the two taboos, mark the cells in between as taboo
                        if not b_find_space_or_wall:
                            for x in range(start+1, end):
                                if taboo[r][x] not in targets and taboo[r+direction][x] == '#' and taboo[r][x] != '#':
                                    taboo[r][x] = 'X' 
                        c = end  # Update the current column index
                c += 1  # Move to the next column
            r += 1  # Move to the next row

    @staticmethod
    def process_taboo_vertical(r, c, rows, cols, taboo, targets, direction):
        """
        Process vertical walls to identify taboo cells.

        Parameters:
        - r (int): Current row index.
        - c (int): Current column index.
        - rows (int): Total number of rows.
        - cols (int): Total number of columns.
        - taboo (list of lists): A grid indicating the state of each cell.
                                'X' represents taboo, '#' represents walls, and ' ' represents an empty space.
        - targets (set of tuples): Set of target positions.
        - direction (int): Represents the direction to move (usually -1 or 1).
        """

        while r < rows - 1:  # While we haven't processed all the rows
            c = 1  # Reset the column index
            while c < cols - 1:  # While we haven't processed all the columns
                if taboo[c][r] == 'X':  # If current cell is taboo

                    # Identify the start of the corridor for vertical processing
                    start = c
                    end = start + 1
                    b_find = False
                    # Search for another taboo or wall upwards or downwards
                    while end < cols:
                        if taboo[end][r] == '#':  # Wall encountered
                            break
                        if taboo[end][r] == 'X':  # Another taboo encountered
                            b_find = True
                            break
                        else:
                            end += 1 

                    # Check if there's a clear space between the two taboos or wall
                    if b_find and end - start > 1:
                        b_find_space_or_wall = False
                        for x in range(start+1, end):
                            check_val = taboo[x][r + direction]
                            if check_val in [' ', 'X'] or (r, x) in targets:
                                b_find_space_or_wall = True
                                break
                        # If there is no clear space or wall between the two taboos, mark the cells in between as taboo
                        if not b_find_space_or_wall:
                            for x in range(start+1, end):
                                if taboo[x][r] not in targets and taboo[x][r + direction] == '#' and taboo[x][r] != '#':
                                    taboo[x][r] = 'X' 
                        c = end  # Update the current column index
                c += 1  # Move to the next column
            r += 1  # Move to the next row

    @staticmethod
    def temp_taboo_cells(puzzle, layout, targets):
        """
        Calculate the taboo cells in a Sokoban puzzle layout.

        Parameters:
        - layout (list of lists): Represents the puzzle layout.
                                  ' ' for empty spaces, '#' for walls.
        - targets (set of tuples): Set of target positions in the puzzle.

        Returns:
        - string: A visual representation of the taboo cells in the puzzle layout.
        """
      
        rows = len(layout)  # Total number of rows in the layout.
        cols = len(layout[0])  # Total number of columns in the layout.

        # Initialize the taboo layout with spaces.
        taboo = [[' ' for _ in range(cols)] for _ in range(rows)]

        # Populate walls in the taboo layout.
        for r in range(rows):
            for c in range(cols):
                if layout[r][c] == '#':
                    taboo[r][c] = '#'

        # Apply rule 1
        # Identify potential taboo cells based on wall configurations.
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                # For each empty cell within the interior of the puzzle.
                if layout[r][c] == ' ' and (r, c) in puzzle.inside_cells and (c, r) not in puzzle.targets:

                    # Check if the cell forms a corner with adjacent walls.
                    # If so, mark it as a taboo cell.
                    if any([
                        layout[r-1][c] == '#' and layout[r][c-1] == '#',
                        layout[r+1][c] == '#' and layout[r][c-1] == '#',
                        layout[r-1][c] == '#' and layout[r][c+1] == '#',
                        layout[r+1][c] == '#' and layout[r][c+1] == '#'
                    ]):
                        taboo[r][c] = 'X'

        # Apply processing functions to refine taboo cells considering horizontal and vertical directions.
        Utility.process_taboo_horizontal(1, 1, rows, cols, taboo, targets, -1)  # Process top horizontal corridors.
        Utility.process_taboo_horizontal(1, 1, rows, cols, taboo, targets, 1)   # Process bottom horizontal corridors.
        Utility.process_taboo_vertical(1, 1, cols, rows, taboo, targets, -1)    # Process left vertical corridors.
        Utility.process_taboo_vertical(1, 1, cols, rows, taboo, targets, 1)     # Process right vertical corridors.

        # Remove taboo markers from target cells. 
        # Target cells cannot be taboo since they are valid positions for boxes.
        for (x, y) in puzzle.targets:
            taboo[y][x] = ' '

        # Return a string representation of the taboo cells.
        return "\n".join(["".join(row) for row in taboo])


    @staticmethod
    def taboo_cells(warehouse, get_additional_values=False):
        """
        Determines the taboo cells in a given warehouse layout.

        Parameters:
        - warehouse: The warehouse layout containing positions of walls and targets.
        - get_additional_values: Flag to decide whether to return extra debug values.

        Returns:
        - The warehouse layout string with taboo cells marked.
        - If get_additional_values is True, also returns x_size, y_size, and inside_cells.
        """

        # Find the dimensions (width and height) of the warehouse.
        X, Y = zip(*warehouse.walls)
        x_size, y_size = 1 + max(X), 1 + max(Y)

        # Initialize a layout filled with spaces.
        layout = [[' ' for _ in range(x_size)] for _ in range(y_size)]

        # Mark the positions of the walls in the layout.
        for (x, y) in warehouse.walls:
            layout[y][x] = '#'

        rows = len(layout)
        cols = len(layout[0])

        # Initialize the taboo layout with spaces.
        taboo = [[' ' for _ in range(cols)] for _ in range(rows)]

        # Find the starting position inside the warehouse by scanning for the first open space after a wall.
        start_r, start_c = None, None
        wall_found = False
        for i in range(rows):
            if not wall_found:
                if layout[i][i] == '#':
                    wall_found = True
            else:
                if layout[i][i] != '#':
                    start_r = i
                    start_c = i
                    break

        # Identify all cells inside the warehouse using a BFS algorithm.
        inside_cells = Utility.bfs_inside(start_r, start_c, layout)

        # Mark walls in the taboo layout.
        for r in range(rows):
            for c in range(cols):
                if layout[r][c] == '#':
                    taboo[r][c] = '#'

        # Rule 1: Mark cells as taboo if they're next to two adjacent walls (forming a corner).
        for r in range(1, rows - 1):
            for c in range(1, cols - 1):
                if layout[r][c] == ' ' and (r, c) in inside_cells and (c, r) not in warehouse.targets:
                    if any([
                        layout[r-1][c] == '#' and layout[r][c-1] == '#',
                        layout[r+1][c] == '#' and layout[r][c-1] == '#',
                        layout[r-1][c] == '#' and layout[r][c+1] == '#',
                        layout[r+1][c] == '#' and layout[r][c+1] == '#'
                    ]):
                        taboo[r][c] = 'X'

        # Rule 2: Use helper functions to refine the taboo cells based on wall configurations.
        # For horizontal walls.
        Utility.process_taboo_horizontal(1, 1, rows, cols, taboo, warehouse.targets, -1)  # top
        Utility.process_taboo_horizontal(1, 1, rows, cols, taboo, warehouse.targets, 1)   # bottom

        # For vertical walls.
        Utility.process_taboo_vertical(1, 1, cols, rows, taboo, warehouse.targets, -1)  # left
        Utility.process_taboo_vertical(1, 1, cols, rows, taboo, warehouse.targets, 1)   # right

        # If a cell is a target, it shouldn't be taboo, so we remove the taboo marker from target cells.
        for (x, y) in warehouse.targets:
            taboo[y][x] = ' '

        # Return the taboo layout.
        if get_additional_values:
            return "\n".join(["".join(row) for row in taboo]), x_size, y_size, inside_cells
        else:
            return "\n".join(["".join(row) for row in taboo])



    @staticmethod
    def get_temp_taboo_cells(puzzle, layout, targets):
        """
        For a given layout and set of target positions, return a list of taboo cells.

        Parameters:
        - layout: The warehouse layout with walls and spaces.
        - targets: List of target positions in the warehouse.

        Returns:
        - List of taboo cell positions.
        """
        return Utility.find_taboo_cells(Utility.temp_taboo_cells(puzzle, layout, targets))

    @staticmethod
    def is_box_stuck(layout, position, targets):
        """
        Check if a box is stuck in a particular position within the layout.

        Parameters:
        - layout: The warehouse layout with walls and spaces.
        - position: Tuple indicating the position of the box.
        - targets: List of target positions in the warehouse.

        Returns:
        - True if the box is stuck in the given position, otherwise False.
        """
        temp_taboo_cells = get_temp_taboo_cells(layout, targets)
        if position in temp_taboo_cells:
            return True
        return False 

    @staticmethod
    def check_stucked_case_old(puzzle, warehouse, new_box_pos, old_box_pos):
        """
        Determine if moving a box to a new position causes it to be stuck.

        Parameters:
        - warehouse: The warehouse object containing walls, box positions, and other details.
        - new_box_pos: The new position of the box.
        - old_box_pos: The original position of the box.

        Returns:
        - True if moving the box to the new position causes it to be stuck, otherwise False.
        """
        

        # Create an initial layout filled with spaces based on puzzle dimensions
        layout = [[' ' for _ in range(puzzle.x_size)] for _ in range(puzzle.y_size)]

        # Populate the layout with wall positions
        for (x, y) in warehouse.walls:
            layout[y][x] = '#'

        new_boxes = []

        # Construct a list of new box positions, excluding the old position of the box
        for box in warehouse.boxes:
            if box != old_box_pos:
                new_boxes.append(box)
        new_boxes.append(new_box_pos)   

        # Generate all possible pairs of boxes
        pairs = list(combinations(new_boxes, 2))

        n_pairs = len(pairs)

        stuck_count = 0
        for pair in pairs:
            # Temporarily treat one of the boxes in the pair as a wall
            layout[pair[0][1]][pair[0][0]] = '#' 

            # Check if the other box in the pair is stuck when the first one is treated as a wall
            if is_box_stuck(layout, pair[1], warehouse.targets):
                # Swap the roles of the boxes and re-check
                layout[pair[0][1]][pair[0][0]] = ' ' 
                layout[pair[1][1]][pair[1][0]] = '#' 
                if is_box_stuck(layout, pair[0], warehouse.targets):
                    stuck_count += 1

            # Reset the box positions back to their original state
            layout[pair[1][1]][pair[1][0]] = ' ' 
            layout[pair[0][1]][pair[0][0]] = ' ' 

        # If the number of cases where boxes are stuck is significant, conclude that the move is problematic
        if stuck_count >= 1:
            return True

        return False

    @staticmethod
    def check_stucked_case(puzzle, boxes, new_box_pos, old_box_pos):
        """
        Determine if moving a box to a new position results in it being stuck.

        Parameters:
        - boxes: List of current positions of all boxes.
        - new_box_pos: The desired new position of the box.
        - old_box_pos: The previous position of the box before the desired move.

        Returns:
        - True if the box becomes stuck in the new position, otherwise False.
        """
         

        # Create an initial layout filled with spaces based on puzzle dimensions
        layout = [[' ' for _ in range(puzzle.x_size)] for _ in range(puzzle.y_size)]

        # Populate the layout with wall positions
        for (x, y) in puzzle.walls:
            layout[y][x] = '#'

        new_boxes = []

        # Formulate a list of box positions, excluding the old position of the box in question
        for box in boxes:
            if box != old_box_pos:
                new_boxes.append(box)
        new_boxes.append(new_box_pos)   

        # Generate all possible pairs of boxes
        pairs = list(combinations(new_boxes, 2))

        n_pairs = len(pairs)

        stuck_count = 0
        for pair in pairs:
            # Temporarily treat one of the boxes in the pair as a wall
            layout[pair[0][1]][pair[0][0]] = '#' 

            # Check if the other box in the pair becomes stuck when the first one is a wall
            if is_box_stuck(layout, pair[1], puzzle.targets):
                # Swap the roles of the boxes and re-check
                layout[pair[0][1]][pair[0][0]] = ' ' 
                layout[pair[1][1]][pair[1][0]] = '#' 
                if is_box_stuck(layout, pair[0], puzzle.targets):
                    stuck_count += 1

            # Reset the boxes' positions back to their original state
            layout[pair[1][1]][pair[1][0]] = ' ' 
            layout[pair[0][1]][pair[0][0]] = ' ' 

        # If the count of instances where boxes are stuck is significant, conclude that the move is problematic
        if stuck_count >= 1:
            return True

        return False

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
            if is_box_stuck(layout, pair[1], puzzle.targets):
                # Swap the roles of the boxes and re-check
                layout[pair[0][1]][pair[0][0]] = ' ' 
                layout[pair[1][1]][pair[1][0]] = '#' 
                if is_box_stuck(layout, pair[0], puzzle.targets):
                    stuck_count += 1

            # Reset the boxes' positions back to their original state
            layout[pair[1][1]][pair[1][0]] = ' ' 
            layout[pair[0][1]][pair[0][0]] = ' ' 

        # If the count of instances where boxes are stuck is significant, conclude that the move is problematic
        if stuck_count >= 1:
            return True

        return False

    @staticmethod
    def calc_moving_cost(warehouse, start, goal):
        """
        Calculate the moving cost from a start position to a goal position in the warehouse.

        Parameters:
        - warehouse: A representation of the warehouse containing walls, boxes, and other obstacles.
        - start: The starting position.
        - goal: The goal position.

        Returns:
        - The cost of moving from the start position to the goal position.
        - Returns None if a path from start to goal is not found.
        """

        def h_moving(n):
            """
            Heuristic function for the A* algorithm. Computes the Manhattan distance from
            the current state to the goal.

            Parameters:
            - n: The current node.

            Returns:
            - Manhattan distance from the current state to the goal.
            """
            state = n.state
            # Uncomment to use Euclidean distance as heuristic
            # return math.sqrt(((state[1] - goal[1]) ** 2) + ((state[0] - goal[0]) ** 2))
            return abs(state[1] - goal[1]) + abs(state[0] - goal[0])

        # Use A* algorithm to find the shortest path from start to goal
        nodes =  astar_graph(PathfindingProblems.WarehouseLookupTableProblem(start, warehouse, goal), h_moving)


        if nodes is not None:
            m_acts = nodes.path()

            return len(m_acts)-1  # Subtract 1 because the start node is also included in the path
        else:
            return None

    @staticmethod
    def find_taboo_cells(s): 
        """
        Extracts the coordinates of 'X' characters from a given string representation of the warehouse.

        Parameters:
        - s: String representation of the warehouse.

        Returns:
        - A list of (x,y) coordinates of 'X' characters.
        """
        lines = s.split('\n')
        taboo_positions = []
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char == 'X':
                    taboo_positions.append((x,y))

        return taboo_positions

    @staticmethod
    def prn(*args, **kwargs):    
        """
        Clear the output and print the provided arguments with logging information.

        Parameters:
        - args: Arguments to be printed.
        - kwargs: Keyword arguments for additional logging details.
        """
        clear_output(wait=True)
        print("--------write_log prn Started---------")
        for arg in args:
            print(arg)
        print("--------write_log prn Finished---------")

    @staticmethod
    def pr(*args, **kwargs):    
        """
        Print the provided arguments with logging information.

        Parameters:
        - args: Arguments to be printed.
        - kwargs: Keyword arguments for additional logging details.
        """
        title = "write_log"
        if kwargs.get('p', "") != "":
            title = kwargs['p']

        print("--------"+title+" Started---------")
        for arg in args:
            print(arg)
        print("--------"+title+" Finished---------")

    @staticmethod
    def replace_str(src, index, ch):
        """
        Replaces a character in a string at a specific index.

        Parameters:
        - src: The source string.
        - index: The index at which the character needs to be replaced.
        - ch: The character to replace with.

        Returns:
        - Modified string.
        """
        a = list(src)
        a[index] = ch
        return ''.join(a)

    @staticmethod
    def move(position, action):
        """
        Move to a new position based on the given action.

        Parameters:
        - position: The current position (x, y).
        - action: Movement action ('Up', 'Down', 'Left', 'Right').

        Returns:
        - New position after performing the action.
        """
        x, y = position
        if action == 'Up':
            return (x, y-1)
        elif action == 'Down':
            return (x, y+1)
        elif action == 'Left':
            return (x-1, y)
        elif action == 'Right':
            return (x+1, y)

    @staticmethod
    def get_new_state(state, new_worker, new_boxes):
        """
        Given the current state, new worker, and box positions, produce the new state.

        Parameters:
        - state: The current state representation.
        - new_worker: The new worker position.
        - new_boxes: List of new box positions.

        Returns:
        - New state representation.
        """
        # Remove boxes and worker from the current state
        new_state = state.replace("$", " ").replace("@", " ")

        # Add new boxes to the state
        rows = new_state.split("\n")
        for box in new_boxes: 
            if rows[box[0]][box[1]] != "*":
                rows[box[0]] = replace_str(rows[box[0]], box[1], "$")

        # Add the worker to the state
        rows[new_worker[0]] = replace_str(rows[new_worker[0]], new_worker[1], "@")

        # Compile the new state into a single string
        new_state = "\n".join(rows)
        return new_state
    
    
    @staticmethod
    def build_wh(walls, targets, boxes, worker):
        """
        Constructs a warehouse object given the walls, targets, boxes, and worker.

        Parameters:
        - walls: List of wall positions.
        - targets: List of target positions.
        - boxes: List of box positions.
        - worker: Worker's position.

        Returns:
        - Warehouse object.
        """
        wh = Warehouse()
        wh.walls = walls
        wh.targets = targets
        wh.boxes = boxes
        wh.worker = worker
        return wh