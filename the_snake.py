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

# Цвет фона - чёрный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

DEFAULT_POSITIONS = (0, 0)
DEFAULT_COLOR = (0, 0, 0)

# Настройка игрового окна:
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=DEFAULT_POSITIONS, body_color=DEFAULT_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает игровой объект."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, position=DEFAULT_POSITIONS):
        super().__init__(
            position=position,
            body_color=APPLE_COLOR
        )

    def randomize_position(self, snake_positions):
        """Устанавливает яблоко в случайную позицию, не занятую змейкой."""
        while True:
            new_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            new_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (new_x, new_y)

            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE)
        )

        pygame.draw.rect(
            screen,
            self.body_color,
            rect
        )

        pygame.draw.rect(
            screen,
            BORDER_COLOR,
            rect,
            1
        )


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, position=DEFAULT_POSITIONS):
        super().__init__(
            position=position,
            body_color=SNAKE_COLOR
        )
        self._reset_state(position)

    def _reset_state(self, position):
        """Устанавливает начальное состояние змейки."""
        self.length = 1
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещает змейку на одну ячейку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head_x = (
            head_x + direction_x * GRID_SIZE
        ) % SCREEN_WIDTH

        new_head_y = (
            head_y + direction_y * GRID_SIZE
        ) % SCREEN_HEIGHT

        new_head = (new_head_x, new_head_y)

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает все сегменты змейки."""
        for position in self.positions:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE)
            )

            pygame.draw.rect(
                screen,
                self.body_color,
                rect
            )

            pygame.draw.rect(
                screen,
                BORDER_COLOR,
                rect,
                1
            )

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self._reset_state(
            (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2
            )
        )


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_UP
                and game_object.direction != DOWN
            ):
                game_object.next_direction = UP

            elif (
                event.key == pygame.K_DOWN
                and game_object.direction != UP
            ):
                game_object.next_direction = DOWN

            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT

            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Запускает игру и управляет игровым циклом."""
    pygame.init()

    snake = Snake(
        (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
    )

    apple = Apple((0, 0))
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)

        # Обработка действий пользователя.
        handle_keys(snake)

        # Обновление направления.
        snake.update_direction()

        # Движение змейки.
        snake.move()

        # Проверка поедания яблока.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с собой.
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        # Очистка экрана.
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка объектов.
        apple.draw()
        snake.draw()

        # Обновление экрана.
        pygame.display.update()


if __name__ == '__main__':
    main()