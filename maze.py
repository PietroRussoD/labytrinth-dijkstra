import random
import sys

class Maze():
    #M rows and N columns:
    def __init__(self, M=32, N=32):
        self.min_value = 1
        self.max_value = sys.maxsize/2
        self.block_symbol = "X"
        symbols_distribution = self.set_distribution(1/5)
        self.m = M
        self.n = N
        self.nodes_number = M * N
        self.tangle = [[random.choice(symbols_distribution) for x in range(N)] for y in range(M)]
        self.start = self.set_point("S")
        self.end = self.set_point("E")

    def set_distribution(self,percentage):
        max_length = 10
        percentage = percentage if 0 <= percentage <= 1 else 0
        number_block_symbols = int(max_length * percentage)
        return [self.block_symbol if i < number_block_symbols else " " for i in range(max_length)]

    def set_point(self, symbol):
        if hasattr(self, 'start') and hasattr(self, 'end'):
            return
        valid_x = list(range(self.n))
        valid_y = list(range(self.m))

        if hasattr(self, 'start'):
            valid_x.remove(self.start[0])
            valid_y.remove(self.start[1])
        if hasattr(self, 'end'):
            valid_x.remove(self.end[0])
            valid_y.remove(self.end[1])

        x = random.choice(valid_x)
        y = random.choice(valid_y)
        self.tangle[y][x] = symbol
        return (x, y)

    def view(self):
        string_view = "-"*self.n + "--\n"
        for i in range(self.m):
            string_view += "|"+"".join([str(x) for x in self.tangle[i]]) + "|\n"
        string_view += "-" * self.n + "--\n"
        print(string_view)

    def dijkstra(self):
        # The distances vector contains the minimum distance from the start node per each node
        distances = [self.max_value for i in range(self.nodes_number)]
        # The provenances vector contains the previous node of the path
        provenances = [-1 for i in range(self.nodes_number)]
        # The visited vector contains 0 if the node is not been visited, 1 otherwise
        visited = [0 for i in range(self.nodes_number)]
        start_node = self.start[1] * self.n + self.start[0]
        end_node = self.end[1] * self.n + self.end[0]

        print("Start node: ", start_node)
        print("End node: ", end_node)

        current = start_node
        distances[current] = 0
        minimum_distance = 0

        # Until the current node is different than the end node and
        # until the minimum distance is different than the maximum value
        while current != end_node and minimum_distance != self.max_value:
            # Find the node with the minimum distance that has not been visited yet
            minimum_distance = self.max_value
            for i in range(self.nodes_number):
                if visited[i] == 0 and distances[i] < minimum_distance:
                    minimum_distance = distances[i]
                    current = i

            # Set the current node as visited
            visited[current] = 1

            # Update the distances vector
            for i in range(self.nodes_number):
                sum = distances[current] + self.weighted_adjacency_matrix[current][i]
                if self.weighted_adjacency_matrix[current][i] != self.max_value and distances[i] > sum:
                    distances[i] = sum
                    provenances[i] = current

        if visited[end_node] == 0:
            print("The path from {:d} to {:d} doesn't exist".format(start_node,end_node))
        else:
            path = []
            i=end_node
            while i != start_node:
                path.insert(0,i)
                i=provenances[i]
            path.insert(0,i)

            breadcrumbs_path = list(path)
            breadcrumbs_path.pop()
            breadcrumbs_path.pop(0)

            for i in range(len(breadcrumbs_path)):
                node = breadcrumbs_path[i]
                y = int(node/self.n)
                x = node%self.n
                self.tangle[y][x]="*"

    def matrix_to_weighted_adjacency_matrix(self):
        matrix_maze = [[1 if self.tangle[y][x]==self.block_symbol else 0 for x in range(self.n)] for y in range(self.m)]
        self.weighted_adjacency_matrix = [[0 for x in range(self.nodes_number)] for y in range(self.nodes_number)]

        # For all nodes
        for row in range(self.m):
            for column in range(self.n):
                current = row*self.n+column

                # N-W   N   N-E
                # W     C   E
                # S-W   S   S-E

                e = (row, column + 1)
                s_e = (row + 1, column + 1)
                s = (row + 1, column)

                east = matrix_maze[e[0]][e[1]] if 0 <= e[0] < self.m and 0 <= e[1] < self.n else -1
                south_east = matrix_maze[s_e[0]][s_e[1]] if 0 <= s_e[0] < self.m and 0 <= s_e[1] < self.n else -1
                south = matrix_maze[s[0]][s[1]] if 0 <= s[0] < self.m and 0 <= s[1] < self.n else -1

                if 0 <= (current + 1) < self.nodes_number and east == 0:
                        self.weighted_adjacency_matrix[current][current + 1] = \
                        self.weighted_adjacency_matrix[current + 1][current] = self.min_value if matrix_maze[row][column] == 0 else self.max_value

                if 0 <= (current + self.n + 1) < self.nodes_number and south == 0 and south_east == 0 and east == 0:
                        self.weighted_adjacency_matrix[current][current + self.n + 1] = \
                        self.weighted_adjacency_matrix[current + self.n + 1][current] = self.min_value if matrix_maze[row][column] == 0 else self.max_value

                if 0 <= (current + self.n) < self.nodes_number and south == 0:
                        self.weighted_adjacency_matrix[current][current + self.n] = \
                        self.weighted_adjacency_matrix[current + self.n][current] = self.min_value if matrix_maze[row][column] == 0 else self.max_value

        # If there is not an arch, the max value is set
        for i in range(self.nodes_number):
            for j in range(self.nodes_number):
                if self.weighted_adjacency_matrix[i][j] == 0:
                    self.weighted_adjacency_matrix[i][j] = self.max_value