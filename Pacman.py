from board import boards
import pygame
import math
import copy
import heapq

pygame.init()

WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT], pygame.RESIZABLE | pygame.SCALED) 
timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('Arial', 20)  
level = copy.deepcopy(boards)
color = 'blue'
PI = math.pi
player_images = []
for i in range (1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (45, 45)))
blinky_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (45, 45))
pinky_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (45, 45))
inky_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (45, 45))
clyde_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (45, 45))
spooked_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (45, 45))
dead_images = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (45, 45))
player_x = 450
player_y = 663
direction = 0
blinky_x = 56
blinky_y = 58
blinky_direction = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
pinky_direction = 2
clyde_x = 440
clyde_y = 438
clyde_direction = 2
counter = 0
flicker = False
turn_allowed = [False, False, False, False]  # right, left, up, down
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
targets = [(player_x, player_y), (player_x, player_y), (player_x, player_y), (player_x, player_y)]
blinky_dead = False
pinky_dead = False
inky_dead = False
clyde_dead = False
blinky_box = False
pinky_box = False
inky_box = False
clyde_box = False
startup_counter = 0
moving = False
ghost_speeds = [2, 2, 2, 2]
lives = 3
game_over = False
game_won = False

class Ghost:
    def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id):
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
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw()

    def draw(self):
        if (not powerup and not self.dead) or (eaten_ghost[self.id] and powerup and not self.dead):
            screen.blit(self.img, (self.x_pos, self.y_pos))
        elif powerup and not self.dead and not eaten_ghost[self.id]:
            screen.blit(spooked_images, (self.x_pos, self.y_pos))
        else:
            screen.blit(dead_images, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect

    def check_collisions(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)
        num3 = 15
        self.turns = [False, False, False, False]
        if 0 < self.center_x // 30 < 29:
            if level[(self.center_y - num3) // num1][self.center_x // num2] == 9:
                self.turns[2] = True
            if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[1] = True
            if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                    or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[0] = True
            if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[3] = True
            if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                    or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                    self.in_box or self.dead)):
                self.turns[2] = True

            if self.direction == 2 or self.direction == 3:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num2) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num2) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[0] = True

            if self.direction == 0 or self.direction == 1:
                if 12 <= self.center_x % num2 <= 18:
                    if level[(self.center_y + num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y + num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[3] = True
                    if level[(self.center_y - num3) // num1][self.center_x // num2] < 3 \
                            or (level[(self.center_y - num3) // num1][self.center_x // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[2] = True
                if 12 <= self.center_y % num1 <= 18:
                    if level[self.center_y // num1][(self.center_x - num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x - num3) // num2] == 9 and (
                            self.in_box or self.dead)):
                        self.turns[1] = True
                    if level[self.center_y // num1][(self.center_x + num3) // num2] < 3 \
                            or (level[self.center_y // num1][(self.center_x + num3) // num2] == 9 and (
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

    def move_clyde(self):
        # r, l, u, d
        # clyde is going to turn whenever advantageous for pursuit
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
                if self.target[1] < self.y_pos and self.turns[2]:
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
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky(self):
        # r, l, u, d
        # blinky is going to turn whenever colliding with walls, otherwise continue straight
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
                self.x_pos += self.speed
        elif self.direction == 1:
            if self.target[0] < self.x_pos and self.turns[1]:
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
                self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
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
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.speed
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[2]:
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
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.speed
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.speed
            elif self.turns[3]:
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_blinky_astar(self):
        # Định nghĩa lưới biểu diễn, chia không gian toạ độ thành lưới các ô trong ma trận, có ở hàm collisions
        num1 = ((HEIGHT - 50) // 32)
        num2 = (WIDTH // 30)

        # Chuyển vị trí hiện tại sang tọa độ lưới
        current_x = self.center_x // num2
        current_y = self.center_y // num1

        # Chuyển vị trí mục tiêu (Pac-Man) sang tọa độ lưới
        target_x = self.target[0] // num2
        target_y = self.target[1] // num1

        # Triển khai thuật toán A*
        # Định nghĩa hàm heuristic, lấy khoảng cách manhattan
        def heuristic(a, b):
            # Khoảng cách Manhattan làm heuristic
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Các hướng di chuyển có thể (phải, trái, lên, xuống)
        neighbors = [(0, 1), (0, -1), (-1, 0), (1, 0)]

        # Hàng đợi ưu tiên cho tập mở, triển khai A* như khi làm trên giấy
        open_set = []
        heapq.heappush(open_set, (0, (current_x, current_y)))

        # Từ điển lưu đường đi và chi phí
        came_from = {}
        g_score = {(current_x, current_y): 0}
        f_score = {(current_x, current_y): heuristic((current_x, current_y), (target_x, target_y))}

        # Tập hợp theo dõi các nút trong tập mở
        open_set_hash = {(current_x, current_y)}

        while open_set:
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)

            # Nếu đã đến mục tiêu
            if current == (target_x, target_y):
                # Tái tạo đường đi
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                if path:
                    next_step = path[-1]  # Bước đầu tiên trong đường đi
                    # Xác định hướng dựa trên bước tiếp theo, dựa trên chênh lệch giữa x1,y1,x2,y2 mà đưa ra đường đi
                    if next_step[0] > current_x:
                        self.direction = 0  # phải
                    elif next_step[0] < current_x:
                        self.direction = 1  # trái
                    elif next_step[1] < current_y:
                        self.direction = 2  # lên
                    elif next_step[1] > current_y:
                        self.direction = 3  # xuống
                break

            for dx, dy in neighbors:
                # Dịch thử đên vị trí tiếp theo
                neighbor = (current[0] + dx, current[1] + dy)

                # Kiểm tra xem neighbor có trong biên và đi được không
                if 0 <= neighbor[0] < len(level[0]) and 0 <= neighbor[1] < len(level):
                    # Kiểm tra ô có đi được không (giá trị < 3 là đi được)
                    if level[neighbor[1]][neighbor[0]] >= 3 and not (self.in_box or self.dead):
                        continue

                    # Tính toán g score tạm thời
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, (target_x, target_y))
                        if neighbor not in open_set_hash:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))
                            open_set_hash.add(neighbor)

        if not hasattr(self, 'direction') or not self.turns[self.direction]:
            # Tìm hướng đi khả dụng đầu tiên, trong trường hợp không tìm được đường đi, đoạn này copy nguyên từ các hàm move có sẵn từ trước
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
                    self.x_pos += self.speed
            elif self.direction == 1:
                if self.target[0] < self.x_pos and self.turns[1]:
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
                    self.x_pos -= self.speed
            elif self.direction == 2:
                if self.target[1] < self.y_pos and self.turns[2]:
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
                    elif self.turns[3]:
                        self.direction = 3
                        self.y_pos += self.speed
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[2]:
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
                    elif self.turns[0]:
                        self.direction = 0
                        self.x_pos += self.speed
                    elif self.turns[1]:
                        self.direction = 1
                        self.x_pos -= self.speed
                elif self.turns[3]:
                    self.y_pos += self.speed
            # Có thể thay đoạn trên = đoạn này nhưng tui thấy khong hay bằng oạn code tác giả viết, do có phán đoán hướng đi dựa theo toạ độ hiện tại với toạ độ đích.
            #for i in range(4):
            #    if self.turns[i]:
            #        self.direction = i
            #    break
            else:
                # Nếu không có hướng nào khả dụng, đứng yên
                return self.x_pos, self.y_pos, self.direction

        # Di chuyển theo hướng đã chọn
        # Các hàm move cần trả về các giá trị self.x_pos, self.y_pos để phía dưới khi chương trình gọi
        # Trả về các giá trị trên thì mới render con ma lên mê cung tại vị trí nào
        if self.direction == 0 and self.turns[0]:
            self.x_pos += self.speed
        elif self.direction == 1 and self.turns[1]:
            self.x_pos -= self.speed
        elif self.direction == 2 and self.turns[2]:
            self.y_pos -= self.speed
        elif self.direction == 3 and self.turns[3]:
            self.y_pos += self.speed

        # Xử lý cuộn màn hình
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30

        return self.x_pos, self.y_pos, self.direction

    def move_inky(self):
        # r, l, u, d
        # inky turns up or down at any point to pursue, but left and right only on collision
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
                if self.target[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.speed
                else:
                    self.x_pos -= self.speed
        elif self.direction == 2:
            if self.target[1] < self.y_pos and self.turns[2]:
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
                self.y_pos += self.speed
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

    def move_pinky(self):
        # r, l, u, d
        # inky is going to turn left or right whenever advantageous, but only up or down on collision
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
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos - 30
        return self.x_pos, self.y_pos, self.direction

def draw_mics():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, HEIGHT - 40))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Game Over! Space bar to restart', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gamewon_text = font.render('Victory! Space bar to restart', True, 'green')
        screen.blit(gamewon_text, (100, 300))

def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white',(j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white',(j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (0.4 * num2)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + (0.5 * num2)), (i * num1 + (0.5 * num1)), num2, num1], PI/2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (0.5 * num2)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - (0.4 * num2)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)
            if level[i][j] == 9:     
                pygame.draw.line(screen,'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_player():
    # 0 -right, 1-left, 2-up, 3-down
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns

def move_player(play_x, play_y):
    # r, l, u, d
    if direction == 0 and turn_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turn_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turn_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turn_allowed[3]:
        play_y += player_speed
    return play_x, play_y

def check_collisions(scr, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scr += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scr += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scr, power, power_count, eaten_ghosts

def get_targets(blink_x, blink_y, ink_x, ink_y, pink_x, pink_y, clyd_x, clyd_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not blinky.dead and not eaten_ghost[0]:
            blink_target = (runaway_x, runaway_y)
        elif not blinky.dead and eaten_ghost[0]:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead and not eaten_ghost[1]:
            ink_target = (runaway_x, player_y)
        elif not inky.dead and eaten_ghost[1]:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            pink_target = (player_x, runaway_y)
        elif not pinky.dead and eaten_ghost[2]:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead and not eaten_ghost[3]:
            clyd_target = (450, 450)
        elif not clyde.dead and eaten_ghost[3]:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    else:
        if not blinky.dead:
            if 340 < blink_x < 560 and 340 < blink_y < 500:
                blink_target = (400, 100)
            else:
                blink_target = (player_x, player_y)
        else:
            blink_target = return_target
        if not inky.dead:
            if 340 < ink_x < 560 and 340 < ink_y < 500:
                ink_target = (400, 100)
            else:
                ink_target = (player_x, player_y)
        else:
            ink_target = return_target
        if not pinky.dead:
            if 340 < pink_x < 560 and 340 < pink_y < 500:
                pink_target = (400, 100)
            else:
                pink_target = (player_x, player_y)
        else:
            pink_target = return_target
        if not clyde.dead:
            if 340 < clyd_x < 560 and 340 < clyd_y < 500:
                clyd_target = (400, 100)
            else:
                clyd_target = (player_x, player_y)
        else:
            clyd_target = return_target
    return [blink_target, ink_target, pink_target, clyd_target]

run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 4:
            flicker = False
    else:
        counter = 0
        flicker = True
    if powerup and power_counter < 600:
        power_counter += 1
    elif powerup and power_counter >= 600:
        powerup = False
        power_counter = 0
        eaten_ghost = [False, False, False, False]
    if startup_counter < 180 and not game_over and not game_won:
        moving  = False
        startup_counter += 1
    else:
        moving = True

    screen.fill('black')
    draw_board()
    center_x = player_x + 23
    center_y = player_y + 24
    if powerup:
        ghost_speeds = [1, 1, 1, 1]
    else:
        ghost_speeds = [2, 0, 0, 0]
    if eaten_ghost[0]:
        ghost_speeds[0] = 2
    if eaten_ghost[1]:
        ghost_speeds[1] = 2
    if eaten_ghost[2]:
        ghost_speeds[2] = 2
    if eaten_ghost[3]:
        ghost_speeds[3] = 2
    if blinky_dead:
        ghost_speeds[0] = 4
    if inky_dead:
        ghost_speeds[1] = 4
    if pinky_dead:
        ghost_speeds[2] = 4
    if clyde_dead:
        ghost_speeds[3] = 4
    game_won = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[i]:
            game_won = False
    player_circle = pygame.draw.circle(screen, 'purple', (center_x, center_y), 20, 2)
    draw_player()
    blinky = Ghost(blinky_x, blinky_y, targets[0], ghost_speeds[0], blinky_images, blinky_direction, blinky_dead, blinky_box, 0)
    inky = Ghost(inky_x, inky_y, targets[1], ghost_speeds[1], inky_images, inky_direction, inky_dead, inky_box, 1)
    pinky = Ghost(pinky_x, pinky_y, targets[2], ghost_speeds[2], pinky_images, pinky_direction, pinky_dead, pinky_box, 2)
    clyde = Ghost(clyde_x, clyde_y, targets[3], ghost_speeds[3], clyde_images, clyde_direction, clyde_dead, clyde_box, 3)
    draw_mics()
    targets = get_targets(blinky_x, blinky_y, inky_x, inky_y, pinky_x, pinky_y, clyde_x, clyde_y)
    turn_allowed = check_position(center_x, center_y)
    if moving:
        player_x, player_y = move_player(player_x, player_y)
        if not blinky.dead and not blinky.in_box:
            blinky_x, blinky_y, blinky_direction = blinky.move_blinky_astar()  # Đổi từ move_blinky()
        else:
            blinky_x, blinky_y, blinky_direction = blinky.move_clyde()

        #if not blinky.dead and not blinky.in_box:
        #    blinky_x, blinky_y, blinky_direction = blinky.move_blinky()
        #else:
        #    blinky_x, blinky_y, blinky_direction = blinky.move_clyde()

        if not inky.dead and not inky.in_box:
            inky_x, inky_y, inky_direction = inky.move_inky()
        else:
            inky_x, inky_y, inky_direction = inky.move_clyde()
        if not pinky.dead and not pinky.in_box:
            pinky_x, pinky_y, pinky_direction = pinky.move_pinky()
        else:
            pinky_x, pinky_y, pinky_direction = pinky.move_clyde()
        clyde_x, clyde_y, clyde_direction = clyde.move_clyde()
    score, powerup, power_counter, eaten_ghost = check_collisions(score, powerup, power_counter, eaten_ghost)

    if not powerup:
        if(player_circle.colliderect(blinky.rect) and not blinky.dead) or \
                (player_circle.colliderect(inky.rect) and not inky.dead) or \
                (player_circle.colliderect(pinky.rect) and not pinky.dead) or \
                (player_circle.colliderect(clyde.rect) and not clyde.dead):
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and eaten_ghost[0] and not blinky.dead:
            if lives > 0:
                lives -= 1
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
    if powerup and player_circle.colliderect(inky.rect) and eaten_ghost[1] and not inky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            pinky_dead = False
            inky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(pinky.rect) and eaten_ghost[2] and not pinky.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            pinky_dead = False
            inky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(clyde.rect) and eaten_ghost[3] and not clyde.dead:
        if lives > 0:
            lives -= 1
            startup_counter = 0
            powerup = False
            power_counter = 0
            player_x = 450
            player_y = 663
            direction = 0
            blinky_x = 56
            blinky_y = 58
            blinky_direction = 0
            inky_x = 440
            inky_y = 388
            inky_direction = 2
            pinky_x = 440
            pinky_y = 438
            pinky_direction = 2
            clyde_x = 440
            clyde_y = 438
            clyde_direction = 2
            eaten_ghost = [False, False, False, False]
            blinky_dead = False
            pinky_dead = False
            inky_dead = False
            clyde_dead = False
        else:
            game_over = True
            moving = False
            startup_counter = 0
    if powerup and player_circle.colliderect(blinky.rect) and not blinky.dead and not eaten_ghost[0]:
        blinky_dead = True
        eaten_ghost[0] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(inky.rect) and not inky.dead and not eaten_ghost[1]:
        inky_dead = True
        eaten_ghost[1] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(pinky.rect) and not pinky.dead and not eaten_ghost[2]:
        pinky_dead = True
        eaten_ghost[2] = True
        score += (2 ** eaten_ghost.count(True)) * 100
    if powerup and player_circle.colliderect(clyde.rect) and not clyde.dead and not eaten_ghost[3]:
        clyde_dead = True
        eaten_ghost[3] = True
        score += (2 ** eaten_ghost.count(True)) * 100   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction_command = 0
            if event.key == pygame.K_LEFT:
                direction_command = 1
            if event.key == pygame.K_UP:
                direction_command = 2
            if event.key == pygame.K_DOWN:
                direction_command = 3
            if event.key == pygame.K_SPACE and (game_over or game_won):
                startup_counter = 0
                powerup = False
                power_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                blinky_x = 56
                blinky_y = 58
                blinky_direction = 0
                inky_x = 440
                inky_y = 388
                inky_direction = 2
                pinky_x = 440
                pinky_y = 438
                pinky_direction = 2
                clyde_x = 440
                clyde_y = 438
                clyde_direction = 2
                eaten_ghost = [False, False, False, False]
                blinky_dead = False
                pinky_dead = False
                inky_dead = False
                clyde_dead = False
                score = 0
                lives = 3
                level = copy.deepcopy(boards)
                game_over = False
                game_won = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and direction_command == 0:
                direction_command = 0
            if event.key == pygame.K_LEFT and direction_command == 1:
                direction_command = 1
            if event.key == pygame.K_UP and direction_command == 2:
                direction_command = 2
            if event.key == pygame.K_DOWN and direction_command == 3:
                direction_command = 3
    for i in range(4):
        if direction_command == i and turn_allowed[i]:
            direction = i
    if player_x > WIDTH:
        player_x = -47
    elif  player_x < -50:
        player_x = WIDTH - 3
    if blinky.in_box and blinky_dead:
        blinky_dead = False
    if inky.in_box and inky_dead:
        inky_dead = False
    if pinky.in_box and pinky_dead:
        pinky_dead = False
    if clyde.in_box and clyde_dead:
        clyde_dead = False

    pygame.display.flip()
pygame.quit()