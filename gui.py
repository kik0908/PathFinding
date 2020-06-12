from string import ascii_letters, digits
import random

import pygame

from typing import Tuple, Dict, Optional

alphabet = ascii_letters + digits + ' '


class BaseGUIObject:
    def __init__(self, scene, rect=pygame.Rect(0, 0, 0, 0), name=''):
        self.rect = rect
        """
        state = 0 - passive
        state = 1 - hovered
        state = 2 - pressed
        state = 3 - active
        """
        self.state = 0
        self.scene = scene
        self.name = name

    def update(self):
        pass

    def render(self, display):
        pass

    def click(self):
        pass

    def check_event(self, event):
        pass


class TextInput(BaseGUIObject):
    def __init__(self, pos: Tuple[int, int, Optional[int], Optional[int]], height, width, scene, passive_state,
                 active_state=None, alphabet=alphabet, name=''):
        self.pos = pos[0:2]
        self.offset = pos[2:] if len(pos) == 4 else [0, 0]
        self.size = (height, width)
        self.passive_state = passive_state
        self.state = 0
        self.active_state = active_state if active_state is not None else passive_state

        super().__init__(scene, pygame.Rect(self.pos, (width, height)), name)

        self.rect_for_check = self.rect.copy()
        self.rect_for_check.left += self.offset[0]
        self.rect_for_check.top += self.offset[1]

        self.alphabet = alphabet if type(alphabet) == list else list(alphabet)

        self.text = []
        self.size_text = height - 4
        self.char_count = 0

        self.surface = pygame.Surface((width, height))

        font = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font, self.size_text)
        self.text_surface = self.font.render(''.join(self.text), True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect()

        self.letters_x_offset = 0

        self.last_tick = pygame.time.get_ticks()
        self.cor_flag = False

    def check_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == 3:
                if event.key == 8:
                    if len(self.text) > 0:
                        self.text.pop()
                        self.text_surface = self.font.render(''.join(self.text), True, (255, 255, 255))
                        self.text_rect = self.text_surface.get_rect()
                        if len(self.text) != 0:
                            a = self.text_rect.width // len(self.text)
                            char_count = self.rect.width // a
                            if len(self.text) > char_count:
                                self.text_rect.right = self.rect.width - 8
                            else:
                                self.text_rect.left = 3

                elif event.unicode in self.alphabet:
                    self.text.append(event.unicode)

                    self.text_surface = self.font.render(''.join(self.text), True, (255, 255, 255))
                    self.text_rect = self.text_surface.get_rect()

                    a = self.text_rect.width // len(self.text)
                    char_count = self.rect.width // a
                    if len(self.text) > char_count:
                        self.text_rect.right = self.rect.width - 8
                    else:
                        self.text_rect.left = 3
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = 3
            else:
                self.state = 0

    def render(self, display):

        if self.state == 0:
            settings = self.passive_state
        else:
            settings = self.active_state

        self.surface.fill(settings['color'])
        _ = pygame.Rect(*(0, 0), *reversed(self.size))
        pygame.draw.rect(self.surface, self.passive_state['color'], _)

        if settings['bd_width'] >= 1:
            pygame.draw.rect(self.surface, settings['bd_color'], _, settings['bd_width'])

        self.surface.blit(self.text_surface, self.text_rect)

        display.blit(self.surface, (self.pos[0], self.pos[1] - 2))

        if self.state == 3:
            last_tick_ = pygame.time.get_ticks()
            if last_tick_ - self.last_tick >= 600:
                self.last_tick = last_tick_
                self.cor_flag = not self.cor_flag

        else:
            self.cor_flag = False

        if self.cor_flag is True:
            pygame.draw.line(display, (200, 200, 200),
                             (self.text_rect.right + self.pos[0] + 2, self.rect.top + 2),
                             (self.text_rect.right + self.pos[0] + 2, self.rect.bottom - 8), 2)


class Label(BaseGUIObject):
    def __init__(self, pos: Tuple[int, int], width, height, text: Dict, scene, passive_state, align='center', name=''):
        self.pos = pos[0:2]
        self.size = (width, height)
        self.text = text
        self.rect_style = passive_state
        self.align = align

        self.offset = pos[2:] if len(pos) == 4 else [0, 0]

        if type(text) == str:
            self.text = {'text': text, 'size': 20, 'color': (255, 255, 255)}

        super().__init__(scene, pygame.Rect(pos, (height, width)), name)

        self.rect_for_check = self.rect
        self.rect_for_check.left += self.offset[0]
        self.rect_for_check.top += self.offset[1]

        self.text['font'] = self.text.get('font', 'arial')
        font = pygame.font.match_font(self.text['font'])
        font = pygame.font.Font(font, self.text['size'])
        self.text_surface = font.render(self.text['text'], True, self.text['color'])
        self.text_rect = self.text_surface.get_rect()
        if self.align == 'center':
            self.text_rect.center = (self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2)
        elif self.align == 'left':
            self.text_rect.center = (self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2)
            self.text_rect.left = self.pos[0] + 2
        else:
            self.text_rect.center = (self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2)
            self.text_rect.right = self.pos[0] + self.rect.width - 2

    def render(self, display):
        pygame.draw.rect(display, self.rect_style['color'], self.rect, self.rect_style['bd_width'])

        display.blit(self.text_surface, self.text_rect)

    def edit_text(self, text: Dict):
        if type(text) == str:
            self.text = {'text': text, 'size': self.text['size'], 'color': self.text['color'], 'font': 'arial'}

        font = pygame.font.match_font(self.text['font'])
        font = pygame.font.Font(font, self.text['size'])
        self.text_surface = font.render(self.text['text'], True, self.text['color'])
        self.text_rect = self.text_surface.get_rect()
        if self.align == 'center':
            self.text_rect.center = (self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2)
        elif self.align == 'left':
            self.text_rect.center = (self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2)
            self.text_rect.left = self.pos[0] + 2
        else:
            self.text_rect.center = (self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2)
            self.text_rect.right = self.pos[0] + self.rect.width - 2


class Button(BaseGUIObject):
    def __init__(self, pos: Tuple[int, int, Optional[int], Optional[int]], width, height, text: Dict, func, scene,
                 passive_state, hovered_state=None,
                 pressed_state=None, name=''):
        """
        ***_state = = {'color': (int, int, int, int), 'bd_color':  (int, int, int, int), 'bd_width': 1}
        text = {'text': '', 'size'=int, 'color'=(int, int, int), 'font'=opt('')}
        """
        self.pos = pos[0:2]
        self.size = (height, width)

        self.offset = pos[2:] if len(pos) == 4 else [0, 0]

        self.func = func
        self.text = text

        super().__init__(scene, pygame.Rect(self.pos, (height, width)), name)

        self.rect_for_check = self.rect.copy()
        self.rect_for_check.left += self.offset[0]
        self.rect_for_check.top += self.offset[1]

        if type(text) == str:
            self.text = {'text': text, 'size': 20, 'color': (255, 255, 255)}

        self.text['font'] = self.text.get('font', 'arial')

        font = pygame.font.match_font(self.text['font'])
        font = pygame.font.Font(font, self.text['size'])
        self.text_surface = font.render(self.text['text'], True, self.text['color'])
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (self.pos[0] + self.rect.width / 2, self.pos[1] + self.rect.height / 2)

        self.states = {0: passive_state}
        if hovered_state is not None:
            self.states.update([(1, hovered_state)])
        if pressed_state is not None:
            self.states.update([(2, pressed_state)])

    def render(self, display):
        settings = self.states.get(self.state, self.states.get(1, self.states[0]))
        pygame.draw.rect(display, settings['color'], self.rect)

        if settings['bd_width'] >= 1:
            pygame.draw.rect(display, settings['bd_color'], self.rect, settings['bd_width'])
        display.blit(self.text_surface, self.text_rect)

    def click(self):
        self.func()

    def check_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect_for_check.collidepoint(*event.pos):
                self.state = 1
            else:
                self.state = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.rect_for_check.collidepoint(*event.pos):
                    self.click()


class CheckBox(BaseGUIObject):
    pass
