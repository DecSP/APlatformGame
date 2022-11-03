import pygame

import lib
from setting import *
from config import conf
from sound import sound


class Menu(object):

    GAME = GAME
    ALT = ""

    TITLE_COLOUR = "#E14D2A"#(0x00, 0x99, 0xFF) ## ??
    SELECTED_COLOUR = "#82CD47" ## ?? 
    UNSELECTED_COLOUR = WHITE #WHITE ## ?

    START = "START"
    OPTIONS = "OPTIONS"
    # SCORES = "High Scores"
    HELP = "HELP"
    QUIT = "QUIT"

    MAIN_OPTIONS = [START, OPTIONS, HELP, QUIT]

    FULLSCREEN = "Fullscreen Mode"
    SOUND = "Sounds"
    BACK = "Return to Main Menu"

    OPTIONS_OPTIONS = [FULLSCREEN, SOUND, BACK]
    OPTIONS_CONF = {FULLSCREEN: "fullscreen", SOUND: "sound"}

    NOSCORES = "There are no scores available at this time"

    EXIT_SURE = "Are you sure?"
    YES = "Yes"
    NO = "No"

    EXIT_OPTIONS = [YES, NO]

    HELP_TEXT = """\
Controls:

        Mouse Left Click
            Slow motion the game and character move to the mouse position but lost health

        ESC in game screen
            Pause the game or exit the main menu


Target:

        Collide the bird to get higher score
        Collide the star or box to get more health
        Do not collide the thorn and the lava bounding game due to lost much health
"""

    def __init__(self, game):
        self.game = game

    def _return_to_menu(self):
        self._display_func = self._main
        self._action_func = self._main_action
        self._choice = self._last_choice
        self._choice_max = len(self.MAIN_OPTIONS)

    def show(self):
        sound.play("title", -1)

        self._last_choice = 0
        self._return_to_menu()
        # background = lib.draw_background_menu()
        title = pygame.font.SysFont("Arial", 90, bold=True).render(self.GAME, True, self.TITLE_COLOUR)
        self.title_width = title.get_width()
        surf= pygame.Surface((screen_width-300,screen_height))
        surf.fill((0,0,0))
        surf.set_alpha(200)
        while True:

            # self.game.display_surface.blit(background, (0, 0))
            self.game.draw_bg()
            self.game.display_surface.blit(surf, (WIDTH / 2 - surf.get_width() / 2, 0))
            

            y_pos = 60

            #  lib.render_text(self.GAME, 72, self.TITLE_COLOUR)
            self.game.display_surface.blit(title, (WIDTH / 2 - self.title_width / 2, y_pos))
            y_pos += title.get_height()

            alt = lib.render_text(self.ALT, 22)
            alt_x = (
                (WIDTH - self.title_width) / 2 + self.title_width - alt.get_width() - 15
            )
            self.game.display_surface.blit(alt, (alt_x, y_pos))
            y_pos += alt.get_height() + 25

            self._display_func(y_pos)

            

            pygame.display.update()
            self.game.clock.tick(MENU_FRAME_RATE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # if in the main menu, exit, otherwise exit to main menu
                        if self._display_func == self._main:
                            self._last_choice = self._choice
                            self._choice = self.MAIN_OPTIONS.index(self.QUIT)
                            self._main_action(False)
                        elif self._display_func == self._exit:
                            raise SystemExit
                        else:
                            self._return_to_menu()
                    elif event.key == pygame.K_UP:
                        self._choice = (self._choice - 1) % self._choice_max
                        sound.play("menu_choosing")
                    elif event.key == pygame.K_DOWN:
                        self._choice = (self._choice + 1) % self._choice_max
                        sound.play("menu_choosing")
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        # If self._action_func() returns true, we leave the menu
                        if self._action_func():
                            sound.stop("title")
                            sound.play("menu_picked")
                            return
                        break

    def _main(self, y_pos):

        y_pos += 50 # ???

        for option_text in self.MAIN_OPTIONS:

            if option_text == self.MAIN_OPTIONS[self._choice]:
                colour = self.SELECTED_COLOUR ## ??
            else:
                colour = self.UNSELECTED_COLOUR ## ??

            option = pygame.font.SysFont("Arial", 40, bold=True).render(option_text, True, colour)
            option_width, option_height = option.get_width(), option.get_height()
            self.game.display_surface.blit(option, (WIDTH / 2 - option_width / 2, y_pos))

            if option_text == self.MAIN_OPTIONS[self._choice]:
                circ_y = y_pos + option_height / 2
                for sign in (-1, 1):
                    circ_pos = (WIDTH / 2 + sign * (option_width / 2 + 25), circ_y)
                    pygame.draw.circle(self.game.display_surface, colour, circ_pos, 5)

            y_pos += option_height + 30 # ???

    def _main_action(self, set_last_choice=True):
        """returns True if the main menu should exit (i. e. play selected)"""

        if set_last_choice:
            self._last_choice = self._choice

        if self.MAIN_OPTIONS[self._choice] == self.START:
            return True
        elif self.MAIN_OPTIONS[self._choice] == self.OPTIONS:
            choice_max = len(self.OPTIONS_OPTIONS)
            self._choice, self._choice_max = choice_max - 1, choice_max
            self._display_func = self._options
            self._action_func = self._options_action
        # elif self.MAIN_OPTIONS[self._choice] == self.SCORES:
        #     self._choice, self._choice_max = 0, 1
        #     self._display_func = self._highscores
        #     self._action_func = self._return_to_menu
        elif self.MAIN_OPTIONS[self._choice] == self.HELP:
            self._choice, self._choice_max = 0, 1
            self._display_func = self._help
            self._action_func = self._return_to_menu
        elif self.MAIN_OPTIONS[self._choice] == self.QUIT:
            self._choice, self._choice_max = 0, len(self.EXIT_OPTIONS)
            self._display_func = self._exit
            self._action_func = self._exit_action

    def _options(self, y_pos):

        y_pos += 50
        x_pos_text = WIDTH / 2 - self.title_width / 2 + 50
        x_pos_box = WIDTH / 2 + self.title_width / 2 - 100

        for option_text in self.OPTIONS_OPTIONS:

            if option_text == self.OPTIONS_OPTIONS[self._choice]:
                colour = self.SELECTED_COLOUR
            else:
                colour = WHITE

            option = lib.render_text(option_text, 24, colour)
            option_width, option_height = option.get_width(), option.get_height()

            if option_text == self.BACK:
                y_pos += option_height + 3  # same as the last line of the loop

            self.game.display_surface.blit(option, (x_pos_text, y_pos))

            if option_text != self.BACK:
                y_pos_box = y_pos + 1
                option_box_w = option_height - 2
                option_box = pygame.Rect(
                    x_pos_box, y_pos_box, option_box_w, option_box_w
                )
                # Line width here is 2
                if getattr(conf, self.OPTIONS_CONF[option_text]):
                    pygame.draw.line(
                        self.game.display_surface,
                        colour,
                        (x_pos_box, y_pos_box),
                        (x_pos_box + option_box_w, y_pos_box + option_box_w),
                        2,
                    )
                    pygame.draw.line(
                        self.game.display_surface,
                        colour,
                        (x_pos_box + option_box_w, y_pos_box),
                        (x_pos_box, y_pos_box + option_box_w),
                        2,
                    )
                pygame.draw.rect(self.game.display_surface, colour, option_box, 2)

            y_pos += option_height + 3

    def _options_action(self):
        sound.play("menu_switch")
        selection = self.OPTIONS_OPTIONS[self._choice]

        if selection == self.BACK:
            self._return_to_menu()
        else:
            # Flip bool value in conf
            attr = not getattr(conf, self.OPTIONS_CONF[selection])
            setattr(conf, self.OPTIONS_CONF[selection], attr)
            if selection == self.FULLSCREEN:
                self.game.set_screen()
            elif selection == self.SOUND:
                # will stop and replay if enabled
                sound.stop_all()
                sound.play("title", -1)

    # def _highscores(self, y_pos):
    #     highscore = lib.render_text(self.SCORES, 34)
    #     highscore_width = highscore.get_width()
    #     highscore_x = WIDTH / 2 - highscore_width / 2
    #     self.game.display_surface.blit(highscore, (highscore_x, y_pos))
    #     y_pos += highscore.get_height()
    #     # underline
    #     pygame.draw.line(
    #         self.game.display_surface,
    #         WHITE,
    #         (highscore_x, y_pos),
    #         (highscore_x + highscore_width, y_pos),
    #         2,
    #     )
    #     y_pos += 20

    #     x_pos_text = WIDTH / 2 - self.title_width / 2 + 100
    #     x_pos_score = WIDTH / 2 + self.title_width / 2 - 125

    #     # Text size here is 22

    #     if len(conf.highscores):
    #         for name_text, score_text in conf.highscores:

    #             name = lib.render_text(name_text, 22)
    #             self.game.display_surface.blit(name, (x_pos_text, y_pos))

    #             score = lib.render_text(str(score_text), 22)
    #             self.game.display_surface.blit(score, (x_pos_score, y_pos))

    #             y_pos += name.get_height() + 3
    #     else:
    #         y_pos += 25
    #         self.__render_lines(self.NOSCORES, 22, 0, y_pos)

    def __render_lines(self, lines, size, spacing, y_pos):

        text = []
        longest = 0
        height = 0

        for line in lines.splitlines():
            if line:
                rendered_text = lib.render_text(line, size)
                width = rendered_text.get_width()
                text.append(rendered_text)
                if not height:
                    height = rendered_text.get_height()
                if width > longest:
                    longest = width
            else:
                text.append(False)

        x_pos = WIDTH / 2 - longest / 2

        for line in text:
            if line:
                self.game.display_surface.blit(line, (x_pos, y_pos))
            y_pos += height + spacing

    def _help(self, y_pos):
        self.__render_lines(self.HELP_TEXT, 18, 2, y_pos)

    def _exit(self, y_pos):
        choice, self._choice = self._choice, self._last_choice
        self._main(y_pos)
        self._choice = choice

        y_pos = HEIGHT / 2 - 75

        box_white = pygame.Rect(WIDTH / 2 - 125, y_pos, 250, 150)
        box_black = box_white.inflate(-5, -5)
        pygame.draw.rect(self.game.display_surface, WHITE, box_white)
        pygame.draw.rect(self.game.display_surface, BACKGROUND, box_black)

        y_pos += 10

        sure = lib.render_text(self.EXIT_SURE, 24)
        self.game.display_surface.blit(sure, (WIDTH / 2 - sure.get_width() / 2, y_pos))

        y_pos += sure.get_height() + 7

        if self.EXIT_OPTIONS[self._choice] == self.YES:
            yes_colour, no_colour = self.SELECTED_COLOUR, WHITE
        else:
            yes_colour, no_colour = WHITE, self.SELECTED_COLOUR

        yes = lib.render_text(self.YES, 38, yes_colour)
        no = lib.render_text(self.NO, 38, no_colour)

        self.game.display_surface.blit(yes, (WIDTH / 2 - yes.get_width() / 2, y_pos))
        y_pos += yes.get_height()
        self.game.display_surface.blit(no, (WIDTH / 2 - no.get_width() / 2, y_pos))

    def _exit_action(self):

        if self.EXIT_OPTIONS[self._choice] == self.YES:
            raise SystemExit
        else:
            self._return_to_menu()
