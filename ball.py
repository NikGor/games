import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("шарики")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOUR = (0, 0, 0)

# Задержка обновления экрана
clock = pygame.time.Clock()
FPS = 60

MAX_SPEED = 50

class Ball:
    def __init__(self, x, y, size, mass):
        self.x = x
        self.y = y
        self.size = size
        self.mass = mass
        self.radius = size
        self.angle = random.uniform(0, 360)
        self.speed = 2
        self.acceleration = 0.3

    def update(self, balls):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        if keys[pygame.K_DOWN]:
            self.speed -= self.acceleration
            self.speed = max(self.speed, 0)

        if keys[pygame.K_LEFT]:
            self.angle += 3

        if keys[pygame.K_RIGHT]:
            self.angle -= 3

        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        self.handle_collision(balls)

        friction_coefficient = 0.993  # Коэффициент трения
        self.speed *= friction_coefficient
        
        if self.x < self.radius:
            self.x = self.radius
            self.angle = 180 - self.angle
        if self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.angle = 180 - self.angle
        if self.y < self.radius:
            self.y = self.radius
            self.angle = -self.angle
        if self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.angle = -self.angle

    def handle_collision(self, balls):
        for ball in balls:
            if ball != self:
                dx = self.x - ball.x
                dy = self.y - ball.y
                distance = math.sqrt(dx ** 2 + dy ** 2)

                if distance < self.radius + ball.radius:
                    angle = math.atan2(dy, dx)
                    total_mass = self.mass + ball.mass

                    # Рассчет новых скоростей
                    self_speed = self.speed
                    ball_speed = ball.speed

                    self_new_speed = ((self_speed * (self.mass - ball.mass) + 2 * ball.mass * ball_speed) / total_mass)
                    ball_new_speed = ((ball_speed * (ball.mass - self.mass) + 2 * self.mass * self_speed) / total_mass)

                    # Применение новых скоростей
                    self.speed = self_new_speed
                    ball.speed = ball_new_speed

                    # Расчет угла разлета
                    self.angle = math.degrees(angle)
                    ball.angle = math.degrees(angle) + 180

                    # Перемещение шаров так, чтобы они не перекрывались
                    overlap = (self.radius + ball.radius - distance + 1) * 0.5
                    self.x += overlap * math.cos(angle)
                    self.y += overlap * math.sin(angle)
                    ball.x -= overlap * math.cos(angle)
                    ball.y -= overlap * math.sin(angle)


    def draw(self, surface):
        pygame.draw.circle(surface, COLOUR, (int(self.x), int(self.y)), self.radius, width=2)

def create_balls(num_balls):
    balls = []
    for _ in range(num_balls):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
 #       size = random.randint(10, 50)
        size = 40
#       mass = size * random.uniform(0.01, 1)
        mass = random.randint(10, 500)
        ball = Ball(x, y, size, mass)
        balls.append(ball)
    return balls

def main():
    balls = create_balls(3)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for ball in balls:
            ball.update(balls)

        win.fill(WHITE)
        for ball in balls:
            ball.draw(win)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
