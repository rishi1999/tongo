import math
import sys
import getopt
import pygame

# display constants
SIZE = WIDTH, HEIGHT = 1000, 600
BG_COLOR = 0, 0, 0
BALL_COLOR = 255, 0, 0

# physics engine constants
METER = 250.0
GRAVITY = 9.8
FRICTION = 0.1
RESTITUTION = 0.9

DEFAULT_RADIUS = 50

# TODO add docstrings to functions
# TODO test cli inputs heavily
# TODO update readme on github to talk about cli arguments when they are production ready


def hex_to_rgb(color):
    hlen = len(color)
    return tuple(clamp(int(color[i:i + hlen / 3], 16), max=255) for i in range(0, hlen, hlen / 3))


def clamp(val, min=0, max=sys.maxsize):
    if min > max:
        print("errrorrrrr")  # TODO figure out how to properly throw exceptions

    if val < min:
        val = min
    elif val > max:
        val = max

    return val


def main(argv):
    global SIZE, WIDTH, HEIGHT, BG_COLOR, BALL_COLOR, METER, GRAVITY, FRICTION, RESTITUTION
    usage_text = """usage: python main.py [options]
        options:
            -h, --help          Displays this usage guide.
            --width=SIZE        Sets width of the screen to SIZE.
            --height=SIZE       Sets height of the screen to SIZE.
            --bgcolor=COLOR     Sets the background color of the screen to COLOR.
            --ballcolor=COLOR   Sets the color of the ball to COLOR.
            --meter=NUM         Sets the length of a meter in the simulation to NUM pixels.
            --gravity=NUM       Sets the acceleration due to gravity in the simulation to NUM meters squared per second.
            --friction=NUM      Sets the coefficient of friction in the simulation to NUM.
            --restitution=NUM   Sets the coefficient of restitution in the simulation to NUM."""
    try:
        opts, args = getopt.getopt(argv, "", ["help=", "width=", "height=", "bgcolor=", "ballcolor=", "meter=",
                                              "gravity=", "friction=", "restitution="])
    except getopt.GetoptError:
        print usage_text
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--help':
            print usage_text
            sys.exit()
        elif opt == '--width':
            WIDTH = clamp(int(arg), 3 * DEFAULT_RADIUS, 4000)
            SIZE = WIDTH, HEIGHT
        elif opt == '--height':
            HEIGHT = clamp(int(arg), 3 * DEFAULT_RADIUS, 4000)
            SIZE = WIDTH, HEIGHT
        elif opt == '--bgcolor':
            if len(arg) != 6:
                print usage_text
                sys.exit(2)
            BG_COLOR = hex_to_rgb(arg)
        elif opt == '--ballcolor':
            if len(arg) != 6:
                print usage_text
                sys.exit(2)
            BALL_COLOR = hex_to_rgb(arg)
        elif opt == '--meter':
            METER = clamp(float(arg), 50, 500)
        elif opt == '--gravity':
            GRAVITY = clamp(float(arg), max=50)
        elif opt == '--friction':
            FRICTION = clamp(float(arg), max=2)
        elif opt == '--restitution':
            RESTITUTION = clamp(float(arg), max=1.5)

    pygame.init()

    global screen
    screen = pygame.display.set_mode(SIZE)
    # TODO fix bg color

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

        b.old_rect = b.rect.copy()

        interval = clock.tick(60) / 1000.0

        if b.held:
            b.drag(interval, speed_limit=10.0)
        else:
            b.move(interval)

        b.update_graphics()


def calculate_speed(velocity):
    return math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)


class Ball:
    def __init__(self, center_location=(WIDTH / 2, HEIGHT / 2), r=DEFAULT_RADIUS, vel=(0.0, 0.0)):
        self.image = pygame.Surface((2 * r, 2 * r))
        pygame.draw.circle(self.image, BALL_COLOR, (r, r), r, 0)
        self.shadow = pygame.Surface((2 * r, 2 * r))
        pygame.draw.circle(self.shadow, BG_COLOR, (r, r), r, 0)
        self.vel = list(vel)
        self.rect = self.image.get_rect(center=center_location)
        self.old_rect = None
        self.r = r
        self.held = False

    def move(self, TIME):
        # prevent ball from "jittering" when at bottom of screen
        if abs(self.vel[1]) < 0.05 and self.rect.bottom == HEIGHT:
            self.vel[1] = 0

            delta = FRICTION * GRAVITY * TIME
            if self.vel[0] > 0:
                self.vel[0] -= delta
            else:
                self.vel[0] += delta
        else:
            # apply gravity to ball
            self.vel[1] += GRAVITY * TIME

            # apply air resistance to ball
            speed = calculate_speed(self.vel)
            self.vel[0] -= 0.1 * TIME * self.vel[0] / speed
            self.vel[1] -= 0.1 * TIME * self.vel[1] / speed

            # TODO add friction

        # update ball location and velocity
        self.rect.move_ip([x * TIME * METER for x in self.vel])
        self.rect.clamp_ip(screen.get_rect())
        if self.rect.left == 0:
            self.vel[0] = abs(self.vel[0])
            self.vel[0] *= RESTITUTION
        if self.rect.right == WIDTH:
            self.vel[0] = -abs(self.vel[0])
            self.vel[0] *= RESTITUTION
        if self.rect.top == 0:
            self.vel[1] = abs(self.vel[1])
            self.vel[1] *= RESTITUTION
        if self.rect.bottom == HEIGHT:
            self.vel[1] = -abs(self.vel[1])
            self.vel[1] *= RESTITUTION

    def drag(self, TIME, speed_limit):
        coords = [x - self.r for x in pygame.mouse.get_pos()]
        self.rect.left = coords[0]
        self.rect.top = coords[1]
        delta = pygame.mouse.get_rel()
        self.vel = [x / METER / TIME for x in delta]

        speed = calculate_speed(self.vel)
        scale = 1
        if speed > speed_limit:
            scale = speed_limit / speed
        self.vel = [x * scale for x in self.vel]

        self.rect.move_ip(delta)

    def update_graphics(self):
        # clear old ball image from screen
        screen.blit(self.shadow, self.old_rect)

        # draw current ball image on screen
        screen.blit(self.image, self.rect)

        pygame.display.update()


if __name__ == '__main__':
    main(sys.argv[1:])
