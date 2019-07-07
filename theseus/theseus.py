from sys import argv

from graph import Graph
import settings

def main():
    maze = Graph(argv)

    print(f'Nodes: {len(maze.nodes)}')
    if maze.start: print(f'Start: {maze.start.location}')
    if maze.end: print(f'End:   {maze.end.location}')
    print(f'Algorithm: {settings.ALGORITHM.__name__}')

if __name__ == '__main__':
    main()