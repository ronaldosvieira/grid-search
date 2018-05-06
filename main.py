import sys
from search import *

def create_instance(width, height, grid):
    instance = Instance()
    
    for i in range(0, height):
        for j in range(0, width):
            if grid[i][j] == '.':
                instance.add_state(j, i, True)
            
    for i in range(0, height):
        for j in range(0, width):
            x_s, x_f = -1 if i > 0 else 0, 2 if i < height - 1 else 0
            y_s, y_f = -1 if j > 0 else 0, 2 if j < width - 1 else 0
            
            for x in range(x_s, x_f):
                for y in range(y_s, y_f):
                    if (not (x == 0 and y == 0) and 
                            grid[i][j] == '.' and grid[i + x][j + y] == '.' and 
                            grid[i][j + y] == '.' and grid[i + x][j] == '.'):
                        instance.add_successor(j, i, j + y, i + x, min(1.5, abs(x) + abs(y)))
    
    return instance

def solve(instance, algorithm, heuristic, start, goal): 
    instance.set_goal(goal)
    
    if algorithm == 'a-star':
        if heuristic is None:
            throw_error("heuristic is mandatory for a-star")
            
        if heuristic not in ['manhattan', 'octile']:
            throw_error("invalid heuristic")
            
        return None
            
    elif algorithm == 'best-fit':
        return None
    elif algorithm == 'uniform-cost':
        return search(instance, start, UniformCostOpenList())
    elif algorithm == 'iterative-deepening':
        depth = 0
        
        while True:
            try:
                return search(instance, start, LimitedDepthFirstOpenList(depth))
            except SolutionNotFoundError:
                depth += 1
                continue
            except KeyboardInterrupt as ki:
                print("ids stopped at depth %d" % depth)
                raise ki
    else:
        throw_error("invalid algorithm")

def throw_error(error = None):
    if error is not None:
        print("error: %s" % error)

    sys.exit(1)

def main():
    raw_data = sys.argv
    
    if len(raw_data) not in [7, 8]:
        print("usage: %s map x_s y_s x_g y_g algorithm heuristic?" % raw_data[0])
        sys.exit(1)
    
    map_name, algorithm = raw_data[1], raw_data[6]
    x_s, y_s, x_g, y_g = map(int, raw_data[2:6])
    
    try:
        heuristic = raw_data[7]
    except:
        heuristic = None
    
    with open("maps/" + map_name, 'r') as file:
        data = file.readlines()
        
    height = int(data[1].split()[1])
    width = int(data[2].split()[1])
    grid = list(map(lambda l: list(l.rstrip()), data[4:]))
    
    instance = create_instance(width, height, grid)
    
    try:
        solution = solve(instance, algorithm, heuristic, (x_s, y_s), (x_g, y_g))
        
        print(solution[0])
        print(solution[-1])
        print()
        print(solution)
    except (SolutionNotFoundError, InvalidGoalError):
        print("<%d, %d, %g>" % (x_s, y_s, 0))
        print("<%d, %d, %g>" % (x_g, y_g, float("inf")))
        print()
    
if __name__ == "__main__":
    main()