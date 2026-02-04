from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Координаты центра экрана
CENTER_X = (GRID_WIDTH // 2) * GRID_SIZE
CENTER_Y = (GRID_HEIGHT // 2) * GRID_SIZE
CENTER_POSITION = (CENTER_X, CENTER_Y)

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """
        Инициализирует базовые атрибуты объекта.
        Args:
            body_color (tuple): Цвет объекта (по умолчанию цвет фона)
        """
        self.position = CENTER_POSITION
        self.body_color = body_color

    def draw(self):
        """
        Метод для отрисовки объекта на поверхности.
        Note:
            Этот метод должен быть переопределен в дочерних классах.
        """
        raise NotImplementedError('Метод draw должен быть переопределен')


class Apple(GameObject):
    """Класс для представления яблока в игре."""

    def __init__(self, body_color=APPLE_COLOR):
        """
        Инициализирует яблоко.
        Args:
            body_color (tuple): Цвет яблока (по умолчанию APPLE_COLOR)
        """
        super().__init__(body_color=body_color)
        self.randomize_position()

    def randomize_position(self, occupied_positions=None):
        """Устанавливает случайную позицию яблока в пределах игрового поля."""
        if occupied_positions is None:
            occupied_positions = [CENTER_POSITION]
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для представления змейки в игре."""

    def __init__(self, body_color=SNAKE_COLOR):
        """
        Инициализирует змейку.
        Args:
            body_color (tuple): Цвет змейки (по умолчанию зеленый)
        """
        super().__init__(body_color=body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (движение)."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.
    Args:
        game_object (Snake): Объект змейки, для которого обрабатываются клавиши
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def check_collision(snake, apple):
    """
    Проверяет, съела ли змейка яблоко.
    Args:
        snake (Snake): Объект змейки
        apple (Apple): Объект яблока
    Returns:
        bool: True если змейка съела яблоко, иначе False
    """
    return snake.get_head_position() == apple.position


def check_self_collision(snake):
    """
    Проверяет, столкнулась ли змейка с самой собой.
    Args:
        snake (Snake): Объект змейки
    Returns:
        bool: True если змейка столкнулась с собой, иначе False
    """
    head_position = snake.get_head_position()
    return head_position in snake.positions[1:]


def main():
    """Основная функция игры."""
    pygame.init()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if check_collision(snake, apple):
            snake.length += 1
            apple.randomize_position()
        elif check_self_collision(snake):
            snake.reset()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
