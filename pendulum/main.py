import math
import time
from pathlib import Path
from threading import Thread

import matplotlib.pyplot as plt
import pygame

from includes.button import Button
from pendulum.includes.graph import coordinates_process
from includes.label import Label
from pendulum.includes.object import Pendulum

_WIDTH = 950
_HEIGHT = 600
_WHITE = "#FFFFFF"
_BLACK = "#000000"
_DARK_RED = "#960000"
_FPS = 60


class PendulumMain:
    def __init__(self) -> None:
        pygame.init()
        self.__screen = pygame.display.set_mode((_WIDTH, _HEIGHT))
        self.__clock = pygame.time.Clock()
        self.__click_region = pygame.Surface(
            (_WIDTH, _HEIGHT), pygame.SRCALPHA, 32).convert_alpha()
        self.__button_font = pygame.font.SysFont("times new roman", 40)
        self.__label_font = pygame.font.SysFont("times new roman", 20)
        self.__background = pygame.image.load(rf"{Path(__file__).parent}"
                                              r"\assets\background.png").convert_alpha()
        self.__exception_region = pygame.Rect(645, 100, 270, 175)

        self.__running = True
        self.__acceleration = False
        self.__times_loop = []
        self.__arr_x = []
        self.__count_loop = 0
        self.__angular_accel_change = 0
        self.__vel_change = 0

        self.__balance = int(_WIDTH / 2)
        self.__pendulum = Pendulum((self.__balance, -10), 2, self.__balance)

    def init_widgets(self):
        self.__btn_vel_increase = Button(self.__screen, font=self.__button_font,text="+",
                                         command=self.increase_vel, use_thread=False)
        self.__btn_vel_decrease = Button(self.__screen, font=self.__button_font, text="-",
                                         command=self.decrease_vel, use_thread=False)
        self.__btn_damp_increase = Button(self.__screen, font=self.__button_font, text="+",
                                          command=self.increase_damp, use_thread=False)
        self.__btn_damp_decrease = Button(self.__screen, font=self.__button_font, text="-",
                                          command=self.decrease_damp, use_thread=False)
        self.__btn_reset_value = Button(self.__screen, font=self.__button_font, text="Reset",
                                        command=self.reset_value, use_thread=False)
        self.__btn_draw_graph = Button(self.__screen, font=self.__button_font,
                                       text="Graph", command=self.draw_graph, use_thread=False)
        self.__label_velocity = Label(
            self.__screen, font=self.__label_font, text="VELOCITY")
        self.__label_damping = Label(
            self.__screen, font=self.__label_font, text="DAMPING")

    def draw_widget(self):
        self.__label_velocity.place(705, 100, 150, 55)
        self.__label_damping.place(705, 160, 150, 55)
        self.__btn_vel_increase.place(645, 100, 55, 55)
        self.__btn_vel_decrease.place(860, 100, 55, 55)
        self.__btn_damp_increase.place(645, 160, 55, 55)
        self.__btn_damp_decrease.place(860, 160, 55, 55)
        self.__btn_draw_graph.place(645, 220, 130, 55)
        self.__btn_reset_value.place(785, 220, 130, 55)
        self.__pendulum.draw(
            self.__screen, self.__click_region, _BLACK, _BLACK, _DARK_RED)

    def increase_vel(self):
        if self.__angular_accel_change + 0.0005 <= 1:
            self.__angular_accel_change += 0.0005

    def decrease_vel(self):
        if self.__angular_accel_change - 0.0005 >= 0:
            self.__angular_accel_change -= 0.0005

    def increase_damp(self):
        if self.__vel_change - 0.0005 >= -0.01:
            self.__vel_change -= 0.0005

    def decrease_damp(self):
        if self.__vel_change + 0.0005 <= 0:
            self.__vel_change += 0.0005

    def reset_value(self):
        self.__vel_change = self.__angular_accel_change = 0

    def draw_graph(self):
        plt.clf()
        position_x, position_y = coordinates_process(
            " ".join(self.__arr_x), " ".join(self.__times_loop))
        plt.plot(position_y, position_x)
        plt.title('Pendulum Graph')
        plt.xlabel('Position update instance')
        plt.ylabel('Position with respect to balance')
        plt.show()

    def animation(self, fps):
        while self.__running:
            if self.__acceleration:
                self.__times_loop.append(str(self.__count_loop))
                self.__pendulum.old_x = self.__pendulum.x
                self.__pendulum.old_y = self.__pendulum.y
                self.__arr_x.append(
                    str(self.__pendulum.x - self.__pendulum.balance))
                self.__pendulum.angacc = - \
                    (0.0005 + self.__angular_accel_change) * \
                    math.sin(self.__pendulum.angle)
                self.__pendulum.vel += self.__pendulum.angacc
                self.__pendulum.vel *= (1 + self.__vel_change)
                self.__pendulum.angle += self.__pendulum.vel
                self.__pendulum.update_position()
                self.__count_loop += 1
            if self.__count_loop % 180 == 0:
                self.reset_region()
            time.sleep(1/fps)


    def reset_region(self):
        try:
            self.__click_region = self.__click_region = pygame.Surface(
                                (_WIDTH, _HEIGHT), pygame.SRCALPHA, 32).convert_alpha()
        except pygame.error:
            pass

    def mainloop(self):
        Thread(target=self.animation, args=(_FPS,)).start()
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.__exception_region.collidepoint(mouse_pos):
                        self.__arr_x = []
                        self.__times_loop = []
                        self.__count_loop = 0
                        self.reset_region()
                        self.__pendulum = Pendulum(
                            pygame.mouse.get_pos(), 15, self.__balance)
                        self.__pendulum.angle_length()
                        self.__acceleration = True

            self.__screen.fill(_WHITE)
            self.__screen.blit(pygame.transform.scale(
                self.__background, (955, 555)), (0, 0))
            self.draw_widget()
            pygame.display.flip()
            self.__clock.tick(_FPS)