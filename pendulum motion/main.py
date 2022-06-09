import pygame
import math
import button
from graph import graph

width, height = 950, 600

Out = False
acceleration = False
length = 0
angle = 0
vel = 0
Aacc = 0
Aacc_change = 0
vel_change = 0
arr_X = []
count_loop = 0
times_loop = []
arr_old_x = []
arr_old_y = []
old_x = 0
old_y = 0


white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
Dark_red = (150, 0, 0)


pygame.init()
background = pygame.display.set_mode((width, height))
background2 = pygame.Surface([width, height], pygame.SRCALPHA, 32)
background2 = background2.convert_alpha()

bg = pygame.image.load(r'assets\background.png').convert()
velocity = pygame.image.load(r'assets\velocity.png').convert()
damping = pygame.image.load(r'assets\damping.png').convert()
graph_img = pygame.image.load(r'assets\graph.png').convert()


plus1 = pygame.image.load(r'assets\plus.png').convert()
plus2 = pygame.image.load(r'assets\plus.png').convert()
minus1 = pygame.image.load(r'assets\minus.jpg').convert()
minus2 = pygame.image.load(r'assets\minus.jpg').convert()



plus_velocity = button.Button(723, 120, plus1, 0.08)
minus_velocity = button.Button(860, 119, minus1, 0.05)
plus_damping = button.Button(718, 168, plus2, 0.08)
minus_damping = button.Button(858, 168, minus2, 0.05)
graph_button = button.Button(780, 230, graph_img, 1)
velocity_button = button.Button(750, 100, velocity, 0.05)
damping_button = button.Button(750, 150, damping, 0.05)


clock = pygame.time.Clock()


class ball(object):

    def __init__(self, XY, radius):
        self.x = XY[0]
        self.y = XY[1]
        self.radius = radius

    def draw(self, bg):
        pygame.draw.lines(bg, black, False, [(width / 2, 50), (self.x, self.y)], 2)
        pygame.draw.circle(bg, black, (self.x, self.y), self.radius)
        pygame.draw.line(background2, Dark_red, (old_x, old_y), (pendulum.x, pendulum.y), 2)
        background.blit(background2, (0, 0))
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
    background.blit(pygame.transform.scale(bg, (955, 555)), (0, 0))
    background.blit(pygame.transform.scale(velocity, (100, 55)), (750, 100))
    background.blit(pygame.transform.scale(damping, (100, 55)), (750, 150 ))
    background.blit(pygame.transform.scale(plus1, (20, 20)), (720, 116))
    background.blit(pygame.transform.scale(minus1, (23, 15)), (860, 119))
    background.blit(pygame.transform.scale(plus2, (20, 20)), (720, 170))
    background.blit(pygame.transform.scale(minus2, (23, 15)), (860, 170))
    background.blit(pygame.transform.scale(graph_img, (100, 55)), (780, 230))
    # grid()
    pendulum.draw(background)
    pygame.display.update()

graph_check = False

pendulum = ball((int(width / 2), -10), 2)
while not Out:
    count_loop += 1
    times_loop.append(str(count_loop))
    clock.tick(120)
    check_click = 0


    for event in pygame.event.get():

        if plus_velocity.draw(background):
            Aacc_change += 0.0005
            print(Aacc_change)
            check_click += 1

        elif minus_velocity.draw(background):
            if Aacc_change < -0.00002:
                pass
            else:
                Aacc_change -= 0.0003
            print(Aacc_change)
            check_click += 1

        elif plus_damping.draw(background):
            vel_change -= 0.0005
            print(vel_change)
            check_click += 1

        elif minus_damping.draw(background):
            vel_change += 0.0005
            print(vel_change)
            check_click += 1
        elif graph_button.draw(background):
            if graph_check == False:
                graph_check = True
            else:
                graph_check = False

            print("done!!!")
            check_click += 1

        if event.type == pygame.QUIT:
            Out = True
        elif check_click == 0:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                pendulum = ball(pygame.mouse.get_pos(), 15)
                angle, length = angle_Length()
                acceleration = True
    if acceleration:
        Aacc = -(0.0005 + Aacc_change) * math.sin(angle)
        vel += Aacc
        vel *= 1 + vel_change
        angle += vel
        get_path(angle, length)
        arr_X.append(str(int(pendulum.x - width / 2)))
        arr_old_x.append((int(pendulum.x)))
        arr_old_y.append((int(pendulum.y)))
        old_x = arr_old_x[len(arr_old_x)-1]
        old_y = arr_old_y[len(arr_old_y)-1]

    if graph_check == True:
        graph.coordinates_process()
    coordiates = 'graph/coordinates.txt'
    with open(coordiates, 'w') as c:
        c.write(' '.join(arr_X))
    c.close()
    times = 'graph/times.txt'
    with open(times, 'w') as t:
        t.write(' '.join(times_loop))
    t.close()
    redraw()

pygame.quit()
