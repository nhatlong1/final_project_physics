import pygame
import math
from include import button
from include import change_parameter

pygame.init()
pygame.font.init()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)

background_color = (white)
(width, height) = (860, 645)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Light Refraction Simulation')
angle = 0

pointofmiddle = (width / 2, height / 2)
myfont = pygame.font.SysFont('times new roman', 20)
parameter_font = pygame.font.SysFont('times new roman', 30)

Material1 = [1.0, "Air"]
Material2 = [1.52, "Glass"]
image = pygame.image.load(r'assets\flashlight.jpg').convert()
parameter_image = pygame.image.load(r'assets\parameter.PNG').convert()
change_parameter_button = button.Button(650, 210, parameter_image, 0.09)

class IncidentRay:
    def __init__(self, angle):
        self.x = width / 2
        self.y = 0
        self.raylen = 400
        self.angle_f = 0
        if 0 < angle:
            self.x = 0
            self.y = height / 2
        if -180 <= angle <= -90:
            self.x = pointofmiddle[0] + math.cos(math.radians(angle)) * self.raylen
            self.y = pointofmiddle[1] + math.sin(math.radians(angle)) * self.raylen
            self.angle_f = 180 - angle - 270 + 270
            textsurface = myfont.render('I : %f' % (180 - angle - 270), False, (0, 0, 0))
            screen.blit(textsurface, (20, 470))

    def display(self):
        pygame.draw.line(screen, red, pointofmiddle, (self.x, self.y), 3)
        image_1 = pygame.transform.scale(image, (150, 50))
        flashlight = pygame.transform.rotate(image_1, self.angle_f)
        screen.blit(flashlight,(self.x, self.y) )

class ReflectedRay:
    def __init__(self, angle):
        self.raylen = 400
        self.ReflectedRayAngle = 180 - angle
        self.reflectedintensity = (self.ReflectedRayAngle - 270) / 90
        self.x = width / 2
        self.y = 0

        if 270 <= self.ReflectedRayAngle <= 360:
            self.x = pointofmiddle[0] + math.cos(math.radians(self.ReflectedRayAngle)) * self.raylen
            self.y = pointofmiddle[1] + math.sin(math.radians(self.ReflectedRayAngle)) * self.raylen
        if 180 > self.ReflectedRayAngle >= 0:
            self.x = width
            self.y = height / 2

    def display(self):
        pygame.draw.line(screen, red, pointofmiddle, (self.x, self.y), 3)


class RefractedRay:
    def __init__(self, angle):
        self.x = width / 2
        self.y = 0
        self.raylen = 400
        TrueAngle = (180 - angle - 270)
        refractedangle = -math.degrees(math.asin(math.sin(math.radians(TrueAngle)) * Material1[0] / Material2[0])) + 90
        if 0 < angle:
            self.x = 0
            self.y = height / 2
        if -180 <= angle <= -90:
            self.x = pointofmiddle[0] + math.cos(math.radians(refractedangle)) * self.raylen
            self.y = pointofmiddle[1] + math.sin(math.radians(refractedangle)) * self.raylen
            textsurface = myfont.render('R : %f' % ((refractedangle - 90) * -1), False, (0, 0, 0))
            textsurface2 = myfont.render(" N1: " + str(Material1[0]), False, (0, 0, 0))
            textsurface3 = myfont.render(" N2: " + str(Material2[0]), False, (0, 0, 0))
            screen.blit(textsurface, (20, 500))
            screen.blit(textsurface2, (20, 150))
            screen.blit(textsurface3, (20, 400))

    def display(self):
        pygame.draw.line(screen, red, pointofmiddle, (self.x, self.y), 3)


class RefractionSurface:
    def __init__(self):
        surface = pygame.Surface((width, height/2), pygame.SRCALPHA)
        # surface.fill((100, 100, 255, 100))
        surface.fill((12, 56, 232, 100))

        screen.blit(surface, (0, height/2))




screen.fill(background_color)

IncidentRay(0).display()
ReflectedRay(0).display()
RefractionSurface()

pygame.display.flip()

running = True
while running:
    screen.fill(background_color)
    pygame.draw.lines(screen, black, False, [(width/2, 0), (width/2, height)])

    RefractionSurface()
    if change_parameter_button.draw(screen):
        change_parameter.inputBox()
        value = open('include/parameter_value.txt', "r")
        data = value.read()
        num1,num2 = data.split(' ')
        Material1[0] = float(num1)
        Material2[0] = float(num2)
    pos = pygame.mouse.get_pos()
    angle = math.atan2(pos[1] - (height / 2), pos[0] - (width / 2)) * 180 / math.pi
    (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
    if pressed1:
        IncidentRay(angle).display()
        ReflectedRay(angle).display()
        RefractedRay(angle).display()
        pygame.display.flip()
        (mouseX, mouseY) = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False