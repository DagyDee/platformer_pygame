import pygame

class Game:
    def __init__(self):
        self._is_running = True
        pygame.init()
        self.display: pygame.Surface = pygame.display.set_mode((600, 600))
    
    def end(self):
        self._is_running = False

    def run(self) -> None:
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
            pygame.display.flip()
        pygame.quit()
        