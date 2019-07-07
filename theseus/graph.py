from itertools import product

from PIL import Image

from constants import Direction, EAST, NORTH, SOUTH, WEST
from node import Node
from settings import ALGORITHM, INPUT_FOLDER, OUTPUT_FOLDER, PATH_COLOR
from timer import timer

class Graph:
    def __init__(self, argv):
        self.end = None
        self.nodes = {}
        self.path = []
        self.start = None

        self._parse_argv(argv)
        self._open_maze()
        self._create_nodes()
        self._connect_nodes()
        self._traverse()
        self._trace()

    @timer
    def _connect_nodes(self):
        for node, direction in product(self.nodes.values(), Direction):
            neighbors = self._find_neighbors(node.location)
            if self.maze.getpixel(neighbors[direction]) == self.cell_color:
                node.set_neighbor(self._find_node(node, direction), direction)

    def _count_branches(self, point, branches = 0):
        assert len(point) >= 2
        assert point[0] in range(self.width)
        assert point[1] in range(self.height)

        for x, y in self._find_neighbors(point).values():
            if x in range(self.width) and y in range(self.height):
                if self.maze.getpixel((x, y)) == self.cell_color:
                    branches += 1
        return branches

    @timer
    def _create_nodes(self):
        for point in product(range(1, self.width - 1), range(1, self.height - 1)):
            if self.maze.getpixel(point) == self.cell_color:
                if self._count_branches(point) > 2:
                    self.nodes[point] = Node(point)
                elif self._is_terminus(point):
                    self.nodes[point] = Node(point)
                    self._set_terminus(self.nodes[point])

    def _find_node(self, node, direction):
        assert isinstance(node, Node)
        assert direction in Direction

        previous = node.location
        current = self._find_neighbors(previous)[direction]

        while self._count_branches(current) == 2:
            for next in self._find_neighbors(current).values():
                if next != previous and self.maze.getpixel(next) == self.cell_color:
                    previous, current = current, next
                    break
        if self._count_branches(current) == 1:
            return None
        elif self._is_edge(current):
            return self.nodes[previous]
        else:
            return self.nodes[current]

    def _find_neighbors(self, point):
        assert len(point) >= 2
        assert point[0] in range(self.width)
        assert point[1] in range(self.height)

        x, y = point[0], point[1]

        return {NORTH: (x, y - 1), SOUTH: (x, y + 1), EAST: (x + 1, y), WEST: (x - 1, y)}

    def _is_edge(self, point):
        assert len(point) >= 2
        assert point[0] in range(self.width)
        assert point[1] in range(self.height)

        if point[0] == 0:
            return True
        elif point[0] == self.width - 1:
            return True
        elif point[1] == 0:
            return True
        elif point[1] == self.height - 1:
            return True
        else:
            return False

    def _is_terminus(self, point):
        assert len(point) >= 2
        assert point[0] in range(self.width)
        assert point[1] in range(self.height)

        for neighbor in self._find_neighbors(point).values():
            if self._is_edge(neighbor):
                return True
        return False

    def _open_maze(self):
        self.maze = Image.open(self.input_file)
        if self.maze.mode != 'RGB':
            self.maze = self.maze.convert('RGB')
            assert self.maze.mode == 'RGB'
        
        self.cell_color = self.maze.getpixel((0, 0))
        self.frames = [self.maze]
        self.height = self.maze.height
        self.width = self.maze.width

    def _parse_argv(self, argv):
        if len(argv) > 1:
            self.input_file = argv[1]
        else:
            self.input_file = 'maze.gif'
        if len(argv) > 2:
            self.output_file = OUTPUT_FOLDER / argv[2]
        else:
            self.output_file = OUTPUT_FOLDER / self.input_file
        self.input_file = INPUT_FOLDER / self.input_file

    def _set_terminus(self, node):
        assert isinstance(node, Node)

        if self.start is None:
            self.start = node
        elif self.end is None:
            self.end = node

    @timer
    def _trace(self):
        for i, j in zip(self.path[-1:0:-1], self.path[-2::-1]):
            for direction in Direction:
                if i.neighbors[direction] is j:
                    previous = i.location
                    current = self._find_neighbors(previous)[direction]
                    while True:
                        self.maze.putpixel(previous, PATH_COLOR)
                        self.frames.append(self.maze.convert('P'))
                        if j and current == j.location:
                            break
                        for next in self._find_neighbors(current).values():
                            if self.maze.getpixel(next) == self.cell_color:
                                previous, current = current, next
        self.maze.putpixel(self.end.location, PATH_COLOR)
        self.frames.append(self.maze.convert('P'))
        self.frames[0].save(self.output_file,
            save_all=True,
            append_images=self.frames[1:],
            duration=20,
            loop=1
            )
    
Graph._traverse = ALGORITHM._traverse