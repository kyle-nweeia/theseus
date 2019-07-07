from pathlib import Path
from sys import setrecursionlimit

from PIL.ImageColor import getcolor

import bfs, dfs

# Folders
INPUT_FOLDER = Path('mazes')
OUTPUT_FOLDER = Path('solutions')

# Maze Solving Algorithm
ALGORITHM = bfs

# Pixel Color
PATH_COLOR = getcolor('red', 'RGB')
SEARCH_COLOR = getcolor('gray', 'RGB')

# Recursion Limit
increase_recursion_limit = False
if increase_recursion_limit:
    setrecursionlimit(9999)
