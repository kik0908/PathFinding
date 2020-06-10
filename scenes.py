from typing import Dict

import pygame

import game_objects
import gui


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


class MainMenu(Scene):
    def __init__(self, display, scene_manager):
        super().__init__(display, scene_manager)

        self.objects.append(gui.Button((90, 90), 26, 120, "Start game", lambda: self.scene_manager.new_scene(
            MainGame(self._display, self.scene_manager)), self,
                                       {'color': (0, 0, 0), 'bd_color': (255, 255, 255), 'bd_width': -1},
                                       {'color': (40, 40, 40), 'bd_color': (255, 255, 255), 'bd_width': 1}))

        self.objects.append(gui.Button((90, 120), 26, 120, "Exit", lambda: exit(0), self,
                                       {'color': (0, 0, 0), 'bd_color': (255, 255, 255), 'bd_width': -1},
                                       {'color': (40, 40, 40), 'bd_color': (255, 255, 255), 'bd_width': 1}))


class EndGame(Scene):
    def __init__(self, display, scene_manager, side):
        super().__init__(display, scene_manager)

        self.side = side

        self.top = display.get_size()[1] / 2
        self.center = display.get_size()[0] / 2

    def set_offset(self, x, y):
        self.objects.append(gui.Label((self.center - 50, self.top - 60), 50, 100, f'{self.side} is winner!', self,
                                      {'color': (0, 0, 0), 'bd_color': (255, 255, 255), 'bd_width': -1}))

        self.objects.append(gui.Button((self.center - 100 - 2, self.top - 5, x, y), 50, 100, "Main menu",
                                       lambda: self.scene_manager.new_scene(
                                           MainMenu(self.scene_manager.display, self.scene_manager)), self,
                                       {'color': (0, 0, 0), 'bd_color': (255, 255, 255), 'bd_width': -1},
                                       {'color': (40, 40, 40), 'bd_color': (255, 255, 255), 'bd_width': 1}))

        self.objects.append(gui.Button((self.center + 2, self.top - 5, x, y), 50, 100, "Return",
                                       lambda: self.scene_manager.new_scene(
                                           MainGame(self.scene_manager.display, self.scene_manager)), self,
                                       {'color': (0, 0, 0), 'bd_color': (255, 255, 255), 'bd_width': -1},
                                       {'color': (40, 40, 40), 'bd_color': (255, 255, 255), 'bd_width': 1}))

    def render(self):
        self.display.set_alpha(245)
        self.display.fill((128, 128, 128))
        for obj in self.objects:
            obj.render(self.display)

    def render_display(self):
        self.render()
        return self.display


class MainGame(Scene):
    def __init__(self, display, scene_manager):
        super().__init__(display, scene_manager)

        self.objects.append(game_objects.TicTacToeGrid((0, 55), 100, (3, 3), width=2, scene=self))
        self.objects.append(gui.Button((1, 1), 50, 100, "Main menu",
                                       lambda: self.scene_manager.new_scene(MainMenu(display, scene_manager)), self,
                                       {'color': (0, 0, 0), 'bd_color': (255, 255, 255), 'bd_width': -1},
                                       {'color': (40, 40, 40), 'bd_color': (255, 255, 255), 'bd_width': 1}))

        self.callbacks.update([('player_win', self.__player_win), ('change_player', self.__change_size)])

        self._variables['player'] = 'x'
        self._variables['x'] = 'First player move'
        self._variables['y'] = 'Second player move'

        self.objects.append(
            gui.Label((101, 1), 50, 170, {'text': 'First player move', 'size': 20, 'color': (255, 255, 255)}, self,
                      {'color': (214, 123, 45), 'bd_color': (255, 255, 255), 'bd_width': -1}, 'left', 'size'))

    def __player_win(self, char):
        self.scene_manager.new_scene(EndGame(pygame.Surface((300, 120)), self.scene_manager, char), True, (1, 130))

    def __change_size(self):
        self._variables['player'] = 'x' if self._variables['player'] == 'y' else 'y'
        self.search_obj('size').edit_text(self._variables[self._variables['player']])

    def discharge(self):
        self.scene_manager.new_scene(MainGame(self._display, self.scene_manager))
