# grid-search
Common state space search algorithms on a 2D grid

## Requirements
- Python 3
- Tkinter (`sudo apt install python3-tk`)
- PIL (`sudo apt install python3-pil python3-pil.imagetk`)

## Usage
`python3 src/main.py <instance> <start_x> <start_y> <goal_x> <goal_y> <strategy> <heuristic?>`

### Examples
- `python3 src/main.py maps/map1.map 10 10 240 240 a-star manhattan` runs A* search on map1.map from (10, 10) to (240, 240) with the manhattan distance heuristic.
- `python3 src/main.py maps/map1.map 10 10 240 240 iterative-deepening` runs iterative deepening search on map1.map from (10, 10) to (240, 240).

## Options
- Default instances: `maps/map1.map`, `maps/map2.map` and `maps/map3.map`.
- Search strategies: `uniform-cost`, `iterative-deepening`, `best-first` and `a-star`.
- Heuristics: `manhattan` and `octile`
