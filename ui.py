import pygame

def event_exit() -> bool:
    is_running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False
    return is_running

_screen = None
def draw_screen(width: int, height: int, image: pygame.Surface) -> pygame.Surface:
    global _screen
    if _screen is None:
        _screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF, 32)
    # blit image on screen
    _screen.blit(image, (0, 0))
    return _screen

def print_fps(screen: pygame.Surface, clock: pygame.time.Clock):
    font = pygame.font.SysFont("monospace", 15)
    screen.blit(font.render("FPS %.2f"%(clock.get_fps()), 1, (255, 0, 0)), (0, 0))