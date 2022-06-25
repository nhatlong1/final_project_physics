import math
from pathlib import Path

import pygame

from includes.label import Label
from includes.button import Button
from includes.entry import Entry
from light.includes.constants import *
from light.includes.objects import IncidentRay, ReflectedRay, RefractionSurface, \
    RefractedRay


class LightRefraction:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Light Refraction Simulation')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.running = True
        self.ray_angle = 0
        self.entries = []

        self.btn_font = pygame.font.Font(rf"{Path(__file__).parent}\assets\fonts\times.ttf", 20)
        self.entry_font = pygame.font.Font(rf"{Path(__file__).parent}\assets\fonts\times.ttf", 14)
        self.label_font = pygame.font.Font(rf"{Path(__file__).parent}\assets\fonts\times.ttf", 22)
        self.flashlight = pygame.image.load(
            rf"{Path(__file__).parent}\assets\images\flashlight.jpg"
        ).convert()
        self.flashlight = pygame.transform.scale(self.flashlight, (150, 50)).convert()
        self.ignore_zone = pygame.Rect((900, 75, 280, 180))

        self.incident_ray = IncidentRay(self.screen, 0, self.label_font)
        self.reflected_ray = ReflectedRay(self.screen, 0)
        self.refracted_ray = RefractedRay(self.screen, self.label_font, 0)
        self.refraction_surface = RefractionSurface(self.screen)

    def init_widgets(self):
        self.label_param_n1 = Label(self.screen, self.label_font, "N1", "#D0D0D0", "#000000",
                                    justify="center")
        self.label_param_n2 = Label(self.screen, self.label_font, "N2", "#D0D0D0", "#000000",
                                    justify="center")
        self.entry_param_n1 = Entry(self.screen, self.entry_font, regex_filter=REGEX_NUMBERS,
                                    border_width=3, clear_on_focus=True)
        self.entry_param_n2 = Entry(self.screen, self.entry_font, regex_filter=REGEX_NUMBERS,
                                    border_width=3, clear_on_focus=True)
        self.btn_change_param = Button(self.screen, self.btn_font, "Change Parameter",
                                       command=self.change_param,
                                       use_thread=False)
        self.entries = [self.entry_param_n1, self.entry_param_n2]

    def draw_widgets(self):
        self.label_param_n1.place(900, 75, 75, 50)
        self.label_param_n2.place(900, 130, 75, 50)
        self.entry_param_n1.place(980, 75, 200, 50)
        self.entry_param_n2.place(980, 130, 200, 50)
        self.btn_change_param.place(940, 210, 200, 50)

    def draw_objects(self):
        pygame.draw.lines(self.screen, BLACK, False,
                          [(WIDTH/2, 0), (WIDTH / 2, HEIGHT)])
        self.incident_ray.display()
        self.reflected_ray.display()
        self.refracted_ray.display()
        self.refraction_surface.display()

    def change_param(self):
        self.refracted_ray.config_material((self.entry_param_n1.get(False, float), "air"),
                                           (self.entry_param_n2.get(False, float), "mat"))

    def mainloop(self):
        self.draw_objects()
        while self.running:
            if pygame.event.peek(pygame.QUIT):
                self.running = False
                pygame.quit()
                return 0
            for event in pygame.event.get():
                for entry in self.entries:
                    entry.handle_entry_events(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.ignore_zone.collidepoint(mouse_pos):
                        # mouse_press = pygame.mouse.get_pressed()
                        angle = math.atan2(
                            mouse_pos[1] - (HEIGHT / 2),
                            mouse_pos[0] - (WIDTH / 2)
                        ) * 180 / math.pi
                        self.flashlight = pygame.transform.scale(self.flashlight, (150, 50))
                        self.flashlight = pygame.transform.rotate(self.flashlight, self.incident_ray.angle_f)
                        self.incident_ray.config(angle)
                        self.reflected_ray.config(angle)
                        self.refracted_ray.config(angle)
                        self.flashlight.blit(self.screen, (self.incident_ray.x, self.incident_ray.y))

            self.screen.fill("#FFFFFF")
            self.draw_objects()
            self.draw_widgets()
            pygame.display.flip()
            self.clock.tick(FPS)





# running = True
# while running:
#     if change_parameter_button.draw(screen):
#         change_parameter.inputBox()
#         value = open('include/parameter_value.txt', "r")
#         data = value.read()
#         num1,num2 = data.split(' ')
#         Material1[0] = float(num1)
#         Material2[0] = float(num2)