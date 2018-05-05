import sys

raw_data = sys.argv

def usage_error(error = None):
    if error is not None:
        print("error: %s" % error)
    
    print("usage: %s map x_s y_s x_g y_g algorithm heuristic?" % raw_data[0])
    sys.exit(1)

if len(raw_data) not in [7, 8]:
    usage_error()

instance, x_s, y_s, x_g, y_g, algorithm = raw_data[1:7]

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