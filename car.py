import pygame
import math

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 1024, 768
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Управляемая машинка")

# Цвета
WHITE = (255, 255, 255)
BLACK = (100, 100, 100)
GREEN = (0, 255, 0)

# Задержка обновления экрана
clock = pygame.time.Clock()
FPS = 60

class Car:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.width = 80
        self.height = 40
        self.angle = 0
        self.speed = 0
        self.acceleration = 0.1
        self.accelerate = 1  # Ускорение при удержании клавиши
        self.max_speed = 20
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLACK, (0, 0, self.width, self.height))
        self.original_image = self.image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collided = False


    def update(self):
        # Если машина не столкнулась с границей, обрабатываем ввод с клавиатуры
        keys = pygame.key.get_pressed()
        if not self.collided:
            if keys[pygame.K_UP]:
                self.speed += self.acceleration
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
            if keys[pygame.K_DOWN]:
                self.speed -= self.acceleration
                if self.speed < -self.max_speed:
                    self.speed = -self.max_speed

            if keys[pygame.K_LEFT]:
                self.angle += 4

            if keys[pygame.K_RIGHT]:
                self.angle -= 4

        # Затухание скорости из-за трения
        self.speed -= self.speed * 0.01

        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y -= self.speed * math.sin(math.radians(self.angle))

        # Ограничиваем положение машины в пределах экрана
        if self.x - self.width/2 < 0:
            self.x = self.width/2
        elif self.x + self.width/2 > WIDTH:
            self.x = WIDTH - self.width/2

        if self.y - self.height/2 < 0:
            self.y = self.height/2
        elif self.y + self.height/2 > HEIGHT:
            self.y = HEIGHT - self.height/2

        self.rotate_car()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def rotate_car(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


def main():
    car = Car()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        car.update()

        win.fill(WHITE)
        win.blit(car.image, car.rect.topleft)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
