import pygame
import math


width, height = 1000, 600

Out = False
acceleration = False
length = 0
angle = 0
vel = 0
Aacc = 0



white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
Dark_red = (150, 0, 0)


pygame.init()
background = pygame.display.set_mode((width, height))
bg = pygame.image.load(r'assets\background.jpg').convert()
clock = pygame.time.Clock()


class ball(object):

    def __init__(self, XY, radius):
        self.x = XY[0]
        self.y = XY[1]
        self.radius = radius

    def draw(self, bg):  #
        pygame.draw.lines(bg, black, False, [(width / 2, 50), (self.x, self.y)], 2)
        pygame.draw.circle(bg, black, (self.x, self.y), self.radius)
        pygame.draw.circle(bg, Dark_red, (self.x, self.y), self.radius - 2)


def grid():
    for x in range(50, width, 50):
        pygame.draw.lines(background, gray, False, [(x, 0), (x, height)])
        for y in range(50, height, 50):
            pygame.draw.lines(background, gray, False, [(0, y), (width, y)])
    pygame.draw.circle(background, black, (int(width / 2), 50), 5)


def angle_Length():
    length = math.sqrt(math.pow(pendulum.x - width / 2, 2) + math.pow(pendulum.y - 50, 2))
    angle = math.asin((pendulum.x - width / 2) / length)
    return (angle, length)


def get_path(first_angle, length):
    pendulum.x = round(width / 2 + length * math.sin(angle))
    pendulum.y = round(50 + length * math.cos(angle))


def redraw():
    background.fill(white)
    background.blit(bg,(1000,500))
    background.blit(pygame.transform.scale(bg, (1000, 600)), (0, 0))
    grid()
    pendulum.draw(background)
    pygame.display.update()


pendulum = ball((int(width / 2), -10), 2)

while not Out:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Out = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pendulum = ball(pygame.mouse.get_pos(), 15)
            angle, length = angle_Length()
            acceleration = True


    if acceleration:
        Aacc = -0.0049 * math.sin(angle)
        vel += Aacc
        vel *= 0.99
        angle += vel
        get_path(angle, length)

    redraw()

pygame.quit()