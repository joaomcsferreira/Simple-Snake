import pygame
from snake import *
from fruit import Fruit


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')

        # Display settings
        self.width, self.height = 800, 500
        self.FPS = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Game settings
        self.game_over = False

    def check_events(self):
        """ Function that checks events coming from the keyboard """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                quit()

    def run_game(self):
        while not self.game_over:
            # Sets speed of the snake
            self.FPS.tick(10)

            # Check keyboard events
            self.check_events()

            self.render_everything()
            pygame.display.update()

    def button(self, size, msg, x, y, w, h, rect, action):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            self.button_config(size, msg, x, y, w, h, rect, color=(255, 255, 255))
            if click[0] == 1 and action == 'run_game':
                new_screen = GameMain()
                new_screen.run_game()
            elif click[0] == 1 and action == 'exit':
                quit()
        else:
            self.button_config(size, msg, x, y, w, h, rect, color=(169, 169, 169))

    def button_config(self, size, msg, x, y, w, h, rect, color=(169, 169, 169)):
        """Renderiza as msg"""
        if rect:
            pygame.draw.rect(self.screen, color, [x, y, w, h])

        txt = pygame.font.Font('../ttf/PressStart2P-Regular.ttf', size)

        txt_surf = txt.render(msg, True, (0, 0, 0))
        txt_rect = txt_surf.get_rect()
        txt_rect.center = ((x + int(w / 2)), (y + int(h / 2)))

        self.screen.blit(txt_surf, txt_rect)

    def render_everything(self):
        self.screen.fill((0, 0, 0))


class GameLoad(Game):
    def __init__(self):
        super().__init__()

        # Background image
        self.background = pygame.image.load('../images/game_intro.png')

    def run_game(self):
        while not self.game_over:
            # Sets speed of the snake
            self.FPS.tick(10)

            # Check keyboard events
            self.check_events()

            self.render_everything()

            self.button(20, 'Play', 234, 380, 150, 50, True, 'run_game')
            self.button(20, 'Exit', 414, 380, 150, 50, True, 'exit')

            pygame.display.update()

    def render_everything(self):
        self.screen.blit(self.background, (0, 0))


class GameMain(Game):
    def __init__(self):
        super().__init__()

        # Snake settings
        self.snake = Snake(self.screen)

        # Snake bots settings
        self.snake_bot = SnakeBot(self.screen)
        self.snake_bot_2 = SnakeBot(self.screen)

        # Fruits settings
        self.fruit = Fruit(self.screen)

    def run_game(self):
        """ Main game loop """
        while not self.game_over:
            # Sets speed of the snake
            self.FPS.tick(10)

            # Check keyboard events
            self.check_events()

            # Checks for some kind of collision
            self.check_collisions()

            self.snake.move()

            # Starting AI bot
            self.snake_bot.initialize()
            self.snake_bot_2.initialize()

            # Renders everything
            self.render_everything()
            pygame.display.update()

    def check_events(self, move=True):
        """ Function that checks events coming from the keyboard """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
                break

            # Direction controls
            if move:
                self.snake.user_move(event)

    def check_collisions(self):
        """ Function that collects all collision checks """

        # Collision with itself
        if self.snake.collision_with_itself():
            self.game_over = True

        # check if one of the boats ate the fruit
        if self.snake.collision_with_bot(self.snake_bot) or self.snake.collision_with_bot(self.snake_bot_2):
            self.game_over = True

        # Check collision with boundaries
        if self.snake.collision_with_boundaries():
            self.game_over = True

        # Collision with a fruit
        if self.snake.eat_fruit(self.fruit):
            self.snake.grow_up(self.fruit)

        if self.snake_bot.eat_fruit(self.fruit) or self.snake_bot_2.eat_fruit(self.fruit):
            self.snake_bot.grow_up(self.fruit)
            self.snake_bot_2.grow_up(self.fruit)

        if self.game_over:
            new_screen = GameOver()
            new_screen.run_game()

    def render_everything(self):
        """ Function that brings together all renderings """
        self.screen.fill((0, 0, 0))
        self.fruit.render()
        self.snake.render()
        self.snake_bot.render()
        self.snake_bot_2.render()


class GameOver(Game):
    def __init__(self):
        super().__init__()

    def run_game(self):
        while not self.game_over:
            # Sets speed of the snake
            self.FPS.tick(10)

            # Check keyboard events
            self.check_events()

            self.render_everything()

            self.button(20, 'Play Again?', 274, 380, 250, 50, True, 'run_game')

            pygame.display.update()


if __name__ == '__main__':
    game = GameLoad()
    game.run_game()
