import pygame
from typing import Optional
from engine.media import Image

import logging
GameEngineLogger = logging.getLogger("Game")

class Game:
    def __init__(self, width: int, height: int, fullscreen=False, caption: Optional[str] = None):
        self._is_running = True
        pygame.init()
     
        self._screen = pygame.Surface((width, height))
        if fullscreen:
            self._display: pygame.Surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self._display: pygame.Surface = pygame.display.set_mode(self._screen.get_size())
            self._screen = self._display
        if caption is not None:
            pygame.display.set_caption(caption)
        self.flag = Image("flag")
        self.flag.load(self)
    
    def end(self):
        self._is_running = False

    def run(self) -> None:
        while self._is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end()
            self.flag.draw(pygame.Rect(200, 300, 0,0), False)
            pygame.display.flip()
        pygame.quit()
        
    @property
    def screen(self) -> "pygame.Surface":
        return self._screen