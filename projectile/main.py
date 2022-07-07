"""
Main file for projectile motion
• Add widgets allowing users to:
    ### Maybe
    - In-game setting UI, allowing users to modify:
        + Camera's panning speed
        + Camera's zoom speed
        + Camera's zoom limit
        + Invert x/y axis
        + Change keyboard control
        + Change boundary size (Or remove boundary completely)
        + Change gravity value
        + Invert gravity
        + Change impulse force modifier
    ###
    - Move obstacle (by name)
    - Reset game window
"""
import time
from pathlib import Path
from collections import deque

import pymunk
from pymunk.pygame_util import *
from pymunk.vec2d import Vec2d
import pygame
from pygame.locals import *

from includes import Button, Label, Entry, Listbox
from projectile.includes import (
    Projectile, Boundary, StaticObstacle, Camera, ObjectSelector, SIZE, GRAY, RED, FPS,
    G_HORIZONTAL, G_VERTICAL, after, blur_screen, get_offset, pg_coord, pm_coord
)

class ProjectileMain:
    """Projectile Motion main class. Entry point for menu
    """
    def __init__(self):
        """Initiate the simulation
        """
        pygame.init()
        self.__space = pymunk.Space()
        self.__screen = pygame.display.set_mode(SIZE)
        self.__clock = pygame.time.Clock()
        self.__draw_options = DrawOptions(self.__screen)
        self.__times_15 = pygame.font.Font(rf"{Path(__file__).parent}\assets\fonts\times.ttf", 15)
        self.__times_20 = pygame.font.Font(rf"{Path(__file__).parent}\assets\fonts\times.ttf", 20)
        self.__times_25 = pygame.font.Font(rf"{Path(__file__).parent}\assets\fonts\times.ttf", 25)

        self.__camera = Camera(5, 0.01, 0.01)
        self.__selected_object = ObjectSelector.Line.name
        self.__object_queue = deque(ObjectSelector)

        self.__running = True
        self.__is_menu_visible = True
        self.__is_description_visible = False
        self.__is_object_list_visible = False
        self.__is_prompt_visible = False
        self.__desc_visible_before_pull = False
        self.__menu_visible_before_pull = True
        self.__ready_to_step = False
        self.__during_query = False
        self.__show_info = False
        self.__pulling = False

        self.__impulse = -1000
        self.__max_obstacles = 20
        self.__objects = []
        self.__entries = []

        self.__space.gravity = G_HORIZONTAL, G_VERTICAL
        self.__active_shape = None

        for segment in Boundary(self.__space.static_body, (0, 0), (1200, 600)).segments:
            self.__space.add(segment)
        self.__create_projectile((100, 100), 25)

    def init_widgets(self):
        """Initiate widgets
        """
        self.__label_info = Label(self.__screen, self.__times_20, "", "#000000", "#E0E0E0",
                                  'center')
        self.__label_object_name = Label(self.__screen, self.__times_20,
                                         f"{self.__selected_object}", "#FFFFFF", "#393939")
        self.__label_name = Label(self.__screen, self.__times_20, "Name",
                                  "#FFFFFF", "#393939")
        self.__label_multiplier = Label(self.__screen, self.__times_20, "Multiplier (Radius)",
                                        "#FFFFFF", "#393939")
        self.__label_position = Label(self.__screen, self.__times_20, "Position (x, y)",
                                      "#FFFFFF", "#393939")
        self.__label_prompt = Label(self.__screen, self.__times_20, "",
                                    "#000000", "#DFDFDF")
        self.__btn_up = Button(self.__screen, self.__times_15, "/\\",
                               command=self.__change_object, args=(1,))
        self.__btn_down = Button(self.__screen, self.__times_15, "\/",
                                 command=self.__change_object, args=(-1,))
        self.__btn_create_object = Button(self.__screen, self.__times_15,
                                          f"Create {self.__selected_object}",
                                          command=self.__create, args=(self.__selected_object,))
        self.__btn_remove_object = Button(self.__screen, self.__times_15,
                                          "Remove Object By Name",
                                          command=self.__remove)
        self.__btn_show_object_list = Button(self.__screen, self.__times_15,
                                             "Show Object List",
                                             command=self.__show_object_list)
        self.__btn_description_visibility = Button(self.__screen, self.__times_15,
                                                   "Show Descriptions",
                                                   command=self.__toggle_desc_visibility)
        self.__btn_menu_visibility = Button(self.__screen, self.__times_15,
                                      "Collapse Menu", command=self.__toggle_menu_visibility)
        self.__btn_prompt_yes = Button(self.__screen, self.__times_15, "Yes",
                                       lambda: None)
        self.__btn_prompt_no = Button(self.__screen, self.__times_15, "No",
                                      lambda: None)
        self.__entry_name = Entry(self.__screen, self.__times_20, "",
                                  border_width=3, clear_on_focus=True)
        self.__entry_multiplier = Entry(self.__screen, self.__times_20, "",
                                  border_width=3, clear_on_focus=True,
                                  regex_filter=r"^( )?([0-9])+( )?$")
        self.__entry_pos_x = Entry(self.__screen, self.__times_20, "", bg=GRAY + "00",
                                   border_width=3, regex_filter=r"^( )?([0-9])+( )?$",
                                   clear_on_focus=True)
        self.__entry_pos_y = Entry(self.__screen, self.__times_20, "", bg=GRAY + "00",
                                   border_width=3, regex_filter=r"([0-9])+",
                                   clear_on_focus=True)
        self.__object_list = Listbox(self.__screen, self.__times_25, self.__max_obstacles,
                                             50, 10, bg_color="#FFFFFF", text_color="#000000")
        self.__entries = [self.__entry_name, self.__entry_multiplier,
                          self.__entry_pos_x, self.__entry_pos_y]
        self.__buttons = [self.__btn_up, self.__btn_down, self.__btn_create_object,
                          self.__btn_remove_object, self.__btn_menu_visibility,
                          self.__btn_description_visibility, self.__btn_show_object_list]

    def __draw_widgets(self):
        """Draw widgets on screen
        """
        if self.__show_info:
            self.__label_info.place(0, 0, SIZE[0], 75)
        if self.__is_menu_visible:
            self.__btn_menu_visibility.place(1000, 500, 200, 50)
            self.__btn_up.place(1000, 35, 200, 25)
            self.__label_object_name.place(1000, 60, 200, 50)
            self.__btn_down.place(1000, 110, 200, 25)
            self.__btn_create_object.place(1000, 280, 200, 50)
            self.__btn_remove_object.place(1000, 335, 200, 50)
            self.__btn_show_object_list.place(1000, 390, 200, 50)
            self.__btn_description_visibility.place(1000, 445, 200, 50)
            self.__entry_name.place(1000, 150, 200, 35)
            self.__entry_multiplier.place(1000, 190, 200, 35)
            self.__entry_pos_x.place(1000, 230, 95, 35)
            self.__entry_pos_y.place(1105, 230, 95, 35)
        else:
            self.__btn_menu_visibility.place(1150, 500, 50, 50)
        if self.__is_object_list_visible:
            blur_screen(self.__screen, strength="99")
            self.__btn_show_object_list.place(1000, 390, 200, 50)
            self.__object_list.place(200, 100, 800, 400)
        if self.__is_prompt_visible:
            blur_screen(self.__screen ,strength="99")
            self.__label_prompt.place(385, 200, 430, 190)
            self.__btn_prompt_yes.place(385,400,200,50)
            self.__btn_prompt_no.place(615,400,200,50)
        if self.__is_description_visible:
            self.__label_name.place(800, 150, 200, 35)
            self.__label_multiplier.place(800, 190, 200, 35)
            self.__label_position.place(800, 230, 200, 35)

    def __update_create_button(self):
        self.__label_object_name.config(text=f"{self.__selected_object}")
        self.__btn_create_object.config(text=f"Create {self.__selected_object}",
                                        command=self.__create, args=(self.__selected_object,))

    def __change_object(self, rotation: int):
        self.__btn_up.config(state="disabled")
        self.__object_queue.rotate(rotation)
        self.__selected_object = self.__object_queue[0].name
        self.__update_create_button()
        time.sleep(0.5)
        self.__btn_up.config(state="normal")

    def __create(self, shape):
        while self.__ready_to_step or self.__during_query:
            self.__btn_create_object.config(state="disabled")
            self.__btn_remove_object.config(state="disabled")
            for entry in self.__entries:
                entry.config(state="disabled")
            self.__show_info = True
            self.__label_info.config(text="Waiting for space to step or query to finish")
        else:
            if any([not bool(entry.get(False)) for entry in self.__entries]):
                self.__show_info = True
                self.__label_info.config("Please fill all the fields")
                for entry in self.__entries:
                    entry.config(state="normal")
                self.__btn_create_object.config(state="normal")
                self.__btn_remove_object.config(state="normal")
                after(2, self.__remove_error_message)
                return
            self.__show_info = False
            self.__btn_create_object.config(state="normal")
            self.__btn_remove_object.config(state="normal")
            for entry in self.__entries:
                entry.config(state="normal")
            obj_name = self.__entry_name.get()
            pos = (self.__entry_pos_x.get(as_type=int), self.__entry_pos_y.get(as_type=int))
            radius = multiplier = self.__entry_multiplier.get(as_type=int)
            tmp_object = StaticObstacle(obj_name, pos, shape, multiplier, radius=radius)
            self.__objects.append(tmp_object)
            self.__space.add(tmp_object.body, tmp_object.shape)
            self.__object_list.add_item(obj_name, self.__prompt_remove, (obj_name,), obj_name)

    def __prompt_remove(self, name: str | None = ...):
        if not self.__is_prompt_visible:
            self.__is_prompt_visible = True
            self.__label_prompt.config(f"Are you sure you want to delete {name}?")
            self.__btn_prompt_yes.config(command=self.__remove, args=(name,))
            self.__btn_prompt_no.config(command=self.__prompt_remove)
        else:
            self.__is_prompt_visible = False

    def __remove(self, name: str | None = None):
        while self.__ready_to_step or self.__during_query:
            self.__btn_create_object.config(state="disabled")
            self.__btn_remove_object.config(state="disabled")
            for entry in self.__entries:
                entry.config(state="disabled")
            self.__show_info = True
            self.__label_info.config(text="Waiting for space to step or query to finish")
        else:
            if not name and not bool(self.__entry_name.get(False)):
                self.__show_info = True
                self.__label_info.config("Please fill \"name\" field")
                for entry in self.__entries:
                    entry.config(state="normal")
                self.__btn_create_object.config(state="normal")
                self.__btn_remove_object.config(state="normal")
                after(2, self.__remove_error_message)
                return
            elif name:
                remove_name = name
            else:
                remove_name = self.__entry_name.get()
            self.__show_info = False
            if not self.__is_object_list_visible:
                self.__btn_create_object.config(state="normal")
                self.__btn_remove_object.config(state="normal")
                for entry in self.__entries:
                    entry.config(state="normal")
            for object in self.__objects:
                if object.name == remove_name:
                    self.__space.remove(object.shape, object.body)
                    self.__objects.remove(object)
                    self.__object_list.remove_item(object.name)
        if self.__is_prompt_visible:
            self.__prompt_remove()

    def __remove_error_message(self):
        self.__show_info = False

    def __show_object_list(self):
        if not self.__is_object_list_visible:
            self.__is_object_list_visible = True
            self.__btn_show_object_list.config("Hide Object List")
            for button in self.__buttons:
                button.config(state="disabled")
            self.__btn_show_object_list.config(state="normal")
            self.__btn_menu_visibility.config(state="disabled")
        else:
            self.__is_object_list_visible = False
            self.__btn_show_object_list.config("Show Object List")
            for button in self.__buttons:
                button.config(state="normal")
            self.__btn_menu_visibility.config(state="normal")

    def __toggle_menu_visibility(self):
        self.__btn_description_visibility.config(state="disabled")
        self.__btn_menu_visibility.config(state="disabled")
        if self.__is_menu_visible:
            self.__is_menu_visible = False
            self.__menu_visible_before_pull = False
            self.__btn_menu_visibility.config("+")
            if self.__is_description_visible:
                self.__toggle_desc_visibility()
        else:
            self.__is_menu_visible = True
            self.__menu_visible_before_pull = True
            self.__btn_menu_visibility.config("Collapse")
        time.sleep(0.5)
        self.__btn_description_visibility.config(state="normal")
        self.__btn_menu_visibility.config(state="normal")

    def __toggle_desc_visibility(self):
        self.__btn_description_visibility.config(state="disabled")
        self.__btn_menu_visibility.config(state="disabled")
        if self.__is_description_visible:
            self.__is_description_visible = False
            self.__desc_visible_before_pull = False
            self.__btn_description_visibility.config("Show Description")
        else:
            self.__is_description_visible = True
            self.__desc_visible_before_pull = True
            self.__btn_description_visibility.config("Hide Description")
        time.sleep(0.5)
        self.__btn_description_visibility.config(state="normal")
        self.__btn_menu_visibility.config(state="normal")

    def __handle_camera_movement(self):
        if any([entry.get_status() for entry in self.__entries]):
            return
        keys = pygame.key.get_pressed()
        self.__camera_transform = self.__camera.compute_translation_and_scaling(keys)
        self.__draw_options.transform = (
            pymunk.Transform.translation(int(SIZE[0] / 2), int(SIZE[1] / 2))
            @ pymunk.Transform.scaling(self.__camera_transform[1])
            @ self.__camera_transform[0]
            @ pymunk.Transform.rotation(self.__camera_transform[2])
            @ pymunk.Transform.translation(-int(SIZE[0] / 2), -int(SIZE[1] / 2))
        )

    def __create_projectile(self, pos: tuple | None = ..., size: int = 20):
        if any([entry.get_status() for entry in self.__entries]):
            return
        if not isinstance(pos, tuple):
            spawn_pos = pm_coord(pygame.mouse.get_pos(), get_offset(self.__camera), self.__screen)
        else:
            spawn_pos = pos
        projectile = Projectile(spawn_pos, radius=size)
        self.__space.add(projectile.body, projectile.shape)

    def __pull_handle(self):
        if self.__pulling:
            if self.__is_menu_visible:
                self.__btn_menu_visibility.config(state="disabled", text="+")
                self.__is_menu_visible = False
                self.__is_description_visible = False
            else:
                self.__is_description_visible = False
                self.__btn_menu_visibility.config(state="disabled")
        else:
            self.__is_menu_visible = self.__menu_visible_before_pull
            self.__is_description_visible = self.__desc_visible_before_pull
            if self.__is_menu_visible and not self.__is_object_list_visible:
                self.__btn_menu_visibility.config(state="normal", text="Collapse")
            elif self.__is_menu_visible and self.__is_object_list_visible:
                self.__btn_menu_visibility.config(state="disabled", text="Collapse")
            else:
                self.__btn_menu_visibility.config(state="normal")

    def mainloop(self):
        """Mainloop
        """
        pygame.display.set_caption("Projectile Motion Simulation (PMS)")

        while self.__running:
            if pygame.event.peek(pygame.QUIT):
                pygame.quit()
                self.__running = False
                return 0
            if self.__is_object_list_visible:
                pygame.event.clear(pygame.MOUSEBUTTONDOWN)
            for event in pygame.event.get():
                for entry in self.__entries:
                    entry.handle_entry_events(event)
                if event.type == KEYDOWN:
                    if event.key == K_c:
                        self.__create_projectile()
                    elif event.key == K_BACKSPACE and self.__active_shape != None:
                        self.__space.remove(self.__active_shape, self.__active_shape.body)
                        self.__active_shape = None
                elif event.type == MOUSEBUTTONDOWN:
                    pg_position = pm_coord(pygame.mouse.get_pos(), get_offset(self.__camera),
                                           self.__screen)
                    self.__active_shape = None
                    for body in self.__space.bodies:
                        if body.body_type == pymunk.Body.DYNAMIC:
                            shape_pos = list(body.shapes)[0]
                            self.__during_query = True
                            q_info = shape_pos.point_query(pg_position)
                            self.__during_query = False
                            distance = q_info.distance
                            if distance < 0:
                                self.__active_shape = shape_pos
                                self.__pulling = True
                                shape_pos.body.angle = (pg_position - shape_pos.body.position).angle
                elif event.type == MOUSEMOTION:
                    self.__m_position = event.pos
                elif event.type == MOUSEBUTTONUP:
                    if self.__pulling:
                        self.__pulling = False
                        pt2 = pm_coord(event.pos, get_offset(self.__camera), self.__screen)
                        pt1 = Vec2d(*self.__active_shape.body.position)
                        imp = self.__impulse * (pt1 - pt2).rotated(-self.__active_shape.body.angle)
                        self.__active_shape.body.apply_impulse_at_local_point(imp)

            self.__ready_to_step = True
            self.__pull_handle()
            self.__screen.fill(GRAY)
            self.__handle_camera_movement()
            self.__space.debug_draw(self.__draw_options)
            self.__draw_widgets()

            if self.__active_shape != None:
                shape_pos = self.__active_shape.body.position
                radius = int(self.__active_shape.radius)
                pg_position = pg_coord(shape_pos, get_offset(self.__camera), self.__screen, "+")
                pygame.draw.circle(self.__screen, RED, pg_position, radius, 3)
                if self.__pulling:
                    pygame.draw.line(self.__screen, RED, pg_position, self.__m_position, 3)
                    pygame.draw.circle(self.__screen, RED, self.__m_position, radius, 3)

            self.__space.step(0.01)
            self.__ready_to_step = False
            pygame.display.flip()
            self.__clock.tick(FPS)
