from collections import deque

from node import Node
from timer import timer

@timer
def _traverse(self, current = None, visited = []):
    queue = deque([self.start])
    parent_of = {self.start: None}

    while current is not self.end:
        current = queue.popleft()
        visited.append(current)
        for next in current.neighbors.values():
            if next != None and not parent_of.get(next, False):
                queue.append(next)
                parent_of[next] = current

    child = visited.pop()
    self.path.append(child)
    while True:
        node = visited.pop()
        if node is parent_of[child]:
            self.path.append(node)
            child = node
        if child is self.start:
            return True
    return False