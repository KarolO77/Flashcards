from settings import *
from game import Game
from score import Score

from sys import exit
from os.path import join


class Main:
    def __init__(self):

        # general
        pygame.init()
        pygame.display.set_caption("Fiszki")
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        # data
        with open(join("Fiszki.txt"), "r", encoding="UTF-8") as file:
            self.data = [
                i.replace("–", "-").strip().upper()
                for i in file.read().strip().splitlines()
            ]

        # components
        self.game = Game(self.data, self.update_score)
        self.score = Score()

    def update_score(self, known, unknown, remaining):
        self.score.remaining = remaining
        self.score.unknown = unknown
        self.score.known = known
        
    def run(self):
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # game
            self.game.run()
            if self.game.started and not self.game.end_of_round:
                self.score.run()

            # updating the game
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    main = Main()
    main.run()