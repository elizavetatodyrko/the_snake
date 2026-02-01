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

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """
    Базовый класс для всех игровых объектов.

    Attributes:
        position (tuple): Позиция объекта на игровом поле (x, y)
        body_color (tuple): Цвет объекта в формате RGB
    """

    def __init__(self, position=(0, 0), body_color=(0, 0, 0)):
        """
        Инициализирует базовые атрибуты объекта.
        
        Args:
            position (tuple): Позиция объекта (по умолчанию (0, 0))
            body_color (tuple): Цвет объекта (по умолчанию черный)
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """
        Метод для отрисовки объекта на поверхности.
        
        Args:
            surface: Поверхность для отрисовки (pygame.Surface)
            
        Note:
            Этот метод должен быть переопределен в дочерних классах.
        """
        raise NotImplementedError('Метод draw должен быть переопределен')


class Apple(GameObject):
    """
    Класс для представления яблока в игре.

    Attributes:
        field_size (tuple): Размер игрового поля (ширина, высота)
        body_color (tuple): Цвет яблока (красный)
    """

    def __init__(self, field_size, position=None):
        """
        Инициализирует яблоко.
        
        Args:
            field_size (tuple): Размер игрового поля
            position (tuple, optional): Начальная позиция яблока
        """
        super().__init__(body_color=APPLE_COLOR)
        self.field_size = field_size
        self.field_width, self.field_height = field_size
        
        if position:
            self.position = position
        else:
            self.randomize_position()
    
    def randomize_position(self):
        """Устанавливает случайную позицию яблока в пределах игрового поля."""
        x = randint(0, self.field_width - 1) * GRID_SIZE
        y = randint(0, self.field_height - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс для представления змейки в игре.

    Attributes:
        length (int): Длина змейки
        positions (list): Список позиций всех сегментов тела
        direction (tuple): Текущее направление движения
        next_direction (tuple): Следующее направление движения
        body_color (tuple): Цвет змейки (зеленый)
        last (tuple): Последняя позиция хвоста для затирания
    """

    def __init__(self, start_position, body_color=SNAKE_COLOR):
        """
        Инициализирует змейку.
        
        Args:
            start_position (tuple): Начальная позиция головы змейки
            body_color (tuple): Цвет змейки (по умолчанию зеленый)
        """
        super().__init__(position=start_position, body_color=body_color)
        self.length = 1
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки (движение)."""
        self.last = self.positions[-1] if self.positions else None
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head_x = head_x + dir_x * GRID_SIZE
        new_head_y = head_y + dir_y * GRID_SIZE
        
        # Телепортация через стены
        if new_head_x < 0:
            new_head_x = SCREEN_WIDTH - GRID_SIZE
        elif new_head_x >= SCREEN_WIDTH:
            new_head_x = 0
        if new_head_y < 0:
            new_head_y = SCREEN_HEIGHT - GRID_SIZE
        elif new_head_y >= SCREEN_HEIGHT:
            new_head_y = 0
            
        new_head = (new_head_x, new_head_y)
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        self.position = new_head

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        # Отрисовка тела змейки (все сегменты кроме головы)
        for position in self.positions[1:]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        if self.positions:
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки.

        Returns:
            tuple: Позиция головы змейки (x, y)
        """
        return self.positions[0] if self.positions else (0, 0)

    def reset(self, start_position):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [start_position]
        self.direction = RIGHT
        self.next_direction = None
        self.position = start_position
        self.last = None


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
    """
    Основная функция игры.
    
    Запускает игру и управляет основным игровым циклом.
    """
    pygame.init()
    
    field_size = (GRID_WIDTH, GRID_HEIGHT)
    start_position = (
        (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE,
        (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE,
    )
    
    snake = Snake(start_position)
    apple = Apple(field_size)
    
    while True:
        clock.tick(SPEED)
        
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if check_collision(snake, apple):
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        
        if check_self_collision(snake):
            snake.reset(start_position)
            apple.randomize_position()
        
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()