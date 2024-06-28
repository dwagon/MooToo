""" Planet Summary Window"""

import time
from typing import TYPE_CHECKING, Any
from enum import StrEnum, auto
import pygame

from MooToo.ui.base_graphics import BaseGraphics
from MooToo.ui.gui_button import Button


if TYPE_CHECKING:
    from MooToo.ui.game import Game
    from MooToo.empire import Empire


#####################################################################################################
class SummaryColumns(StrEnum):
    NAME = auto()
    CLIMATE = auto()
    GRAVITY = auto()
    MINERALS = auto()
    SIZE = auto()


#####################################################################################################
class SummaryButtons(StrEnum):
    RETURN = auto()
    CLIMATE = auto()
    MINERALS = auto()
    SIZE = auto()
    NO_ENEMY = auto()
    GRAVITY = auto()
    HOSTILE = auto()
    ABUNDANCE = auto()
    IN_RANGE = auto()
    SEND_COLONY = auto()
    SEND_OUTPOST = auto()
    UP = auto()
    DOWN = auto()


#####################################################################################################
#####################################################################################################
class PlanetSummaryWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game", empire: "Empire"):
        super().__init__(game)
        self.screen = screen
        self.empire = empire
        self.data = []
        self.images = self.load_images()
        self.sorting = SummaryColumns.NAME
        self.buttons = {
            SummaryButtons.CLIMATE: Button(self.images["climate_button"], pygame.Vector2(441, 201)),
            SummaryButtons.RETURN: Button(self.images["return_button"], pygame.Vector2(454, 440)),
            SummaryButtons.MINERALS: Button(self.images["minerals_button"], pygame.Vector2(502, 201)),
            SummaryButtons.SIZE: Button(self.images["size_button"], pygame.Vector2(567, 201)),
            SummaryButtons.NO_ENEMY: Button(
                self.images["no_enemy_button"],
                pygame.Vector2(440, 266),
            ),
            SummaryButtons.GRAVITY: Button(
                self.images["normal_gravity_button"],
                pygame.Vector2(440, 289),
            ),
            SummaryButtons.HOSTILE: Button(
                self.images["non_hostile_button"],
                pygame.Vector2(440, 311),
            ),
            SummaryButtons.ABUNDANCE: Button(
                self.images["abundance_button"],
                pygame.Vector2(440, 335),
            ),
            SummaryButtons.IN_RANGE: Button(
                self.images["in_range_button"],
                pygame.Vector2(440, 358),
            ),
            SummaryButtons.SEND_COLONY: Button(self.images["send_colony_button"], pygame.Vector2(454, 385)),
            SummaryButtons.SEND_OUTPOST: Button(
                self.images["send_outpost_button"],
                pygame.Vector2(454, 413),
            ),
            SummaryButtons.UP: Button(self.images["up_button"], pygame.Vector2(420, 15)),
            SummaryButtons.DOWN: Button(self.images["down_button"], pygame.Vector2(420, 448)),
        }

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        start = time.time()
        images["window"] = self.load_image("PLNTSUM.LBX", 0, palette_index=7)
        images["climate_button"] = self.load_image("PLNTSUM.LBX", 1, palette_index=7)
        images["minerals_button"] = self.load_image("PLNTSUM.LBX", 2, palette_index=7)
        images["size_button"] = self.load_image("PLNTSUM.LBX", 3, palette_index=7)
        images["no_enemy_button"] = self.load_image("PLNTSUM.LBX", 4, palette_index=7)
        images["normal_gravity_button"] = self.load_image("PLNTSUM.LBX", 5, palette_index=7)
        images["non_hostile_button"] = self.load_image("PLNTSUM.LBX", 6, palette_index=7)
        images["abundance_button"] = self.load_image("PLNTSUM.LBX", 7, palette_index=7)
        images["in_range_button"] = self.load_image("PLNTSUM.LBX", 8, palette_index=7)
        images["send_colony_button"] = self.load_image("PLNTSUM.LBX", 9, palette_index=7)
        images["send_outpost_button"] = self.load_image("PLNTSUM.LBX", 10, palette_index=7)
        images["up_button"] = self.load_image("PLNTSUM.LBX", 11, palette_index=7)
        images["down_button"] = self.load_image("PLNTSUM.LBX", 12, palette_index=7)
        images["return_button"] = self.load_image("PLNTSUM.LBX", 14, palette_index=7)

        end = time.time()
        print(f"PlanetSummary: Loaded {len(images)} in {end-start} seconds")
        return images

    #####################################################################################################
    def draw(self):
        """Draw the window"""
        self.screen.blit(self.images["window"], pygame.Vector2(0, 0))
        for button in self.buttons.values():
            button.draw(self.screen)
        top_left = pygame.Vector2(20, 37)
        self.data.sort(key=lambda x: x[self.sorting])

        for planet_data in self.data:
            self.draw_planet(planet_data, top_left)
            top_left += pygame.Vector2(0, 55)

    #####################################################################################################
    def draw_planet(self, planet_data: dict[str, Any], top_left: pygame.Vector2):
        tl = top_left.copy()
        self.draw_text(planet_data[SummaryColumns.NAME], tl)
        tl += pygame.Vector2(91, 0)
        self.draw_text(planet_data[SummaryColumns.CLIMATE], tl)
        tl += pygame.Vector2(75, 0)
        self.draw_text(planet_data[SummaryColumns.GRAVITY], tl)
        tl += pygame.Vector2(90, 0)
        self.draw_text(planet_data[SummaryColumns.MINERALS], tl)
        tl += pygame.Vector2(90, 0)
        self.draw_text(planet_data[SummaryColumns.SIZE], tl)

    #####################################################################################################
    def draw_text(self, text: str, top_left: pygame.Vector2) -> None:
        text_surface = self.text_font.render(text, True, "white", "black")
        self.screen.blit(text_surface, top_left)

    #####################################################################################################
    def collect_data(self) -> list[dict[SummaryColumns, Any]]:
        """Gather all the information required"""
        data = []
        for system in self.empire.known_systems:
            for planet in self.game.galaxy.systems[system].orbits:
                if not planet:
                    continue
                planet_data = {
                    SummaryColumns.NAME: planet.name,
                    SummaryColumns.CLIMATE: planet.climate,
                    SummaryColumns.GRAVITY: planet.gravity,
                    SummaryColumns.MINERALS: planet.richness,
                    SummaryColumns.SIZE: planet.size,
                }
                data.append(planet_data)
        return data

    #####################################################################################################
    def loop(self) -> None:
        self.data = self.collect_data()
        while True:
            self.screen.fill("black")
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    if buttons[0]:
                        if self.buttons[SummaryButtons.RETURN].clicked():
                            return
                        self.button_left_down()
                    elif buttons[2]:
                        return

            pygame.display.flip()

            self.clock.tick(60)

    #####################################################################################################
    def button_left_down(self):
        if self.buttons[SummaryButtons.SIZE].clicked():
            self.sorting = SummaryColumns.SIZE
        elif self.buttons[SummaryButtons.GRAVITY].clicked():
            self.sorting = SummaryColumns.GRAVITY
        elif self.buttons[SummaryButtons.CLIMATE].clicked():
            self.sorting = SummaryColumns.CLIMATE
        elif self.buttons[SummaryButtons.MINERALS].clicked():
            self.sorting = SummaryColumns.MINERALS


# EOF
