""" Generic Text Box window"""

import time
from typing import TYPE_CHECKING
import pygame
from MooToo.ui.base_graphics import BaseGraphics
from MooToo.ui.gui_button import Button

if TYPE_CHECKING:
    from MooToo.ui.game import Game


#####################################################################################################
#####################################################################################################
class TextBoxWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        """ """
        super().__init__(game)
        self.screen = screen
        self.images = self.load_images()
        self.close_button = Button(self.images["close_button"], pygame.Vector2(285, 440))

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        start = time.time()
        images["top"] = self.load_image("TEXTBOX.LBX", 0)
        images["sides"] = self.load_image("TEXTBOX.LBX", 1)
        images["bottom"] = self.load_image("TEXTBOX.LBX", 2)
        images["close_button"] = self.load_image("TEXTBOX.LBX", 3)
        end = time.time()
        print(f"TextBox: Loaded {len(images)} in {end-start} seconds")

        return images

    #####################################################################################################
    def button_left_down(self):
        if self.close_button.clicked():
            return True
        return False

    #####################################################################################################
    def draw(self, text: list[str], font=None) -> None:
        top_left = self.draw_frame()
        if not font:
            font = self.text_font
        line_size = font.render("M", True, "purple").get_size()
        for line in text:
            text_surface = font.render(line, True, "white")
            self.screen.blit(text_surface, top_left)
            top_left.y += line_size[1]
        self.close_button.draw(self.screen)

    #####################################################################################################
    def draw_frame(self) -> pygame.Vector2:
        top_left = pygame.Vector2(640 / 2 - self.images["top"].get_size()[0] / 2, 10)
        pygame.draw.rect(
            self.screen,
            "black",
            pygame.Rect(
                top_left.x + 10,
                top_left.y,
                self.images["sides"].get_size()[0] - 20,  # Each side is 10px wide
                self.images["sides"].get_size()[1] + 55,  # Margin of top + bottom
            ),
        )
        text_top_left = top_left + pygame.Vector2(10, 10)
        self.screen.blit(self.images["top"], top_left)
        top_left += pygame.Vector2(0, self.images["top"].get_size()[1])
        self.screen.blit(self.images["sides"], top_left)
        top_left += pygame.Vector2(0, self.images["sides"].get_size()[1])
        self.screen.blit(self.images["bottom"], top_left)
        return text_top_left
