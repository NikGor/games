import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
CELL_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 10, 10
WIDTH, HEIGHT = GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Общий класс для всех персонажей
class Character:
    def __init__(self, grid_x, grid_y, color):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = grid_y * CELL_SIZE + CELL_SIZE // 2
        self.color = color

    def move(self, dx, dy):
        self.grid_x += dx
        self.grid_y += dy
        self.x = self.grid_x * CELL_SIZE + CELL_SIZE // 2
        self.y = self.grid_y * CELL_SIZE + CELL_SIZE // 2

        # Обработка краев экрана
        if self.grid_x < 0:
            self.grid_x = 0
        if self.grid_x >= GRID_WIDTH:
            self.grid_x = GRID_WIDTH - 1
        if self.grid_y < 0:
            self.grid_y = 0
        if self.grid_y >= GRID_HEIGHT:
            self.grid_y = GRID_HEIGHT - 1

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), CELL_SIZE // 2)

# Класс для Пакмана
class Pacman(Character):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, YELLOW)

# Класс для призраков
class Ghost(Character):
    def __init__(self, grid_x, grid_y, color, move_behavior, vertical_direction):
        super().__init__(grid_x, grid_y, color)
        self.move_behavior = move_behavior
        self.move_counter = 0  # Счетчик для задержки движения
        self.vertical_direction = vertical_direction

    def move(self):
        self.move_behavior(self)

# Функция для вертикального движения призрака
def vertical_move(ghost):
    ghost.move_counter += 1
    if ghost.move_counter >= 10:
        ghost.move_counter = 0
        ghost.grid_y += ghost.vertical_direction

        # Обработка краев экрана
        if ghost.grid_y < 0:
            ghost.grid_y = 0
            ghost.vertical_direction = 1
        if ghost.grid_y >= GRID_HEIGHT:
            ghost.grid_y = GRID_HEIGHT - 1
            ghost.vertical_direction = -1

        ghost.x = ghost.grid_x * CELL_SIZE + CELL_SIZE // 2
        ghost.y = ghost.grid_y * CELL_SIZE + CELL_SIZE // 2


# Класс для точек
class Dot:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y

    def draw(self):
        pygame.draw.circle(win, BLACK, (self.grid_x * CELL_SIZE + CELL_SIZE // 2, self.grid_y * CELL_SIZE + CELL_SIZE // 2), 5)

# Создание Пакмана
pacman = Pacman(GRID_WIDTH // 2, GRID_HEIGHT // 2)

# Создание охотника-призрака
ghosts = [
    Ghost(0, GRID_HEIGHT // 2, RED, vertical_move, 1),  # Первый призрак двигается вниз
    Ghost(GRID_WIDTH - 1, GRID_HEIGHT // 2, (0, 255, 0), vertical_move, -1)  # Второй призрак двигается вверх
]

# Создание точек
dots = [Dot(random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)) for _ in range(10)]

# Управление FPS
clock = pygame.time.Clock()
FPS = 10

# Создание игрового цикла
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Получение текущего состояния клавиш
        keys = pygame.key.get_pressed()

        # Обработка движения Пакмана
        if keys[pygame.K_LEFT]:
            pacman.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            pacman.move(1, 0)
        if keys[pygame.K_UP]:
            pacman.move(0, -1)
        if keys[pygame.K_DOWN]:
            pacman.move(0, 1)

        # Обработка движения охотников-призраков
        for ghost in ghosts:
            ghost.move()

        # Проверка столкновения с точками
        eaten_dots = []
        for dot in dots:
            if pacman.grid_x == dot.grid_x and pacman.grid_y == dot.grid_y:
                eaten_dots.append(dot)
        for dot in eaten_dots:
            dots.remove(dot)

        # Проверка окончания игры
        if len(dots) == 0:
            game_over = True
            game_result = "Win"
        for ghost in ghosts:
            if pacman.grid_x == ghost.grid_x and pacman.grid_y == ghost.grid_y:
                game_over = True
                game_result = "Game Over!"

    # Отрисовка
    win.fill(WHITE)
    for dot in dots:
        dot.draw()
    pacman.draw()
    ghost.draw()

    # Отрисовка сетки
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(win, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(win, BLACK, (0, y), (WIDTH, y))

    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render(game_result, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        win.blit(text, text_rect)

    pygame.display.update()

    # Управление FPS
    clock.tick(FPS)

pygame.quit()
