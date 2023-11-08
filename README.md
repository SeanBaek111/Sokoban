# Sokoban Solver

This repository contains a Python implementation of a solver for the Sokoban puzzle game. The solver uses various heuristic functions to efficiently find solutions to the game's puzzles.

<p align="center">
<img height="300" alt="image" src="https://github.com/SeanBaek111/Sokoban/assets/33170173/eeddf290-707b-4d79-9cd8-3b6f0d410283">
<img height="300" alt="image" src="https://github.com/SeanBaek111/Sokoban/assets/33170173/311099b0-819e-4e10-90c8-5816a37db2c4">
</p>



## Contents

- `warehouses/`: Directory containing different warehouse puzzle layouts.
- `ActionStateValidation.py`: Defines the state validation logic.
- `HeuristicUtilities.py`: Utility functions for heuristics.
- `Heuristics.py`: Implements various heuristic functions. 
- `PathfindingProblems.py`: Defines pathfinding problem sets. 
- `RunSokoban.ipynb`: A Jupyter notebook to run and test the Sokoban solver.
- `SokobanPuzzle.py`: Core logic for the Sokoban puzzle representation.
- `Solver.py`: The main solver algorithm for the puzzles.
- `TeamInfo.py`: Contains team information.
- `Utility.py`: General utility functions.
- `search.py`: Implements search algorithms.
- `sokoban.py`: Entry point for the solver.
- `sokoban_timing_data.csv`: Timing data for solver performance.

## Running the Solver

To run the solver and test it against various puzzles, use the `RunSokoban.ipynb` Jupyter notebook. The notebook demonstrates the setup and execution of the solver, including importing necessary modules, displaying team information, running the solver on specific puzzles, and evaluating performance.

```python
from TeamInfo import TeamInfo
from Solver import Solver
from Heuristics import Heuristics
from HeuristicUtilities import HeuristicUtilities

# Display team information
team_info = TeamInfo()
print(team_info.my_team())

# Run the solver on a puzzle
warehouse_index = 1
evaluate_warehouse(warehouse_index, False, Heuristics.heur_manhattan_distance)
```

## Observer Mode

The `observer_mode` feature provides a visual simulation of the solver's progress through each step of the puzzle. This is useful for understanding the decision-making process of the solver and debugging.

To enable observer mode, set the `observer_mode` flag to `True` when initializing the Solver. Here's an example:

```python
observer_mode = True 
warehouse_index = 1 
evaluate_warehouse(warehouse_index, False, Heuristics.heur_manhattan_distance, show_wh, show_taboo_cells,observer_mode)
