import pygame
import time

def event_exit() -> bool:
    is_running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
    return is_running

t_start = time.monotonic()
def print_fps(clock: pygame.time.Clock, t_update_sec = 1):
    global t_start
    if (time.monotonic() - t_start) > t_update_sec:
        t_start = time.monotonic()
        print("FPS %.2f" % clock.get_fps())