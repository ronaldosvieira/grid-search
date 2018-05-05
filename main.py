import sys
from search import *

raw_data = sys.argv

def usage_error(error = None):
    if error is not None:
        print("error: %s" % error)
    
    print("usage: %s map x_s y_s x_g y_g algorithm heuristic?" % raw_data[0])
    sys.exit(1)

if len(raw_data) not in [7, 8]:
    usage_error()

map_name, algorithm = raw_data[1], raw_data[6]
x_s, y_s, x_g, y_g = map(int, raw_data[2:6])

with open("maps/" + map_name, 'r') as file:
    data = file.readlines()
    
height = int(data[1].split()[1])
width = int(data[2].split()[1])
grid = list(map(lambda l: list(l.rstrip()), data[4:]))

instance = Instance()

for i in range(0, height):
    for j in range(0, width):
        instance.add_state(i, j, grid[i][j] == '.')
        
for i in range(0, height):
    for j in range(0, width):
        for x in range(-1 if i > 0 else 0, 2 if i < height - 1 else 0):
            for y in range(-1 if j > 0 else 0, 2 if j < width - 1 else 0):
                instance.add_successor(i, j, i + x, j + y)
                
instance.set_goal(instance.states[(x_g, y_g)])

if algorithm == 'a-star':
    try:
        heuristic = raw_data[7]
    except:
        usage_error("heuristic is mandatory for a-star")
        
    if heuristic not in ['manhattan', 'octile']:
        usage_error("invalid heuristic")
        
    pass
        
elif algorithm == 'best-fit':
    pass
elif algorithm == 'uniform-cost':
    pass
elif algorithm == 'iterative-deepening':
    pass
else:
    usage_error("invalid algorithm")