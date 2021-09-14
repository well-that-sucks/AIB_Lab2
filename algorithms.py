from collections import deque as queue

class Algoritms:

    min_step = 99999

    def return_min(self, res1, res2):
        if (res1[0] <= res2[0]):
            return res1
        return res2

    def retrieve_shortest_path(self, maze, pos, target, path_matrix):
        d_row = [-1, 0, 1, 0]
        d_col = [0, 1, 0, -1]
        t_matrix = [[0 for element in row] for row in maze]
        t_matrix[target[1]][target[0]] = path_matrix[target[1]][target[0]]
        position = target

        while position != pos:
            for i in range(4):
                adjx = position[0] + d_row[i]
                adjy = position[1] + d_col[i]
                if path_matrix[position[1]][position[0]] == path_matrix[adjy][adjx] + 1:
                    t_matrix[adjy][adjx] = t_matrix[position[1]][position[0]] - 1
                    position = (adjx, adjy)
                    break
        return t_matrix

    def find_path_dfs(self, maze, pos, target, step, path_matrix, visited):
        if not(pos[1] in range(len(maze)) and pos[0] in range(len(maze[0]))) or visited[pos[1]][pos[0]]:
            return (999999, path_matrix)
        path_matrix[pos[1]][pos[0]] = step
        if pos == target:
            return (step, path_matrix)
        if maze[pos[1]][pos[0]] != '#':
            visited[pos[1]][pos[0]] = True
            res = self.find_path_dfs(maze, (pos[0] + 1, pos[1]), target, step + 1, [x[:] for x in path_matrix], visited)
            if res[0] != 999999:
                return res
            res = self.find_path_dfs(maze, (pos[0] - 1, pos[1]), target, step + 1, [x[:] for x in path_matrix], visited)
            if res[0] != 999999:
                return res
            res = self.find_path_dfs(maze, (pos[0], pos[1] + 1), target, step + 1, [x[:] for x in path_matrix], visited)
            if res[0] != 999999:
                return res
            res = self.find_path_dfs(maze, (pos[0], pos[1] - 1), target, step + 1, [x[:] for x in path_matrix], visited)
            if res[0] != 999999:
                return res
            #res = self.find_path_dfs(maze, (pos[0] + 1, pos[1]), target, step + 1, [x[:] for x in path_matrix], visited)
            #res = self.return_min(res, self.find_path_dfs(maze, (pos[0] - 1, pos[1]), target, step + 1, [x[:] for x in path_matrix], visited))
            #res = self.return_min(res, self.find_path_dfs(maze, (pos[0], pos[1] + 1), target, step + 1, [x[:] for x in path_matrix], visited))
            #res = self.return_min(res, self.find_path_dfs(maze, (pos[0], pos[1] - 1), target, step + 1, [x[:] for x in path_matrix], visited))
            #visited[pos[1]][pos[0]] = False
            return res
        return (999999, path_matrix)

    def find_path_bfs(self, maze, pos, target, step, path_matrix, visited):
        d_row = [-1, 0, 1, 0]
        d_col = [0, 1, 0, -1]
        q = queue()
        q.append((step, pos[0], pos[1]))

        while (len(q) > 0):
            cell = q.popleft()
            visited[cell[2]][cell[1]] = True
            if path_matrix[cell[2]][cell[1]] > cell[0] or path_matrix[cell[2]][cell[1]] == 0:
                path_matrix[cell[2]][cell[1]] = cell[0]
            if (cell[1], cell[2]) == target:
                return cell[0], self.retrieve_shortest_path(maze, pos, target, path_matrix)
            else:
                for i in range(4):
                    adjx = cell[1] + d_row[i]
                    adjy = cell[2] + d_col[i]
                    if adjy in range(len(maze)) and adjx in range(len(maze[0])) and not(visited[adjy][adjx]) and maze[adjy][adjx] != '#':
                        q.append((cell[0] + 1, adjx, adjy))

        return path_matrix[target[1]][target[0]], self.retrieve_shortest_path(maze, pos, target, path_matrix)

    def find_path_ucs(self, maze, pos, target, step, path_matrix, visited):

        d_row = [-1, 0, 1, 0]
        d_col = [0, 1, 0, -1]

        queue = []
        queue.append([-step, pos[0], pos[1]])

        while (len(queue) > 0):
            queue = sorted(queue)
            cell = queue[-1]
            del queue[-1]
            cell[0] *= -1
            visited[cell[2]][cell[1]] = True
            if path_matrix[cell[2]][cell[1]] > cell[0] or path_matrix[cell[2]][cell[1]] == 0:
                path_matrix[cell[2]][cell[1]] = cell[0]
            if (cell[1], cell[2]) == target:
                return cell[0], self.retrieve_shortest_path(maze, pos, target, path_matrix)
            else:
                for i in range(4):
                    adjx = cell[1] + d_row[i]
                    adjy = cell[2] + d_col[i]
                    if adjy in range(len(maze)) and adjx in range(len(maze[0])) and not(visited[adjy][adjx]) and maze[adjy][adjx] != '#':
                        queue.append([(cell[0] + 1) * (-1), adjx, adjy])
    
            # mark as visited
    
        return path_matrix[target[1]][target[0]], self.retrieve_shortest_path(maze, pos, target, path_matrix)

    def find_path(self, search_function, maze, starting_pos, ending_pos):
        res = search_function(maze, starting_pos, ending_pos, 1, [[0 for element in row] for row in maze], [[False for element in row] for row in maze])
        return res[0], res[1]

    def get_dfs_function(self):
        return self.find_path_dfs
    
    def get_bfs_function(self):
        return self.find_path_bfs

    def get_ucs_function(self):
        return self.find_path_ucs