import time
from IPython.display import clear_output


class HeuristicUtilities:
    @staticmethod
    def print_solution(goal_node):
        """Show solution represented by a specific goal node."""
        path = goal_node.path()
        print(f"Solution takes {len(path) - 1} steps from the initial state")
        for node in path:
            if node.action is not None:
                print(f"Move to {node.action}")
            print(node.state)

    @staticmethod
    def print_solution_replay(goal_node, delay=0.5):
        """Show solution represented by a specific goal node with a delay."""
        path = goal_node.path()
        print(f"Solution takes {len(path) - 1} steps from the initial state")
        for node in path:
            if node.action is not None:
                time.sleep(delay)
                clear_output(wait=True)
                print(f"Move to {node.action}")
            print(node.state)

    @staticmethod
    def get_objects(state):
        """Extracts objects (worker, boxes, targets) from the state string."""
        worker, boxes, targets = None, [], []
        rows = state.strip().split('\n')
        for row_num, row in enumerate(rows):
            for col_num, char in enumerate(row):
                if char in ('@', '!'):
                    worker = (col_num, row_num)
                if char in ('$', '*'):
                    boxes.append((col_num, row_num))
                if char in ('.', '*', '!'):
                    targets.append((col_num, row_num))
        return worker, boxes, targets

    @staticmethod
    def extract_grid(warehouse):
        """Extracts a visual grid from the warehouse state."""
        x_size, y_size = 1 + max(x for x, _ in warehouse.walls), 1 + max(y for _, y in warehouse.walls)
        vis = [[" "] * x_size for _ in range(y_size)]
        for (x, y) in warehouse.walls:
            vis[y][x] = "#"
        for (x, y) in warehouse.targets:
            vis[y][x] = "."
        for (x, y) in warehouse.boxes:
            vis[y][x] = "*" if (x, y) in warehouse.targets else "$"
        worker_x, worker_y = warehouse.worker
        vis[worker_y][worker_x] = "!" if (worker_x, worker_y) in warehouse.targets else "@"
        return vis

    @staticmethod
    def manhattan_distance(point1, point2):
        """Compute the Manhattan distance between two points."""
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
