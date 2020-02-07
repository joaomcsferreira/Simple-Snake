import pygame
from random import choice


class Snake:
    def __init__(self, screen):
        """ A simple idea of a snake """
        self.screen = screen

        # Snake settings
        self.body = [(200, 200)]
        self.color = (0, 200, 0)
        self.surface = pygame.Surface((15, 15))
        self.surface.fill(self.color)

        # Movement constants
        self.UP, self.DOWN, self.LEFT, self.RIGHT = 1, 2, 3, 4
        self.my_direction = self.RIGHT

    def move(self):
        """ Function that actually makes the account move, updates the coordinates """
        for pos in range(len(self.body) - 1, 0, -1):
            self.body[pos] = self.body[pos - 1][0], self.body[pos - 1][1]

        if self.my_direction == self.UP:
            self.body[0] = self.body[0][0], self.body[0][1] - 20
        elif self.my_direction == self.DOWN:
            self.body[0] = self.body[0][0], self.body[0][1] + 20
        elif self.my_direction == self.LEFT:
            self.body[0] = self.body[0][0] - 20, self.body[0][1]
        elif self.my_direction == self.RIGHT:
            self.body[0] = self.body[0][0] + 20, self.body[0][1]

    def user_move(self, event):
        """ Controls direction according to keyboard actions """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and self.my_direction != self.DOWN:
                self.my_direction = self.UP
            if event.key == pygame.K_DOWN and self.my_direction != self.UP:
                self.my_direction = self.DOWN
            if event.key == pygame.K_LEFT and self.my_direction != self.RIGHT:
                self.my_direction = self.LEFT
            if event.key == pygame.K_RIGHT and self.my_direction != self.LEFT:
                self.my_direction = self.RIGHT

    def collision_with_boundaries(self):
        """ Check if snake collided with boundaries """
        if self.body[0][0] == 800 or self.body[0][1] == 600 or self.body[0][0] < 0 or self.body[0][1] < 0:
            return True
        else:
            return False

    def collision_with_itself(self):
        """ Check if the snake has hit itself """
        for pos in range(1, len(self.body)):
            if self.body[0][0] == self.body[pos][0] and self.body[0][1] == self.body[pos][1]:
                return True

    def collision_with_bot(self, bot):
        for pos in bot.body:
            if self.body[0][0] == pos[0] and self.body[0][1] == pos[1]:
                return True

    def eat_fruit(self, fruit):
        """ Checks if there is a collision between the fruit and the snake """
        if self.body[0][0] == fruit.position[0] and self.body[0][1] == fruit.position[1]:
            return True
        else:
            return False

    def grow_up(self, fruit):
        """ Responsible for the snake's growth """
        self.body.append((self.body[-1][0], self.body[-1][1]))
        fruit.update()

    def render(self):
        """ Draws each part of the snake's turn on the screen """
        for pos in self.body:
            self.screen.blit(self.surface, pos)


class SnakeBot(Snake):
    def __init__(self, screen):
        super().__init__(screen)

        # Snake settings
        self.body = [(600, 200), (620, 200), (640, 200)]
        self.color = (255, 255, 255)
        self.surface.fill(self.color)

        # Time constant
        self.cont = 0

        # Movement settings
        self.my_direction = self.LEFT
        self.direction_choice = [self.UP, self.DOWN, self.LEFT, self.RIGHT]

    def user_move(self, event=0):
        self.cont = self.cont + 1

        if self.cont == 10:
            self.my_direction = choice(self.direction_choice)
            self.cont = 0

    def collision_with_boundaries(self):
        if self.body[0][0] == 800:
            self.body[0] = (0, self.body[0][1])
        elif self.body[0][1] == 600:
            self.body[0] = (self.body[0][0], 0)
        elif self.body[0][0] < 0:
            self.body[0] = (800, self.body[0][1])
        elif self.body[0][1] < 0:
            self.body[0] = (self.body[0][0], 600)

    def initialize(self):
        self.move()
        self.user_move()
        self.collision_with_boundaries()
