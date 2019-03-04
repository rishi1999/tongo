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


def main():
    screen = pygame.display.set_mode(SIZE)

    # initialize ball
    b = Ball()
    ballrect = b.image.get_rect()
    ballrect.left = b.x
    ballrect.top = b.y

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # clear old ball image from screen
        screen.blit(b.old_pos, ballrect)

        if abs(b.speed[1]) < 0.05 and ballrect.bottom > HEIGHT - 5:
            b.speed[1] = 0
            ballrect.bottom = HEIGHT
            b.floored = True

        # apply gravity to ball
        if not b.floored:
            b.speed[1] += GRAVITY * PERIOD

        # apply air resistance to ball
        absolute_speed = math.sqrt(b.speed[0] ** 2 + b.speed[1] ** 2)
        b.speed[0] -= 0.1 * PERIOD * b.speed[0] / absolute_speed
        b.speed[1] -= 0.1 * PERIOD * b.speed[1] / absolute_speed

        # update ball location
        b.x += (b.speed[0] * PERIOD * METER)
        b.y += (b.speed[1] * PERIOD * METER)
        delta_x = int(b.x - ballrect.left)
        delta_y = int(b.y - ballrect.top)
        ballrect = ballrect.move(delta_x, delta_y)

        # deal with collisions
        if ballrect.left < 0:
            ballrect.left = 0
            b.speed[0] = -b.speed[0]
        if ballrect.right > WIDTH:
            ballrect.right = WIDTH
            b.speed[0] = -b.speed[0]
        if ballrect.top < 0:
            ballrect.top = 0
            b.speed[1] = -b.speed[1]
        if ballrect.bottom > HEIGHT:
            ballrect.bottom = HEIGHT
            b.speed[1] = -b.speed[1]

        # update graphics
        screen.blit(b.image, ballrect)
        pygame.display.update()
        time.sleep(PERIOD)


class Ball:
    def __init__(self):
        r = 50
        self.image = pygame.Surface((2*r, 2*r))
        pygame.draw.circle(self.image, RED, (r, r), r, 0)
        self.old_pos = pygame.Surface((2*r, 2*r))
        pygame.draw.circle(self.old_pos, BLACK, (r, r), r, 0)
        self.speed = [2.0, 0.0]
        self.x = WIDTH / 2 - r
        self.y = HEIGHT / 2 - r
        self.floored = False


if __name__ == '__main__':
    main()
