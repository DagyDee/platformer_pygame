from engine.game import Game
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
logger = logging.getLogger("Game")

def main():
    game = Game()
    game.run()
    logger.info("The game_src was ended")

if __name__ == '__main__':
    try:
        logger.info("Starting up!")
        main()
    except KeyboardInterrupt:
        logger.info("Shutting down because interrupted")
    except Exception:
        logger.critical("A fatal error has occurred", exc_info=True)