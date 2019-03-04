import math
import pygame
import sys
import time

pygame.init()

SIZE = WIDTH, HEIGHT = 1000, 600
BLACK = 0, 0, 0
RED = 255, 0, 0

PERIOD = 0.018
METER = 250.0
GRAVITY = 9.8

# TODO somehow starting at (100, 100) causes the ball to gain momentum?? pls fix.


def main():
    screen = pygame.display.set_mode(SIZE)

    # initialize ball
    b = Ball()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # clear old ball image from screen
        old_rect = b.rect
        screen.blit(b.old_pos, old_rect)

        # prevent ball from "jittering" when at bottom of screen
        if abs(b.speed[1]) < 0.05 and b.rect.bottom > HEIGHT - 5:
            b.speed[1] = 0
            b.rect.bottom = HEIGHT
            b.floored = True

        # apply gravity to ball
        if not b.floored:
            b.speed[1] += GRAVITY * PERIOD

        # apply air resistance to ball
        absolute_speed = math.sqrt(b.speed[0] ** 2 + b.speed[1] ** 2)
        b.speed[0] -= 0.1 * PERIOD * b.speed[0] / absolute_speed
        b.speed[1] -= 0.1 * PERIOD * b.speed[1] / absolute_speed

        # update ball location
        b.rect.left += (b.speed[0] * PERIOD * METER)
        b.rect.top += (b.speed[1] * PERIOD * METER)
        delta_x = int(b.rect.left - old_rect.left)
        delta_y = int(b.rect.top - old_rect.top)
        b.rect = b.rect.move(delta_x, delta_y)

        # deal with collisions
        if b.rect.left < 0:
            b.rect.left = 0
            b.speed[0] = -b.speed[0]
        if b.rect.right > WIDTH:
            b.rect.right = WIDTH
            b.speed[0] = -b.speed[0]
        if b.rect.top < 0:
            b.rect.top = 0
            b.speed[1] = -b.speed[1]
        if b.rect.bottom > HEIGHT:
            b.rect.bottom = HEIGHT
            b.speed[1] = -b.speed[1]

        # update graphics
        screen.blit(b.image, b.rect)
        pygame.display.update()
        time.sleep(PERIOD)


class Ball:
    def __init__(self, center_location=(WIDTH / 2, HEIGHT / 2), r=50):
        self.image = pygame.Surface((2*r, 2*r))
        pygame.draw.circle(self.image, RED, (r, r), r, 0)
        self.old_pos = pygame.Surface((2*r, 2*r))
        pygame.draw.circle(self.old_pos, BLACK, (r, r), r, 0)
        self.speed = [2.0, 0.0]
        self.rect = self.image.get_rect(center=center_location)
        self.floored = False


if __name__ == '__main__':
    main()
