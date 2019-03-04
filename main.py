import math
import pygame
import sys
import time

pygame.init()

# display constants
SIZE = WIDTH, HEIGHT = 1000, 600
BLACK = 0, 0, 0
RED = 255, 0, 0

# physics engine constants
PERIOD = 0.018
METER = 250.0
GRAVITY = 9.8

# TODO somehow starting at (100, 100) causes the ball to gain momentum?? pls fix.


def main():
    screen = pygame.display.set_mode(SIZE)

    b = Ball()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                b.held = True
                pygame.mouse.get_rel()
            if event.type == pygame.MOUSEBUTTONUP:
                b.held = False

        old_rect = b.rect

        if b.held:
            b.drag()
        else:
            b.move(old_rect)

        b.update_graphics(screen, old_rect)


class Ball:
    def __init__(self, center_location=(WIDTH / 2, HEIGHT / 2), r=50):
        self.image = pygame.Surface((2*r, 2*r))
        pygame.draw.circle(self.image, RED, (r, r), r, 0)
        self.shadow = pygame.Surface((2 * r, 2 * r))
        pygame.draw.circle(self.shadow, BLACK, (r, r), r, 0)
        self.speed = [2.0, 0.0]
        self.rect = self.image.get_rect(center=center_location)
        self.floored = False
        self.held = False

    def move(self, old_rect):
        # prevent ball from "jittering" when at bottom of screen
        if abs(self.speed[1]) < 0.05 and self.rect.bottom > HEIGHT - 5:
            self.speed[1] = 0
            self.rect.bottom = HEIGHT
            self.floored = True

        # apply gravity to ball
        if not self.floored:
            self.speed[1] += GRAVITY * PERIOD

        # apply air resistance to ball
        absolute_speed = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
        self.speed[0] -= 0.1 * PERIOD * self.speed[0] / absolute_speed
        self.speed[1] -= 0.1 * PERIOD * self.speed[1] / absolute_speed

        # update ball location
        self.rect.left += (self.speed[0] * PERIOD * METER)
        self.rect.top += (self.speed[1] * PERIOD * METER)
        delta_x = int(self.rect.left - old_rect.left)
        delta_y = int(self.rect.top - old_rect.top)
        self.rect = self.rect.move(delta_x, delta_y)

        # deal with collisions
        if self.rect.left < 0:
            self.rect.left = 0
            self.speed[0] = -self.speed[0]
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0:
            self.rect.top = 0
            self.speed[1] = -self.speed[1]
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.speed[1] = -self.speed[1]

    def drag(self):
        coords = pygame.mouse.get_pos()
        self.rect.left = coords[0]
        self.rect.top = coords[1]
        delta = pygame.mouse.get_rel()
        self.speed = [x / 10 for x in delta]
        self.rect = self.rect.move(delta)

    def update_graphics(self, screen, old_rect):
        # clear old ball image from screen
        screen.blit(self.shadow, old_rect)

        # draw current ball image on screen
        screen.blit(self.image, self.rect)

        pygame.display.update()
        time.sleep(PERIOD)


if __name__ == '__main__':
    main()
