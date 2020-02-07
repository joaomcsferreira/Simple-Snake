import pygame
from snake import *
from fruit import Fruit


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')

        # Display settings
        self.width = 800
        self.height = 600
        self.FPS = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Snake settings
        self.snake = Snake(self.screen)

        # Snake bots settings
        self.snake_bot = SnakeBot(self.screen)
        self.snake_bot_2 = SnakeBot(self.screen)

        # Fruits settings
        self.fruit = Fruit(self.screen)

        # Game settings
        self.game_over = False

    def run_game(self):
        """ Main game loop """
        while not self.game_over:
            # Sets speed of the snake
            self.FPS.tick(10)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    quit()

                # Direction controls
                self.snake.user_move(event)

            # Collision with itself
            if self.snake.collision_with_itself():
                self.game_over = True
                quit()

            if self.snake.collision_with_bot(self.snake_bot) or self.snake.collision_with_bot(self.snake_bot_2):
                quit()

            # Collision with boundaries
            self.game_over = self.snake.collision_with_boundaries()

            # Collision with a fruit
            if self.snake.eat_fruit(self.fruit):
                self.snake.grow_up(self.fruit)

            if self.snake_bot.eat_fruit(self.fruit) or self.snake_bot_2.eat_fruit(self.fruit):
                self.snake_bot.grow_up(self.fruit)
                self.snake_bot_2.grow_up(self.fruit)

            self.snake.move()

            # Starting AI bot
            self.snake_bot.initialize()
            self.snake_bot_2.initialize()

            self.screen.fill((0, 0, 0))
            self.fruit.render()
            self.snake.render()
            self.snake_bot.render()
            self.snake_bot_2.render()
            pygame.display.update()

        if self.game_over:
            pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run_game()
