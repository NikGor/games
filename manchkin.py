import random
import datetime


class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.inventory = []

    @property
    def strength(self):
        total_bonus = 0
        # Вычисляем силу на основе бонусов сокровищ в инвентаре
        if self.inventory:
            total_bonus = sum(item.bonus for item in self.inventory)
        return total_bonus


class Monster:
    def __init__(self, name, level, treasure):
        self.name = name
        self.level = level
        self.treasure = treasure


class Treasure:
    def __init__(self, name, bonus):
        self.name = name
        self.bonus = bonus


def write_log(player1, player2):
    with open(filename, 'a') as logfile:
        logfile.write(f"{player1.level}, {player1.strength}, {player2.level}, {player2.strength}\n")


start_time = datetime.datetime.now()
filename = f"{start_time.strftime('%Y%m%d%H%M%S')}_start.txt"
with open(filename, 'w') as logfile:
    logfile.write("Player 1 Level, Player 1 Strength, Player 2 Level, Player 2 Strength\n")

# Создаем игроков
player1 = Player("Игрок 1")
player2 = Player("Игрок 2")

# Создаем сокровища
treasures = [
    Treasure("Зелье силы", 1),
    Treasure("Зелье здоровья", 1),
    Treasure("Медная монета", 1),
    Treasure("Серебряная монета", 1),
    Treasure("Золотая монета", 1),
    Treasure("Старый меч", 1),
    Treasure("Старая броня", 1),
    Treasure("Подкова", 1),
    Treasure("Магический свиток", 2),
    Treasure("Драгоценный камень", 2),
    Treasure("Деревянный амулет", 2),
    Treasure("Шкатулка", 2),
    Treasure("Золотая корона", 3),
    Treasure("Драгоценное ожерелье", 3),
    Treasure("Легендарный артефакт", 5)
]

# Начало игры
print("Добро пожаловать в Манчкин!")
print(f"{player1.name} и {player2.name}, ваша цель - достичь 10 уровня и победить!")

current_player = player1
other_player = player2

while True:
    print(f"\nХод игрока {current_player.name} (Уровень: {current_player.level}, Сила: {current_player.strength})")

    action = input("Выберите действие: (1) Сражаться с монстром, (2) Забрать сокровище: ")

    # Создаем монстров
    strength_coefficient = 1 if current_player.strength == 0 else current_player.strength
    monster_levels = [
        1,
        2,
        3,
        current_player.level * 2,
        current_player.level * 3,
        current_player.level * 4,
        current_player.level + random.randint(1, int(strength_coefficient * 1.5)),
        current_player.level + random.randint(1, int(strength_coefficient * 1.75)),
        current_player.level * 5,
        current_player.level + random.randint(1, int(strength_coefficient * 2)),
    ]

    monsters = [
        Monster("Травка", monster_levels[0], Treasure("Подорожник", 1)),
        Monster("Скелет", monster_levels[1], Treasure("Старинный череп", 1)),
        Monster("Вурдалак", monster_levels[3], Treasure("Зонтик от солнца", 1)),
        Monster("Дракон", monster_levels[2], Treasure("Горшок Золота", 2)),
        Monster("Орк", monster_levels[4], Treasure("Топор орка", 2)),
        Monster("Зомби", monster_levels[6], Treasure("Гнилая повязка", 2)),
        Monster("Кобольд", monster_levels[5], Treasure("Изношенный щит", 3)),
        Monster("Гарпия", monster_levels[7], Treasure("Перо гарпии", 3)),
        Monster("Ведьма", monster_levels[8], Treasure("Зелье здоровья", 4)),
        Monster("Минотавр", monster_levels[9], Treasure("Минотавров рог", 5))
    ]

    if action == "1":
        monster = random.choice(monsters)
        print(f"Вы встретили монстра: {monster.name} (Уровень: {monster.level})")

        if current_player.strength + current_player.level >= monster.level:
            print("Победа! Вы получаете сокровище:")
            print(f"- {monster.treasure.name} (Бонус: {monster.treasure.bonus})")
            current_player.level += 1
            print(f"Ваш уровень повышен! Новый уровень: {current_player.level}")
            current_player.inventory.append(monster.treasure)
            print(f"Ваша сила: {current_player.strength}")
            print("Ваш инвентарь:")
            for item in current_player.inventory:
                print(f"- {item.name} (Бонус: {item.bonus})")
        else:
            if current_player.inventory:
                num_lost_treasures = random.randint(1, len(current_player.inventory))
                lost_treasures = random.sample(current_player.inventory, num_lost_treasures)
                for treasure in lost_treasures:
                    current_player.inventory.remove(treasure)
                print(f"Поражение! Вы теряете уровень и {num_lost_treasures} сокровищ(а) из инвентаря.")
                current_player.level -= 1
                print(f"Новый уровень: {current_player.level}")
                print(f"Ваша сила: {current_player.strength}")
                print("Ваш инвентарь:")
                for item in current_player.inventory:
                    print(f"- {item.name} (Бонус: {item.bonus})")
            else:
                print(f"Поражение! Вы теряете уровень, но у вас нет сокровищ для потери.")
                current_player.level -= 1
                print(f"Новый уровень: {current_player.level}")
                print(f"Ваша сила: {current_player.strength}")

    if action == "2":
        chosen_treasure = random.choice(treasures)
        print(f"Вы получили сокровище: {chosen_treasure.name} (Бонус: {chosen_treasure.bonus})")
        current_player.inventory.append(chosen_treasure)
        print(f"Ваша сила: {current_player.strength}")
        print("Ваш инвентарь:")
        for item in current_player.inventory:
            print(f"- {item.name} (Бонус: {item.bonus})")

    write_log(player1, player2)

    if current_player.level < 1:
        print(f"Очень жаль, {current_player.name}! Вы проиграли!")
        break
    elif current_player.level >= 10:
        print(f"Поздравляем, {current_player.name}! Вы достигли 10 уровня и победили!")
        break

    current_player, other_player = other_player, current_player