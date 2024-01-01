from settings import *
from os.path import join

class Score:
    def __init__(self):

        # general
        self.surface = pygame.Surface((360,100))
        self.rect = self.surface.get_rect(center = (WINDOW_WIDTH/2, 90))
        self.display_surface = pygame.display.get_surface()

        # ye
        self.end_height = 0
        self.font = pygame.font.Font(join('fonts','nocontinue.ttf'), 30)
        self.custom_image = pygame.transform.scale(pygame.image.load(join('visuals','WIDE_CUSTOM_BUTTON.jpg')), (80,50))

        # data
        self.known = 0
        self.unknown = 0
        self.remaining = 0

    def display_text(self, pos, text):
        text_surface = self.font.render(f'{text}', True, FINE_BLACK)
        text_rect = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        self.surface.fill(BOARD_COLOR)
        
        for index, points in enumerate([self.known, self.unknown, self.remaining]):
            x_pos = index * 140
            y_pos = self.surface.get_height() / 4 + self.end_height
            text_pos = (x_pos+self.custom_image.get_width()/2, y_pos+self.custom_image.get_height() / 2)

            self.surface.blit(self.custom_image, (x_pos,y_pos))
            self.display_text(text_pos, points)

        self.display_surface.blit(self.surface, self.rect)