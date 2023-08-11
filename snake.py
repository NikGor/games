import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 320, 240
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Задержка обновления экрана (скорость змейки)
clock = pygame.time.Clock()
FPS = 9


class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.change_to = self.direction

    def change_direction(self, new_dir):
        if new_dir == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if new_dir == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if new_dir == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if new_dir == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def move(self, food_pos):
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "RIGHT":
            self.position[0] += 10

        self.body.insert(0, list(self.position))

        if self.position[0] == food_pos[0] and self.position[1] == food_pos[1]:
            return True
        else:
            self.body.pop()
            return False

    def check_collision(self):
        if self.position[0] >= WIDTH or self.position[0] <= 0 \
                or self.position[1] >= HEIGHT or self.position[1] <= 0:
            return True

        for segment in self.body[1:]:
            if segment == self.position:
                return True

        return False

    def get_head_position(self):
        return self.position

    def get_body(self):
        return self.body


class Food:
    def __init__(self):
        self.position = [random.randrange(1, (WIDTH // 10)) * 10,
                         random.randrange(1, (HEIGHT // 10)) * 10]
        self.is_food_on_screen = True

    def spawn_food(self):
        if not self.is_food_on_screen:
            self.position = [random.randrange(1, (WIDTH // 10)) * 10,
                             random.randrange(1, (HEIGHT // 10)) * 10]
            self.is_food_on_screen = True
        return self.position

    def set_food_on_screen(self, choice):
        self.is_food_on_screen = choice


def draw_objects(win, snake, food):
    win.fill(WHITE)

    for pos in snake.get_body():
        pygame.draw.rect(win, GREEN, pygame.Rect(
            pos[0], pos[1], 10, 10))

    pygame.draw.rect(win, RED, pygame.Rect(
        food.position[0], food.position[1], 10, 10))

    pygame.display.update()


def main():
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_UP]:
                    snake.change_direction("UP")
                if keys[pygame.K_DOWN]:
                    snake.change_direction("DOWN")
                if keys[pygame.K_LEFT]:
                    snake.change_direction("LEFT")
                if keys[pygame.K_RIGHT]:
                    snake.change_direction("RIGHT")

        food_pos = food.spawn_food()
        if snake.move(food_pos):
            food.set_food_on_screen(False)

        if snake.check_collision():
            break

        draw_objects(win, snake, food)
        clock.tick(FPS)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
