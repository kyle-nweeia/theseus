from node import Node
from timer import timer

@timer
def _traverse(self, destination = None, source = None, visited = []):
    if source:
        assert isinstance(source, Node)
    else:
        source = self.start
    if destination:
        assert isinstance(source, Node)
    else:
        destination = self.end

    if source in visited:
        return False
    visited.append(source)
    if source is destination:
        self.path.append(source)
        return True
    for next in source.neighbors.values():
        if self._traverse.unwrapped(self, destination, next, visited):
            self.path.append(source)
            return True