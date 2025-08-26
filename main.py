from engine.game import Game
from engine.media import Image
import logging

# nastavení loggeru
logging.basicConfig(
    level=logging.DEBUG,                               # logujeme od úrovně DEBUG výš
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",  # formát zprávy
    handlers=[                                          # kam zapisujeme
        logging.FileHandler("game.log"),                # do souboru
        logging.StreamHandler()                         # do konzole
    ]
)

# vytvoříme pojmenovaný logger
GameLogger = logging.getLogger("Main")

def main():
    Image.default_dir = 'res/imgs/'
    game_size = (1366, 768)
    game = Game(game_size[0], game_size[1], caption="Space Ground Adventure")
    game.run()
    GameLogger.info("The game_src was ended")


if __name__ == '__main__':
    try:
        GameLogger.info("Starting up!")
        main()
    except KeyboardInterrupt:
        GameLogger.info("Shutting down because interrupted")
    except Exception:
        GameLogger.critical("A fatal error has occurred", exc_info=True)