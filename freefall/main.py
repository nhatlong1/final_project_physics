"""Main

Main file for free fall. Import this file in parent main.py
"""
from threading import Thread
import time
from pathlib import Path
from math import inf, sqrt
import pygame
from includes.constants import GAME_HEIGHT, GAME_WIDTH, FPS, BLACK, WHITE, \
    LIGHT_GRAY2, ENTRY_ACTIVE, ENTRY_INACTIVE, NORMAL_STATE, DISABLED_STATE
from includes.button import Button
from includes.entry import Entry
from includes.label import Label
from includes.camera import CameraGroup
from includes.sprites import FallObject, BackgroundSprite


class FreeFallSim:
    """Main class.
    """
    def __init__(self) -> None:
        """Init
        """
        pygame.init()

        self.__entries = []
        self.__buttons = []
        self.__labels = []

        self.so = lambda msg: Thread(target=self.show_output,
                            args=(msg, self.__calculate_button)).start()

        self.__screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.__clock = pygame.time.Clock()
        self.__running = False
        try:
            self.__font = pygame.font.Font(rf"{Path(__file__).parent}\assets\fonts\times.ttf", 16)
        except FileNotFoundError:
            self.__font = pygame.font.Font(pygame.font.get_default_font(), 16)
        self.__camera = CameraGroup(limit_x_negative=0, limit_x_positive=0)
        self.__fall_object = FallObject((-100, 0), self.__camera, allow_keyboard_control=False,
                                        fill_color="#000000", rect_size=(25, 25))
        self.__background = BackgroundSprite(self.__camera,
                                             rf"{Path(__file__).parent}\assets\images\meter.png")


    def init_widgets(self):
        self.__ga_entry = Entry(self.__screen, font=self.__font, text="9.8")
        self.__height_entry = Entry(self.__screen, font=self.__font, text="500")
        self.__time_entry = Entry(self.__screen, font=self.__font, text="0")
        self.__velocity_entry = Entry(self.__screen, font=self.__font, text="0")
        self.__ga_label = Label(self.__screen, font=self.__font,
                                text="Grav. Accel (m/s^2)")
        self.__height_label = Label(self.__screen, font=self.__font,
                                text="Height (m)")
        self.__time_label = Label(self.__screen, font=self.__font,
                                text="Fall Time (s)")
        self.__velocity_label = Label(self.__screen, font=self.__font,
                                text="Velocity (m/s)")
        self.__set_button = Button(self.__screen, font=self.__font, text="Set",
                                  command=self.set_object)
        self.__calculate_button = Button(self.__screen, font=self.__font, text="Calculate",
                                       command=self.calculate)
        self.__reset_button = Button(self.__screen, font=self.__font, text="Reset",
                                     command=self.reset)
        self.__fall_button = Button(self.__screen, font=self.__font, text="Drop",
                                  command=lambda: Thread(target=self.begin_fall).start())
        self.__entries = [self.__ga_entry, self.__height_entry, self.__time_entry,
                          self.__velocity_entry]
        self.__buttons = [self.__set_button, self.__calculate_button, self.__reset_button]
        self.__labels = [self.__height_label, self.__ga_label, self.__time_label,
                         self.__velocity_label]
        self.calculate()
        self.set_object()


    def draw_widget(self):
        self.__ga_entry.place(GAME_WIDTH-100, y=GAME_HEIGHT-600, width=100, height=50)
        self.__height_entry.place(GAME_WIDTH-100, y=GAME_HEIGHT-540, width=100, height=50)
        self.__time_entry.place(GAME_WIDTH-100, y=GAME_HEIGHT-480, width=100, height=50)
        self.__velocity_entry.place(GAME_WIDTH-100, y=GAME_HEIGHT-420, width=100, height=50)
        self.__set_button.place(GAME_WIDTH-100, GAME_HEIGHT-360, width=100, height=50)
        self.__calculate_button.place(GAME_WIDTH-100, GAME_HEIGHT-300, width=100, height=50)
        self.__reset_button.place(GAME_WIDTH-100, GAME_HEIGHT-240, width=100, height=50)
        self.__fall_button.place(GAME_WIDTH-100, GAME_HEIGHT-180, width=100, height=50)
        self.__ga_label.place(GAME_WIDTH-300, GAME_HEIGHT-600, 190, 50)
        self.__height_label.place(GAME_WIDTH-300, GAME_HEIGHT-540, 190, 50)
        self.__time_label.place(GAME_WIDTH-300, GAME_HEIGHT-480, 190, 50)
        self.__velocity_label.place(GAME_WIDTH-300, GAME_HEIGHT-420, 190, 50)

        try:
            self.__output_label.place(0, 0, GAME_WIDTH, 50)
        except:
            pass


    def widgets_visibility(self, labels: bool = True, buttons: bool = True, entries: bool = True):
        if labels is False:
            for label in self.__labels:
                label.config(bg="#FFFFFF", fg="#FFFFFF")
        else:
            for label in self.__labels:
                label.config(bg=LIGHT_GRAY2, fg=BLACK)
        if buttons is False:
            for button in self.__buttons:
                button.config(disabled_color="#FFFFFF", text_color="#FFFFFF",
                              normal_color="#FFFFFF")
                button.config(state="disabled")
        else:
            for button in self.__buttons:
                button.config(disabled_color=DISABLED_STATE, text_color=WHITE,
                              normal_color=NORMAL_STATE)
                button.config(state="normal")
        if entries is False:
            for entry in self.__entries:
                entry.config(active_color="#FFFFFF", border_color="#FFFFFF", state="disabled", fg="#FFFFFF")
        else:
            for entry in self.__entries:
                entry.config(active_color=ENTRY_ACTIVE, border_color=ENTRY_INACTIVE,
                             state="normal", fg="#000000")


    def set_object(self):
        height = GAME_HEIGHT - float(self.__height_entry.get(False))
        self.__fall_object.speed = 0
        self.__fall_object.position.y = height
        self.__fall_object.rect.y = round(self.__fall_object.position.y)
        self.__fall_object.position.x = int(GAME_WIDTH / 2 - 25 / 2)
        self.__fall_object.rect.x = round(self.__fall_object.position.x)

    def calculate(self):
        ga = self.__ga_entry.get(False)
        height = self.__height_entry.get(False)
        velocity = self.__velocity_entry.get(False)
        fall_time = self.__time_entry.get(False)
        status = [bool(ga), bool(height), bool(velocity), bool(fall_time)]
        try:
            ga = float(ga) if status[0] else None
            height = float(height) if status[1] else None
            velocity = float(velocity) if status[2] else None
            fall_time = float(fall_time) if status[3] else None
        except ValueError as ve:
            self.so(f"All value must be float {ve}")
            return
        status = [bool(ga), bool(height), bool(velocity), bool(fall_time)]
        count = status.count(True)
        if count < 2:
            self.so("Not enough values (min 2)")
            return
        if status[0] and status[3]:
            velocity = ga * fall_time
            if velocity == 0:
                velocity = inf
            height = 0.5 * ga * fall_time * fall_time
            self.__velocity_entry.set(f"{velocity:.2f}")
            self.__height_entry.set(f"{height:.2f}")
            return
        if status[0] and status[1]:
            fall_time = sqrt((2 * height) / ga)
            velocity = ga * fall_time
            if velocity == 0:
                velocity = inf
            self.__velocity_entry.set(f"{velocity:.2f}")
            self.__time_entry.set(f"{fall_time:.2f}")
            return
        if status[0] and status[2]:
            fall_time = velocity / ga
            height = 0.5 * ga * fall_time * fall_time
            self.__time_entry.set(f"{fall_time:.2f}")
            self.__height_entry.set(f"{height:.2f}")
            return
        if status[1] and status[3]:
            ga = (2 * height) / (fall_time * fall_time)
            velocity = ga * fall_time
            if velocity == 0:
                velocity = inf
            self.__ga_entry.set(f"{ga:.2f}")
            self.__velocity_entry.set(f"{velocity:.2f}")
            return
        if status[1] and status[2]:
            self.so("Can not calculate")
            return
        if status[2] and status[3]:
            ga = velocity / fall_time
            height = 0.5 * ga * fall_time * fall_time
            self.__ga_entry.set(f"{ga:.2f}")
            self.__height_entry.set(f"{height:.2f}")
            return


    def reset(self):
        for entry in self.__entries:
            entry.set("0")
        self.__fall_object.position.x = -100
        self.__fall_object.position.y = 0
        self.__fall_object.rect.x = round(self.__fall_object.position.x)
        self.__fall_object.rect.y = round(self.__fall_object.position.y)


    def begin_fall(self):
        if self.__running is True:
            return
        else:
            self.set_object()
            self.__fall_button.config(text="Abort", command=self.end_fall)
            self.__running = True
        self.widgets_visibility(False, False, False)
        ga = float(self.__ga_entry.get(False))
        ft = float(self.__time_entry.get(False))
        t = 0
        total = 0
        vel = 0
        while t < ft:
            if not self.__running:
                break
            self.__camera.focus(self.__fall_object)
            t += 1/100
            vel = ga * t
            distance_traveled = vel * 1/100
            self.__fall_object.position.y += distance_traveled
            total += distance_traveled
            self.__fall_object.rect.y = round(self.__fall_object.position.y)
            time.sleep(1/100)


    def end_fall(self):
        self.__running = False
        self.__fall_button.config(text="Drop", command=self.begin_fall)
        self.widgets_visibility(True, True, True)
        self.__camera.reset_position()
        self.set_object()


    def show_output(self, output_text: str = "", button: Button = ...):
        self.__output_label = Label(self.__screen, font=self.__font, text=output_text,
                             bg=LIGHT_GRAY2, fg=BLACK)
        if isinstance(button, Button):
            button.config(state="disabled")
        time.sleep(2)
        if isinstance(button, Button):
            button.config(state="normal")
        del self.__output_label


    def mainloop(self):
        """Main game loop
        """
        prev_time = time.time()
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 0
                for entry in self.__entries:
                    entry.handle_entry_events(event)

            self.__screen.fill("#FFFFFF")
            self.__camera.update(dt)
            self.__camera.custom_draw()
            self.draw_widget()
            pygame.display.flip()
            self.__clock.tick(FPS)
