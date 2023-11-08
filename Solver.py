import time
import search
from Heuristics import Heuristics
from SokobanPuzzle import SokobanPuzzle

from Utility import *


class Solver:
    puzzle = None
    solution = None
    start_time = None
    
    @classmethod
    def solve_sokoban_elem(cls, warehouse, allow_taboo_push=False, h=None, observer_mode=False):
        '''    
        Solve using elementary actions the Sokoban puzzle provided.

        @param warehouse: a valid Warehouse object

        @return
            If puzzle cannot be solved return 'Impossible'
            If a solution was found, return a list of elementary actions that solves
                the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
                For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
                If the puzzle is already in a goal state, simply return []
        '''

        global puzzle
        global start_time
        global solution 


        start_time = time.time()

        # Check if already solved
        if set(warehouse.boxes) == set(warehouse.targets):
            return []

        macro_moves = [] 

       # allow_taboo_push = True

         # execute best_first_graph_search to solve the puzzle
        heuristic = Heuristics.heuristic83Lookup
        if h != None:
            heuristic = h

        cls.puzzle = SokobanPuzzle(warehouse, allow_taboo_push = allow_taboo_push, show_wh=show_wh,show_taboo_cells=show_taboo_cells , observer_mode=observer_mode)
        M = search.best_first_graph_search(cls.puzzle, heuristic)
       # M = search.astar_graph_search(puzzle, heuristic)
      #  M = search.uniform_cost_search(puzzle)
       # M = search.depth_first_graph_search(puzzle)
       # M = search.breadth_first_graph_search(puzzle)
      #  depth_first_graph_search(problem):


     # breadth_first_graph_search(problem):


      #  M = search.astar_graph_search(puzzle, heuristic)
       # M = search.astar_graph_search(SokobanPuzzle(warehouse, allow_taboo_push = allow_taboo_push), heuristic)

        if M is None:
            print("M is None")
            return ['Impossible']



        cls.solution = M.solution()
        return solution


    @classmethod
    def solve_sokoban_macro(cls, warehouse, allow_taboo_push=False, h=None, show_wh=False, show_taboo_cells=False, observer_mode=False):

        '''    
        Solve using macro actions the puzzle defined in the warehouse passed as
        a parameter. A sequence of macro actions should be 
        represented by a list M of the form
                [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
        For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
        means that the worker first goes the box at row 3 and column 4 and pushes it left,
        then goes to the box at row 5 and column 2 and pushes it up, and finally
        goes the box at row 12 and column 4 and pushes it down.

        @param warehouse: a valid Warehouse object

        @return
            If puzzle cannot be solved return the string 'Impossible'
            Otherwise return M a sequence of macro actions that solves the puzzle.
            If the puzzle is already in a goal state, simply return []
        ''' 
        


        start_time = time.time()

        # Check if already solved
        if set(warehouse.boxes) == set(warehouse.targets):
            return []

        macro_moves = [] 

       # allow_taboo_push = True

         # execute best_first_graph_search to solve the puzzle
        heuristic = Heuristics.heuristic83Lookup
        if h != None:
            heuristic = h

        cls.puzzle = SokobanPuzzle(warehouse, allow_taboo_push = allow_taboo_push, show_wh=show_wh,show_taboo_cells=show_taboo_cells, observer_mode=observer_mode )
        
         # Define a wrapper function for the heuristic that provides the puzzle
        def heuristic_wrapper(n):
            return h(cls.puzzle, n)

        # Use the wrapper function as the heuristic for the search algorithm
        M = search.best_first_graph_search(cls.puzzle, heuristic_wrapper)
        
      #  M = search.best_first_graph_search(cls.puzzle, heuristic)
       # M = search.astar_graph_search(puzzle, heuristic)
      #  M = search.uniform_cost_search(puzzle)
       # M = search.depth_first_graph_search(puzzle)
       # M = search.breadth_first_graph_search(puzzle)
      #  depth_first_graph_search(problem):


     # breadth_first_graph_search(problem):


      #  M = search.astar_graph_search(puzzle, heuristic)
       # M = search.astar_graph_search(SokobanPuzzle(warehouse, allow_taboo_push = allow_taboo_push), heuristic)

        if M is None:
            print("M is None")
            return ['Impossible']


        m_acts = M.path()

        actions = [p.action for p in m_acts] 
        states = [p.state[0] for p in m_acts] 

        prev_boxes_pos = m_acts[0].state[1]
        for m_act in m_acts:          
            worker_pos = m_act.state[0]
            cur_boxes_pos = m_act.state[1]
            if prev_boxes_pos != cur_boxes_pos: 
                macro_moves.append((Utility.swap_coordinates(worker_pos), m_act.action))
            prev_boxes_pos = cur_boxes_pos
        cls.solution = M
        return macro_moves