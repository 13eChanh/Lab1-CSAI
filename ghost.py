import pygame
import time
import sys
from utils import ucs_search
from collections import deque
import heapq

# Dictionary to store performance metrics
performance_data = {
    'bfs': {'times': [], 'memory': [], 'nodes': []},
    'dfs': {'times': [], 'memory': [], 'nodes': []},
    'ucs': {'times': [], 'memory': [], 'nodes': []},
    'astar': {'times': [], 'memory': [], 'nodes': []}
}

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id, level, powerup, eaten_ghost,
                 spooked_img, dead_img, HEIGHT, WIDTH, screen):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + 22
        self.center_y = self.y_pos + 22
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direct
        self.dead = dead
        self.in_box = box
        self.id = id
        self.level = level
        self.powerup = powerup
        self.screen = screen
        self.eaten_ghost = eaten_ghost
        self.spooked_img = spooked_img
        self.dead_img = dead_img
        self.HEIGHT = HEIGHT
        self.WIDTH = WIDTH
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not self.powerup and not self.dead) or (self.eaten_ghost[self.id] and self.powerup and not self.dead):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif self.powerup and not self.dead and not self.eaten_ghost[self.id]:
            self.screen.blit(self.spooked_img, (self.x_pos, self.y_pos))
        else:
            self.screen.blit(self.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if self.level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (self.level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if self.level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (self.level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (self.level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if self.level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if self.level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if self.level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if self.level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (self.level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if self.level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if self.level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (self.level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True
        else:
            self.turns[0] = True
            self.turns[1] = True
        if 350 < self.x_pos < 550 and 370 < self.y_pos < 480:
            self.in_box = True
        else:
            self.in_box = False
        return self.turns, self.in_box

    def move_not_path(self):
        if self.direction == 0:
            if self.target[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.speed
            elif not self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[0]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.target[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.speed
            elif not self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[1]:
                if self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.speed
            elif self.target[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.speed
            elif not self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[2]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos -= self.speed
        elif self.direction == 3:
            if self.target[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.speed
            elif not self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
            elif self.turns[3]:
                if self.target[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.target[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
                else:
                    self.y_pos += self.speed

        return self.x_pos, self.y_pos, self.direction

    def move_clyde(self):
        start_time = time.time()
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        current_x = int(self.center_x // num2)
        current_y = int(self.center_y // num1)
        target_x = int(self.target[0] // num2)
        target_y = int(self.target[1] // num1)

        path, nodes_expanded, max_memory = ucs_search(
            (current_x, current_y),
            (target_x, target_y),
            self.level,
            self.id,
            self.in_box,
            self.dead
        )

        end_time = time.time()
        performance_data['ucs']['times'].append((end_time - start_time) * 1000)  # Convert to milliseconds
        performance_data['ucs']['nodes'].append(nodes_expanded)
        performance_data['ucs']['memory'].append(max_memory)

        if not path:
            self.x_pos, self.y_pos, self.direction = self.move_not_path()
        else:
            next_dir = path[0]
            self.direction = next_dir
            if self.direction == 0 and self.turns[0]:
                self.x_pos += self.speed
            elif self.direction == 1 and self.turns[1]:
                self.x_pos -= self.speed
            elif self.direction == 2 and self.turns[2]:
                self.y_pos -= self.speed
            elif self.direction == 3 and self.turns[3]:
                self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = self.WIDTH
        elif self.x_pos > self.WIDTH:
            self.x_pos -= 30

        return self.x_pos, self.y_pos, self.direction

    def move_blinky_astar(self):
        start_time = time.time()
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        current_x = self.center_x // num2
        current_y = self.center_y // num1
        target_x = self.target[0] // num2
        target_y = self.target[1] // num1

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        neighbors = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        open_set = []
        heapq.heappush(open_set, (0, (current_x, current_y)))
        came_from = {}
        g_score = {(current_x, current_y): 0}
        f_score = {(current_x, current_y): heuristic((current_x, current_y), (target_x, target_y))}
        open_set_hash = {(current_x, current_y)}
        nodes_expanded = 0
        max_memory = sys.getsizeof(open_set) + sys.getsizeof(came_from) + sys.getsizeof(g_score) + sys.getsizeof(
            f_score) + sys.getsizeof(open_set_hash)

        while open_set:
            nodes_expanded += 1
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)

            if current == (target_x, target_y):
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                if path:
                    next_step = path[-1]
                    if next_step[0] > current_x:
                        self.direction = 0
                    elif next_step[0] < current_x:
                        self.direction = 1
                    elif next_step[1] < current_y:
                        self.direction = 2
                    elif next_step[1] > current_y:
                        self.direction = 3
                break

            for dx, dy in neighbors:
                neighbor = (current[0] + dx, current[1] + dy)
                if 0 <= neighbor[0] < len(self.level[0]) and 0 <= neighbor[1] < len(self.level):
                    if self.level[neighbor[1]][neighbor[0]] >= 3 and not (self.in_box or self.dead):
                        continue
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, (target_x, target_y))
                        if neighbor not in open_set_hash:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
                            open_set_hash.add(neighbor)
                            current_memory = sys.getsizeof(open_set) + sys.getsizeof(came_from) + sys.getsizeof(
                                g_score) + sys.getsizeof(f_score) + sys.getsizeof(open_set_hash)
                            max_memory = max(max_memory, current_memory)

        end_time = time.time()
        performance_data['astar']['times'].append((end_time - start_time) * 1000)  # Convert to milliseconds
        performance_data['astar']['nodes'].append(nodes_expanded)
        performance_data['astar']['memory'].append(max_memory)

        if not hasattr(self, 'direction') or not self.turns[self.direction]:
            self.x_pos, self.y_pos, self.direction = self.move_not_path()

        if self.direction == 0 and self.turns[0]:
            self.x_pos += self.speed
        elif self.direction == 1 and self.turns[1]:
            self.x_pos -= self.speed
        elif self.direction == 2 and self.turns[2]:
            self.y_pos -= self.speed
        elif self.direction == 3 and self.turns[3]:
            self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = self.WIDTH
        elif self.x_pos > self.WIDTH:
            self.x_pos = -30
        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        start_time = time.time()
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        current_x = self.center_x // num2
        current_y = self.center_y // num1
        target_x = self.target[0] // num2
        target_y = self.target[1] // num1

        def bfs(start, goal):
            queue = deque([start])
            visited = set()
            parent = {}
            nodes_expanded = 0
            max_memory = sys.getsizeof(queue) + sys.getsizeof(visited) + sys.getsizeof(parent)

            while queue:
                nodes_expanded += 1
                current = queue.popleft()
                if current == goal:
                    path = []
                    while current in parent:
                        path.append(current)
                        current = parent[current]
                    path.append(start)
                    path.reverse()
                    return path, nodes_expanded, max_memory

                visited.add(current)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (current[0] + dx, current[1] + dy)
                    if (0 <= neighbor[0] < len(self.level[0]) and
                            0 <= neighbor[1] < len(self.level)):
                        cell_value = self.level[neighbor[1]][neighbor[0]]
                        if (cell_value < 3 or cell_value == 9) and neighbor not in visited:
                            if neighbor not in parent:
                                parent[neighbor] = current
                            queue.append(neighbor)
                            current_memory = sys.getsizeof(queue) + sys.getsizeof(visited) + sys.getsizeof(parent)
                            max_memory = max(max_memory, current_memory)
            return None, nodes_expanded, max_memory

        path, nodes_expanded, max_memory = bfs((current_x, current_y), (target_x, target_y))

        end_time = time.time()
        performance_data['bfs']['times'].append((end_time - start_time) * 1000)  # Convert to milliseconds
        performance_data['bfs']['nodes'].append(nodes_expanded)
        performance_data['bfs']['memory'].append(max_memory)

        if path and len(path) > 1:
            next_step = path[1]
            dx = next_step[0] - current_x
            dy = next_step[1] - current_y

            if dx > 0:
                self.direction = 0
            elif dx < 0:
                self.direction = 1
            elif dy < 0:
                self.direction = 2
            elif dy > 0:
                self.direction = 3

        if not hasattr(self, 'direction') or not self.turns[self.direction]:
            self.x_pos, self.y_pos, self.direction = self.move_not_path()

        if self.direction == 0 and self.turns[0]:
            self.x_pos += self.speed
        elif self.direction == 1 and self.turns[1]:
            self.x_pos -= self.speed
        elif self.direction == 2 and self.turns[2]:
            self.y_pos -= self.speed
        elif self.direction == 3 and self.turns[3]:
            self.y_pos += self.speed
        else:
            for i in range(4):
                if self.turns[i]:
                    self.direction = i
                    break

        if self.x_pos < -30:
            self.x_pos = self.WIDTH
        elif self.x_pos > self.WIDTH:
            self.x_pos = -30

        return self.x_pos, self.y_pos, self.direction

    def move_pinky_joreii(self):
        start_time = time.time()
        num1 = (self.HEIGHT - 50) // 32
        num2 = (self.WIDTH // 30)
        current_x = self.center_x // num2
        current_y = self.center_y // num1
        target_x = self.target[0] // num2
        target_y = self.target[1] // num1

        def joreii_dfs(start, goal):
            stack = deque([start])
            visited = set()
            parent = {}
            nodes_expanded = 0
            max_memory = sys.getsizeof(stack) + sys.getsizeof(visited) + sys.getsizeof(parent)

            while stack:
                nodes_expanded += 1
                current = stack.pop()
                if current == goal:
                    path = []
                    while current != start:
                        path.append(current)
                        current = parent[current]
                    path.append(start)
                    path.reverse()
                    return path, nodes_expanded, max_memory

                visited.add(current)
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    neighbor = (current[0] + dx, current[1] + dy)
                    if 0 <= neighbor[0] < len(self.level[0]) and 0 <= neighbor[1] < len(self.level):
                        if ((self.level[neighbor[1]][neighbor[0]] < 3) or (
                                self.level[neighbor[1]][neighbor[0]] == 9)) and neighbor not in visited:
                            if neighbor not in parent:
                                parent[neighbor] = current
                            stack.append(neighbor)
                            current_memory = sys.getsizeof(stack) + sys.getsizeof(visited) + sys.getsizeof(parent)
                            max_memory = max(max_memory, current_memory)
            return None, nodes_expanded, max_memory

        pinky_path, nodes_expanded, max_memory = joreii_dfs((current_x, current_y), (target_x, target_y))

        end_time = time.time()
        performance_data['dfs']['times'].append((end_time - start_time) * 1000)  # Convert to milliseconds
        performance_data['dfs']['nodes'].append(nodes_expanded)
        performance_data['dfs']['memory'].append(max_memory)

        if pinky_path and len(pinky_path) > 1:
            next_step = pinky_path[1]
            if next_step[0] > current_x:
                self.direction = 0
            elif next_step[0] < current_x:
                self.direction = 1
            elif next_step[1] < current_y:
                self.direction = 2
            elif next_step[1] > current_y:
                self.direction = 3

        if not hasattr(self, 'direction') or not self.turns[self.direction]:
            self.x_pos, self.y_pos, self.direction = self.move_not_path()

        if self.direction == 0 and self.turns[0]:
            self.x_pos += self.speed
        elif self.direction == 1 and self.turns[1]:
            self.x_pos -= self.speed
        elif self.direction == 2 and self.turns[2]:
            self.y_pos -= self.speed
        elif self.direction == 3 and self.turns[3]:
            self.y_pos += self.speed

        if self.x_pos < -30:
            self.x_pos = self.WIDTH
        elif self.x_pos > self.WIDTH:
            self.x_pos = -30

        return self.x_pos, self.y_pos, self.direction
