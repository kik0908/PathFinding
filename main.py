import pygame

import scenes

WIDTH = 460
HEIGHT = 460
FPS = 60

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')

scene_manager = scenes.SceneManager(screen)
scene_manager.new_scene(scenes.Main(screen, scene_manager))

running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    events = pygame.event.get()
    scene_manager.next_step(events)

    pygame.display.flip()

pygame.quit()
