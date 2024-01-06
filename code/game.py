from settings import *
from timer import Timer
from button import Button
from myfuncs import *

from os.path import join

class Game:
    def __init__(self, data, update_score):

        # general 
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (0, 0))

        self.frame_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT+20))
        self.frame_rect = self.frame_surface.get_rect(topleft = (0,-20))

        # connection
        self.update_score_func = update_score
        
        # status
        self.started = False
        self.end_of_round = False
        self.translation_view = False
        self.ended = False

        # fonts
        self.font = "Amble-Bold.ttf"
        self.card_font_size = 50 # 60
        self.def_font_size = 15 # 20
        self.card_font = pygame.font.Font(join('fonts',self.font), self.card_font_size)
        self.definition_font = pygame.font.Font(join('fonts',self.font), self.def_font_size)
        self.start_font = pygame.font.Font(join('fonts',self.font), 30) # 40

        # dictionaries
        self.data = data
        self.all_words_dict = dict()

        self.displayed_current_word = ''
        self.displayed_current_translation = ''

        self.unknown_keys = []
        self.known_keys = []

        #buttons
        self.card_image = pygame.image.load(join('visuals','CARD.jpg'))
        self.continue_image = pygame.image.load(join('visuals','WIDE_CUSTOM_BUTTON.jpg')) # same for restart button

        self.dict_button_image = pygame.transform.scale(self.card_image, (self.card_image.get_width()*0.75, self.card_image.get_height()//2))
        self.known_image = pygame.transform.scale(self.continue_image, (80,80))

        self.buttons = {
            'card' : Button((WINDOW_WIDTH//2 - self.card_image.get_width()//2, self.card_image.get_height()//2), self.card_image),
            'left_dict' : Button((WINDOW_WIDTH//2 - self.dict_button_image.get_width()//2, WINDOW_HEIGHT//5), self.dict_button_image, "WORD TO DEFINITION"),
            'right_dict' : Button((WINDOW_WIDTH//2 - self.dict_button_image.get_width()//2, WINDOW_HEIGHT//2), self.dict_button_image, "DEFINITION TO WORD"),
            'restart' : Button((WINDOW_WIDTH//2 + self.continue_image.get_width()//5, WINDOW_HEIGHT//2), self.continue_image, "RESTART"),
            'continue' : Button((WINDOW_WIDTH//2 - self.continue_image.get_width()*1.2, WINDOW_HEIGHT//2), self.continue_image, "CONTINUE"),
            'known' : Button((WINDOW_WIDTH//2 + self.known_image.get_width()//3, WINDOW_HEIGHT - self.known_image.get_height()*2 -10), self.known_image, ">>>"),
            'unknown' : Button((WINDOW_WIDTH//2 - self.known_image.get_width()*1.5, WINDOW_HEIGHT - self.known_image.get_height()*2 -10), self.known_image, "<<<")
        }

        # timer 
        self.timers = {
            'mouse' : Timer(MOUSE_WAIT_TIME),
            'key' : Timer(KEY_WAIT_TIME),
        }

        # points
        self.known = 0
        self.unknown = 0
        self.remaining = 0
    
    # update
    def get_mouse_pos(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()
            
    def update_score(self, command=None):
        if command == 'known':
            self.known += 1
            self.remaining -= 1
        elif command == 'unknown':
            self.unknown += 1
            self.remaining -= 1

        self.update_score_func(self.known, self.unknown, self.remaining)

    def check_game_buttons(self):
        self.keys = pygame.key.get_pressed()

        if not self.started:
            if not self.timers['mouse'].active:

                if self.buttons['left_dict'].clicked(self.mouse_pos):
                    self.create_left_to_right_words_dict()
                    self.get_next_word()
                    self.timers['mouse'].activate()

                if self.buttons['right_dict'].clicked(self.mouse_pos):
                    self.create_right_to_left_words_dict()
                    self.get_next_word()
                    self.timers['mouse'].activate()

        elif self.started:
            if not self.timers['mouse'].active:

                if self.buttons['card'].clicked(self.mouse_pos):
                    if self.translation_view == False:
                        self.translation_view = True
                    else:
                        self.translation_view = False
                    self.timers['mouse'].activate()

                if self.buttons['known'].clicked(self.mouse_pos):
                    self.known_word()
                    self.timers['mouse'].activate()

                if self.buttons['unknown'].clicked(self.mouse_pos):
                    self.unknown_word()
                    self.timers['mouse'].activate()

            if not self.timers['key'].active:

                if self.keys[pygame.K_d] or self.keys[pygame.K_RIGHT]:
                    self.known_word()
                    self.timers['key'].activate()

                if self.keys[pygame.K_a] or self.keys[pygame.K_LEFT]:
                    self.unknown_word()
                    self.timers['key'].activate()

    def check_end_buttons(self):
        if not self.timers['mouse'].active:

            if self.buttons['restart'].clicked(self.mouse_pos):
                self.restart_game()
                self.timers['mouse'].activate()

            if self.buttons['continue'].clicked(self.mouse_pos) and not self.ended:
                self.end_of_round = False
                self.update_score()
                self.timers['mouse'].activate()

    def restart_game(self):
        self.end_of_round = False
        self.ended = False
        self.started = False

        self.known = 0
        self.unknown = 0
        self.remaining = 0

        self.buttons['restart'] = Button((WINDOW_WIDTH//2 + self.continue_image.get_width()//5, WINDOW_HEIGHT//2), self.continue_image, "RESTART")
        self.unknown_keys.clear()
        self.all_words_dict.clear()

    # create dicts
    def create_left_to_right_words_dict(self):

        for phrase in self.data:
            p1, p2 = phrase.find(" - "), phrase.rfind(" - ")

            if p1 == p2:
                english_word = phrase[:p1]
                polish_word = phrase[p1+3:]
                self.all_words_dict[english_word] = (polish_word)

            elif p1 != p2:
                english_word = phrase[:p1]
                polish_word = phrase[p1+3:p2]
                definition_of_word = check_brackets(phrase[p2+3:])
                translated_definition = translate_text(definition_of_word)

                self.all_words_dict[english_word] = (polish_word, definition_of_word, translated_definition)

        self.remaining = len(self.all_words_dict)
        self.dict_gen = (i for i in self.all_words_dict.keys())
        self.update_score()
        self.started = True

    def create_right_to_left_words_dict(self):

        for phrase in self.data:
            p1, p2 = phrase.find(" - "), phrase.rfind(" - ")

            if p1 == p2:
                english_word = phrase[:p1]
                polish_word = phrase[p1+3:]
                self.all_words_dict[polish_word] = (english_word)

            elif p1 != p2:
                english_word = phrase[:p1]
                polish_word = phrase[p1+3:p2]
                definition_of_word = check_brackets(phrase[p2+3:])
                translated_definition = translate_text(definition_of_word)

                self.all_words_dict[polish_word] = (english_word, translated_definition, definition_of_word)

        self.remaining = len(self.all_words_dict)
        self.dict_gen = (i for i in self.all_words_dict.keys())
        self.update_score()
        self.started = True
    
    # dict operations
    def get_next_word(self):
        try:
            self.current_word = next(self.dict_gen)

            if isinstance(self.all_words_dict[self.current_word], tuple):
                self.translation = self.all_words_dict[self.current_word][0]
                self.translated_definition = self.all_words_dict[self.current_word][1]
                self.native_definition = self.all_words_dict[self.current_word][2]
            else: 
                self.translation = self.all_words_dict[self.current_word]
                self.translated_definition = ''
                self.native_definition = ''
            self.card_update()

        except StopIteration:
            self.create_new_game()

    def create_new_game(self): # if list go out of words, create new dict
        if self.unknown_keys:
            self.unknown_keys = list(set(self.unknown_keys))
            self.dict_gen = (i for i in self.unknown_keys[:])

            self.known = 0
            self.unknown = 0
            self.remaining = len(self.unknown_keys)

            self.unknown_keys.clear()
            self.get_next_word()
            self.translation_view = False
            self.ended = False
        else:
            self.ended = True
            self.buttons['restart'].pos = (WINDOW_WIDTH//2 - self.continue_image.get_width()//2, WINDOW_HEIGHT//2)
            self.buttons['restart'].rect = self.buttons['restart'].image.get_rect(topleft = self.buttons['restart'].pos)
            self.buttons['restart'].text_pos = (WINDOW_WIDTH//2, self.buttons['restart'].text_pos[1])
            
        self.end_of_round = True

    def card_update(self):
        self.displayed_current_word = extract_phrase(adjust_text(self.current_word))
        self.cw_len = len(self.displayed_current_word)
        self.displayed_current_definition_word = extract_phrase(adjust_text(self.native_definition, 8))

        self.displayed_current_translation = extract_phrase(adjust_text(self.translation))
        self.ct_len = len(self.displayed_current_translation)
        self.displayed_current_definition_trans = extract_phrase(adjust_text(self.translated_definition, 8))

        self.translation_view = False

    def known_word(self):
        self.known_keys.append(self.current_word)
        self.update_score('known')
        self.get_next_word()

    def unknown_word(self):
        self.unknown_keys.append(self.current_word)
        self.update_score('unknown')
        self.get_next_word()

    # display
    def display_game(self):
        if not self.started:
            # choose dict bttns
            self.surface.blit(self.buttons['left_dict'].image, self.buttons['left_dict'].pos)
            display_text(self.surface, self.buttons['left_dict'].text, self.buttons['left_dict'].text_pos, self.start_font)

            self.surface.blit(self.buttons['right_dict'].image, self.buttons['right_dict'].pos)
            display_text(self.surface, self.buttons['right_dict'].text, self.buttons['right_dict'].text_pos, self.start_font)

        elif self.started:
            # know/mistake button
            self.surface.blit(self.buttons['known'].image, self.buttons['known'].pos)
            display_text(self.surface, self.buttons['known'].text, self.buttons['known'].text_pos, self.start_font)

            self.surface.blit(self.buttons['unknown'].image, self.buttons['unknown'].pos)
            display_text(self.surface, self.buttons['unknown'].text, self.buttons['unknown'].text_pos, self.start_font)

    def display_card(self):
        if self.started:
            self.surface.blit(self.buttons['card'].image, self.buttons['card'].pos)

            if not self.translation_view:
                # show current word
                for index, phrase in enumerate(self.displayed_current_word):
                    position = (self.buttons['card'].text_pos[0], 
                    self.buttons['card'].text_pos[1] - (self.card_font_size * (self.cw_len/2 - 0.5)) + index*(self.card_font_size))

                    display_text(self.surface, phrase, position, self.card_font)

                # show definition
                for index, phrase in enumerate(self.displayed_current_definition_word):
                    position = (self.buttons['card'].text_pos[0], 
                    self.buttons['card'].text_pos[1] + 90 + index*self.def_font_size)

                    display_text(self.surface, phrase, position, self.definition_font)
            

            elif self.translation_view:
                # show translation
                for index, phrase in enumerate(self.displayed_current_translation):
                    position = (self.buttons['card'].text_pos[0], 
                    self.buttons['card'].text_pos[1] - (self.card_font_size * (self.ct_len/2 - 0.5)) + index*(self.card_font_size))

                    display_text(self.surface, phrase, position, self.card_font)

                # show definition
                for index, phrase in enumerate(self.displayed_current_definition_trans):
                    position = (self.buttons['card'].text_pos[0], 
                    self.buttons['card'].text_pos[1] + 90 + index*self.def_font_size)

                    display_text(self.surface, phrase, position, self.definition_font)

    def display_end(self): # end of round || end of game
        if not self.ended:
            # continue
            self.surface.blit(self.buttons['continue'].image, self.buttons['continue'].pos)
            display_text(self.surface, self.buttons['continue'].text, self.buttons['continue'].text_pos, self.start_font)

            # restart
            self.surface.blit(self.buttons['restart'].image, self.buttons['restart'].pos)
            display_text(self.surface, self.buttons['restart'].text, self.buttons['restart'].text_pos, self.start_font)
        
        elif self.ended:
            self.surface.blit(self.buttons['restart'].image, self.buttons['restart'].pos)
            display_text(self.surface, self.buttons['restart'].text, self.buttons['restart'].text_pos, self.start_font)
   
    # run
    def run(self):

        # update
        self.get_mouse_pos()
        self.timer_update()

        # game
        self.surface.fill(BOARD_COLOR)

        if not self.end_of_round:
            self.check_game_buttons()
            self.display_game()
            self.display_card()

        if self.end_of_round:
            self.check_end_buttons()
            self.display_end()

        # screen + frame
        self.display_surface.blit(self.surface, self.rect)
        pygame.draw.rect(self.display_surface, WHITE, self.frame_rect, 20)