from typing import Dict

import pygame

import game_objects
import gui
from algos import matrix1


class SceneManager:
    def __init__(self, display):
        self.display = display
        self.__active_scene = None

        self.old_scene = None
        self.use_old_scene = False

    def new_scene(self, scene, flag=False, coords=(0, 0)):
        if flag is True:
            self.old_scene = self.scene
            self.use_old_scene = True
            self.coords = coords

        else:
            self.use_old_scene = False
        self.__active_scene = scene
        self.__active_scene.set_offset(*coords)

    def update(self, events):
        self.__active_scene.update(events)

    def render(self):
        self.__active_scene.render()

    def next_step(self, events):
        if self.use_old_scene is True:
            self.old_scene.render()

            sur = self.__active_scene.render_display()
            self.display.blit(sur, self.coords)

            self.update(events)

        else:
            self.update(events)
            self.render()

    def stop_old_scene(self):
        self.__active_scene = self.old_scene
        self.use_old_scene = False

    @property
    def scene(self):
        return self.__active_scene


class Scene:
    def __init__(self, display, scene_manager: SceneManager):
        self._display = display
        self.objects = []

        self.scene_manager = scene_manager

        self.callbacks = {}

        self._variables = {}

    def callback(self, name, kwargs: Dict = {}):
        self.callbacks.get(name)(**kwargs)

    def update(self, events):
        self.handling_events(events)

        for obj in self.objects:
            ans = obj.update()
            if ans is not None:
                self.callbacks.get(ans[0])(ans[1])

    def handling_events(self, events):
        for event in events:
            for obj in self.objects:
                if obj.check_event(event):
                    obj.click(event)
            if event.type == pygame.QUIT:
                exit(0)

    def render(self):
        for obj in self.objects:
            obj.render(self._display)

    def render_display(self):
        self.render()
        return self._display

    def add_obj(self, obj):
        self.objects.append(obj)

    @property
    def display(self):
        return self._display

    def discharge(self):
        pass

    def search_obj(self, name):
        for obj in self.objects:
            if obj.name == name:
                return obj

    def search_all_obj(self, name):
        _ = []
        for obj in self.objects:
            if obj.name == name:
                _.append(obj)

        return _

    def set_offset(self, x, y):
        pass


class Main(Scene):
    def __init__(self, display, scene_manager):
        super().__init__(display, scene_manager)

        self.objects.append(game_objects.MyGrid((0, 0), 30, (15, 15), matrix1))
