from constants import EAST, NORTH, SOUTH, WEST

class Node:
    def __init__(self, location):
        assert len(location) >= 2

        self.location = location
        self.neighbors = {NORTH: None, SOUTH: None, EAST: None, WEST: None}

    def set_neighbor(self, node, direction): # See if this can be improved with property()
        if node:
            assert isinstance(node, Node)
        
        self.neighbors[direction] = node