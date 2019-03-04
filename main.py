import math
import pygame
import sys
import time

pygame.init()

size = width, height = 1000, 600
black = 0, 0, 0
red = 255, 0, 0


def main():
    period = 0.018
    meter = 250.0
    gravity = 9.8

    screen = pygame.display.set_mode(size)

    b = Ball()
    ballrect = b.image.get_rect()
    ballrect.left = width / 2 - 50
    ballrect.top = height / 2 - 50

    x = ballrect.left
    y = ballrect.top

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if abs(b.speed[1]) < 0.05 and ballrect.bottom > height - 5:
            b.speed[1] = 0
            ballrect.bottom = height
            gravity = 0

        b.speed[1] += gravity * period

        absolute_speed = math.sqrt(b.speed[0] ** 2 + b.speed[1] ** 2)
        b.speed[0] -= 0.1 * period * b.speed[0] / absolute_speed
        b.speed[1] -= 0.1 * period * b.speed[1] / absolute_speed

        x += (b.speed[0] * period * meter)
        y += (b.speed[1] * period * meter)

        delta_x = int(x - ballrect.left)
        delta_y = int(y - ballrect.top)

        ballrect = ballrect.move(delta_x, delta_y)
        if ballrect.left < 0:
            ballrect.left = 0
            b.speed[0] = -b.speed[0]
        if ballrect.right > width:
            ballrect.right = width
            b.speed[0] = -b.speed[0]
        if ballrect.top < 0:
            ballrect.top = 0
            b.speed[1] = -b.speed[1]
        if ballrect.bottom > height:
            ballrect.bottom = height
            b.speed[1] = -b.speed[1]

        screen.fill(black)
        screen.blit(b.image, ballrect)
        pygame.display.flip()
        time.sleep(period)


class Ball:
    def __init__(self):
        self.image = pygame.Surface((100, 100))
        pygame.draw.circle(self.image, red, (50, 50), 50, 0)
        self.speed = [2.0, 0.0]


if __name__ == '__main__':
    main()
