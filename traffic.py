import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Траффик")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Задержка обновления экрана
clock = pygame.time.Clock()
FPS = 60

class Car:
    def __init__(self, lane, speed):
        self.lane = lane
        self.y = self.lane * 100 + 50
        self.x = -50  # Начальная позиция за пределами экрана
        self.speed = speed
        self.distance_threshold = 150  # Дистанция для снижения скорости

    def update(self, cars):
        self.x += self.speed

        for car in cars:
            if car != self and car.lane == self.lane:
                distance = car.x - self.x
                if 0 < distance < self.distance_threshold:
                    self.speed = min(self.speed, car.speed)

        if self.x > WIDTH:
            self.x = -50
            self.speed = random.uniform(3, 5)  # Рандомная скорость при появлении

    def draw(self, surface):
        pygame.draw.rect(surface, BLACK, (self.x, self.y, 50, 30))

def main():
    cars = []
    next_car_time = time.time() + random.uniform(0.5, 2.0)  # Время появления следующей машинки
    lane = random.randint(0, 1)  # Начальная полоса
    num_cars = 10  # Максимальное количество машинок в каждой полосе

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Создание новой машинки с неравномерной генерацией
        if time.time() > next_car_time and len(cars) < num_cars:
            car = Car(lane, random.uniform(1, 5))
            cars.append(car)
            next_car_time = time.time() + random.uniform(0.5, 2.0)
            lane = 1 - lane  # Переключение полосы

        for car in cars:
            car.update(cars)

        win.fill(WHITE)
        for car in cars:
            car.draw(win)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()
