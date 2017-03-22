from maze import Maze
import random

labyrinths = [Maze(5, 15), Maze(6,6), Maze(7,3), Maze(random.randrange(50),random.randrange(50))]

for i in range(len(labyrinths)):
    labyrinth = labyrinths[i]
    labyrinth.matrix_to_weighted_adjacency_matrix()
    labyrinth.dijkstra()
    labyrinth.view()