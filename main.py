"""Main

Main file. Run this file
"""
import sys
import tkinter as tk
from threading import Thread
from includes.constants import WIN_WIDTH, WIN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, \
    GREEN
from freefall.main import FreeFallSim
from freefall.main_2 import FreeFallSimExp
from light.main import LightRefraction
from pendulum.main import PendulumMain
from projectile.main import ProjectileMain

class Main:
    """Main
    Main class
    """
    def __init__(self, ff_exp: bool = False) -> None:
        """Init
        """
        self.__root = tk.Tk()
        self.__root.title("S4VN: Final Project")
        self.__root.resizable(False, False)
        self.__root.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}"
                           f"+{int(SCREEN_WIDTH / 2 - WIN_WIDTH / 2)}"
                           f"+{int(SCREEN_HEIGHT / 2 - WIN_HEIGHT / 2)}")
        self.__root.protocol("WM_DELETE_WINDOW", self.protocol_quit)

        if isinstance(ff_exp, bool):
            self.__ff_exp = ff_exp

    def init_widget(self):
        """Init widget.
        Init widgets displayed on screen
        """
        self.__freefall_button = tk.Button(self.__root, text="Freefall",
                                         command=lambda: Thread(target=self.start_ff).start(),
                                         font=("Times New Roman", 25), bg=GREEN)
        self.__pendulum_button = tk.Button(self.__root, text="Pendulum",
                                           command=self.start_pen,
                                           font=("Times New Roman", 25), bg=GREEN)
        self.__projectile_button = tk.Button(self.__root, text="Projectile Motion",
                                           command=self.start_pms,
                                           font=("Times New Roman", 25), bg=GREEN)
        self.__light_refraction = tk.Button(self.__root, text="Light Refraction",
                                           command=self.start_light,
                                           font=("Times New Roman", 25), bg=GREEN)

    def draw_widget(self):
        """Draw widget
        Draw widgets initiated in init_widget
        """
        self.__freefall_button.place(x=100, y=75, width=400, height=100)
        self.__pendulum_button.place(x=100, y=180, width=400, height=100)
        self.__projectile_button.place(x=100, y=285, width=400, height=100)
        self.__light_refraction.place(x=100, y=390, width=400, height=100)

    def start_ff(self):
        """start_ff
        Start freefall simulation
        """
        if self.__ff_exp:
            ffs = FreeFallSimExp()
        else:
            ffs = FreeFallSim()
        self.__root.withdraw()
        #ffsr = ffs.mainloop()
        ffs.init_widgets()
        ffs.mainloop()
        self.__root.deiconify()

    def start_pen(self):
        """start_pen
        Start Pendulum simulation
        """
        self.__root.withdraw()
        pendulum = PendulumMain()
        pendulum.init_widgets()
        pendulum.mainloop()
        self.__root.deiconify()

    def legacy_start(self):
        print("Deprecated")

    def start_pms(self):
        self.__root.withdraw()
        pms = ProjectileMain()
        pms.init_widgets()
        pms.mainloop()
        self.__root.deiconify()

    def start_light(self):
        self.__root.withdraw()
        light = LightRefraction()
        light.init_widgets()
        light.mainloop()
        self.__root.deiconify()

    def protocol_quit(self):
        """For root.protocol
        """
        self.__root.destroy()
        sys.exit()

    def run(self):
        self.__root.mainloop()


if __name__ == "__main__":
    FF_EXP = False
    if len(sys.argv) > 1:
        if "--ff-exp" in sys.argv:
            print("Using experimental version for freefall")
            FF_EXP = True
    main = Main(ff_exp=FF_EXP)
    main.init_widget()
    main.draw_widget()
    main.run()
