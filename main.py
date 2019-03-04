import math
import pygame
import sys
import time

pygame.init()

# display constants
SIZE = (WIDTH, HEIGHT) = (1000, 600)
BLACK = 0, 0, 0
RED = 255, 0, 0

# physics engine constants
METER = 250.0
GRAVITY = 9.8


def main():
    screen = pygame.display.set_mode(SIZE)
    global screen

    b = Ball()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                b.held = True
                pygame.mouse.get_rel()
            if event.type == pygame.MOUSEBUTTONUP:
                b.held = False

        old_rect = b.rect.copy()

        interval = clock.tick(60) / 1000.0

        if b.held:
            b.drag(interval)
        else:
            b.move(old_rect, interval)

        b.update_graphics(old_rect)


class Ball:
    def __init__(self, center_location=(WIDTH / 2, HEIGHT / 2), r=50):
        self.image = pygame.Surface((2*r, 2*r))
        pygame.draw.circle(self.image, RED, (r, r), r, 0)
        self.shadow = pygame.Surface((2 * r, 2 * r))
        pygame.draw.circle(self.shadow, BLACK, (r, r), r, 0)
        self.speed = [2.0, 0.0]
        self.rect = self.image.get_rect(center=center_location)
        self.r = r
        self.floored = False
        self.held = False

    def move(self, old_rect, TIME):
        # prevent ball from "jittering" when at bottom of screen
        if abs(self.speed[1]) < 0.05 and self.rect.bottom > HEIGHT - 5:
            self.speed[1] = 0
            self.rect.bottom = float(HEIGHT)
            self.floored = True

        # apply gravity to ball
        if not self.floored:
            self.speed[1] += GRAVITY * TIME

        # apply air resistance to ball
        absolute_speed = math.sqrt(self.speed[0] ** 2 + self.speed[1] ** 2)
        self.speed[0] -= 0.1 * TIME * self.speed[0] / absolute_speed
        self.speed[1] -= 0.1 * TIME * self.speed[1] / absolute_speed

        # update ball location
        self.rect.move_ip([x * TIME * METER for x in self.speed])

        # deal with collisions
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.speed[1] = -self.speed[1]
        self.rect.clamp(screen.get_rect())

    def drag(self, TIME):
        coords = [x - self.r for x in pygame.mouse.get_pos()]
        self.rect.left = coords[0]
        self.rect.top = coords[1]
        delta = pygame.mouse.get_rel()
        self.speed = [x / METER / TIME for x in delta]
        self.rect.move_ip(delta)

    def update_graphics(self, old_rect):
        # clear old ball image from screen
        screen.blit(self.shadow, old_rect)

        # draw current ball image on screen
        screen.blit(self.image, self.rect)

        pygame.display.update()


if __name__ == '__main__':
    main()
