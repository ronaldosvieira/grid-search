import sys, time
from search import *

def create_instance(width, height, grid):
    instance = Instance()
    
    for i in range(0, height):
        for j in range(0, width):
            if grid[i][j] == '.':
                instance.add_state(i, j, True)
            
    for i in range(0, height):
        for j in range(0, width):
            x_s, x_f = -1 if i > 0 else 0, 2 if i < height - 1 else 1
            y_s, y_f = -1 if j > 0 else 0, 2 if j < width - 1 else 1
            
            for x in range(x_s, x_f):
                for y in range(y_s, y_f):
                    if (not (x == 0 and y == 0) and 
                            grid[i][j] == '.' and grid[i + x][j + y] == '.' and 
                            grid[i][j + y] == '.' and grid[i + x][j] == '.'):
                        instance.add_successor(i, j, i + x, j + y, min(1.5, abs(x) + abs(y)))
    
    return instance

def solve(instance, algorithm, heuristic, start, goal): 
    instance.set_goal(goal)
    
    if algorithm == 'a-star':
        if heuristic is None:
            throw_error("heuristic is mandatory for a-star")
        elif heuristic == 'manhattan':
            return search(instance, start, AStarFringe(ManhattanDistanceHeuristic(goal)))
        elif heuristic == 'octile':
            return search(instance, start, AStarFringe(OctileDistanceHeuristic(goal)))
        else:
            throw_error("invalid heuristic")
            
    elif algorithm == 'best-first':
        return search(instance, start, BestFirstFringe(ManhattanDistanceHeuristic(goal)))
    elif algorithm == 'uniform-cost':
        return search(instance, start, UniformCostFringe())
    elif algorithm == 'limited-depth-first':
        return search(instance, start, LimitedDepthFirstFringe(float(heuristic)))
    elif algorithm == 'iterative-deepening':
        limit = 0
        fringe = LimitedDepthFirstFringe(limit)
        
        while True:
            try:
                return search(instance, start, fringe)
            except SolutionNotFoundError as s:
                limit += 0.5
                
                if fringe.filtered_out:
                    fringe = s.fringe
                    
                    fringe.limit = limit
                    fringe.initialized = False
                    fringe.init(list(reversed(fringe.filtered_out)))
                else:
                    fringe = LimitedDepthFirstFringe(limit)
                
                continue
            except KeyboardInterrupt as ki:
                print("ids stopped at depth %d" % limit)
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
    
    with open(map_name, 'r') as file:
        data = file.readlines()
        
    height = int(data[1].split()[1])
    width = int(data[2].split()[1])
    grid = list(map(lambda l: list(l.rstrip()), data[4:]))
    
    instance = create_instance(width, height, grid)
    
    try:
        start_time = time.time()
        
        solution = solve(instance, algorithm, heuristic, (x_s, y_s), (x_g, y_g))
        
        end_time = time.time()
        
        for node in solution.info["nodes_generated"]:
            x, y = node.state.label
            grid[x][y] = '!' if (x, y) in solution.info["nodes_expanded"] else ':'
        
        for step in solution:
            x, y = step.state.label
            grid[x][y] = 'x'
            
        grid[x_s][y_s] = 'S'
        grid[x_g][y_g] = 'G'
        
        print(solution[0])
        print(solution[-1])
        print()
        print(solution)
        print("\n".join(map(lambda l: "".join(l), grid)))
        print("nodes generated: %d" % (len(solution.info["nodes_generated"])))
        print("nodes expanded: %d" % len(solution.info["nodes_expanded"]))
        print("depth: %d" % solution.info["depth"])
        print("cost: %d" % solution.info["cost"])
        print("time elapsed: %g" % (end_time - start_time))
    except InvalidGoalError:
        print("<%d, %d, %g>" % (x_s, y_s, 0))
        print("<%d, %d, %g>" % (x_g, y_g, float("inf")))
        print()
    except SolutionNotFoundError as e:
        for node in e.fringe.nodes():
            x, y = node.state.label
            grid[x][y] = '!' if (x, y) in e.visited else ':'
            
        grid[x_s][y_s] = 'S'
        grid[x_g][y_g] = 'G'
        
        print("<%d, %d, %g>" % (x_s, y_s, 0))
        print("<%d, %d, %g>" % (x_g, y_g, float("inf")))
        print()
        print("\n".join(map(lambda l: "".join(l), grid)))
    
if __name__ == "__main__":
    main()