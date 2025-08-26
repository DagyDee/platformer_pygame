import pygame
from typing import Dict, Set, Optional, List, Callable  # modul typing umožnuje lepší kontrolu nad kódem
from pathlib import Path  # z relativní cesty vytvoří cestu absolutní

import logging
GameEngineLogger = logging.getLogger("Media")

class Image:
    default_dir = '.'  # výchozí složka s obrázky
    _accepted_extensions = ['.png', '.jpg', '.gif', '.bmp']
    _images_cache: Dict[str, List[pygame.Surface]] = {}

    def __init__(self, image_name: str, convert_size: Optional[tuple[int, int]] = None, load: bool = True):
     
        self.name = image_name
        self.speed = 0
        self._image_index = 0
        self._image_tick = 0
        self._size = (0, 0)

        self._game = None
        self._subimages: Optional[List[pygame.Surface]] = None

        if image_name in self._images_cache:  # Pokud je obrázek v cache, použij ho
            GameEngineLogger.debug(f"Image {image_name} is in cache")
            self._subimages = self._images_cache[image_name]
            self._count_size()
            return
        
        if not load:  # Pokud se obrázek nemá načítat
            GameEngineLogger.debug(f"Image {image_name} is not due to load")
            if not self._subimages:
                GameEngineLogger.debug(f"Image {image_name} has not been loaded, emptying all subimages")
                self._images_cache[image_name] = self._subimages
            return
        
        # --- Načtení obrázku z disku ---
        GameEngineLogger.debug(f"Loading image {image_name} from disk")

        image_dir = Path(self.default_dir).resolve()

        # Zkus složku se jménem image_name
        folder = image_dir / image_name
        if folder.is_dir():
            files = [f for f in folder.iterdir() if f.suffix in self._accepted_extensions]
        else:
            # Pokud složka neexistuje, hledej v root složce soubory začínající na image_name
            files = [f for f in image_dir.iterdir() if f.stem.startswith(image_name) and f.suffix in self._accepted_extensions]

        # Seřaď soubory podle názvu
        files.sort()

        # Načti obrázky
        self._subimages = [pygame.image.load(str(f)).convert_alpha() for f in files]

        # Pokud je potřeba, změň velikost
        if convert_size:
            self._subimages = [pygame.transform.scale(img, convert_size) for img in self._subimages]

        # Ulož do cache
        self._images_cache[image_name] = self._subimages

        self._count_size()


    def _count_size(self) -> tuple[int, int]:
        """Spočítá maximální šířku a výšku mezi všemi načtenými obrázky."""
        max_w = 0
        max_h = 0
        for sub in self._subimages:
            w, h = sub.get_size()
            if w > max_w:
                max_w = w
            if h > max_h:
                max_h = h
        self._size = (max_w, max_h)
        return self._size
    
    def load(self, game: "Game") -> None:
        self._game = game
    
    def draw(self, rect: pygame.Rect, resize=False) -> None:
        GameEngineLogger.debug(f"Drawing image {self.name}")
        img: "pygame.Surface" = self._subimages[self._image_index]
        if resize:
            GameEngineLogger.debug(f"Drawing image {self.name} - resizing")
            img = pygame.transform.scale(img, rect.size)
        if self.screen is not None:
            offset_x, offset_y = self.screen.get_abs_offset()
            self.screen.blit(img, (rect.x - offset_x, rect.y - offset_y))

    def transform(self, transformation: Callable):
        GameEngineLogger.debug(f"Transforming image {self.name}, has {len(self._subimages)} subimages")
        self._subimages = [transformation(img) for img in self._subimages]
        self._images_cache[self.name] = self._subimages

    @property
    def screen(self) -> Optional["pygame.Surface"]:
        if self._game is None:
            return None
        return self._game.screen
    
    @property
    def image_index(self) -> int:
        return self._image_index

    @image_index.setter
    def image_index(self, value: int) -> None:
        if value >= len(self._subimages):
            value %= len(self._subimages)
        self._image_index = value
        self._image_tick = 0

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    @size.setter
    def size(self, val: tuple[int, int]) -> None:

        def scale(img: pygame.Surface):
            new_surface = pygame.Surface(val).convert_alpha()
            pygame.transform.smoothscale(img, val, new_surface)
            return new_surface

        self.transform(scale)
        self._count_size()

    @property
    def subimage(self) -> Optional[pygame.Surface]:
        if not self._subimages:
            return None
        return self._subimages[self._image_index]