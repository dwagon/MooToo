""" Colony Summary Window"""

import time
from typing import TYPE_CHECKING
import pygame

from MooToo.constants import PopulationJobs
from MooToo.ui.constants import DisplayMode
from MooToo.ui.base_graphics import BaseGraphics, load_image
from MooToo.ui.gui_button import Button


if TYPE_CHECKING:
    from MooToo.ui.game import Game
    from MooToo.planet import Planet


#####################################################################################################
#####################################################################################################
class ColonySummaryWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.images = self.load_images()
        self.return_button = Button(self.images["return_button"], pygame.Vector2(530, 445))
        self.buy_now_rects: dict[Planet, pygame.Rect] = {}
        self.building_rect: dict[Planet, pygame.Rect] = {}
        self.planet_rect: dict[Planet, pygame.Rect] = {}

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        start = time.time()
        images["window"] = load_image("COLSUM.LBX", 0, palette_index=2)
        images["return_button"] = load_image("COLSUM.LBX", 1, palette_index=2)
        images["purchase_button"] = load_image("COLSUM.LBX", 11, palette_index=2)

        images["farmer"] = load_image("RACEICON.LBX", 0, palette_index=2)
        images["worker"] = load_image("RACEICON.LBX", 3, palette_index=2)
        images["scientist"] = load_image("RACEICON.LBX", 5, palette_index=2)
        end = time.time()
        print(f"Colonies: Loaded {len(images)} in {end-start} seconds")
        return images

    #####################################################################################################
    def draw(self):
        """Draw the window"""
        self.screen.blit(self.images["window"], pygame.Vector2(0, 0))
        self.return_button.draw(self.screen)
        self.buy_now_rects = {}
        self.building_rect = {}
        top_left = pygame.Vector2(10, 37)
        for planet in self.game.empire.owned_planets:
            self.draw_planet(planet, top_left)
            top_left += pygame.Vector2(0, 31)

    #####################################################################################################
    def draw_planet(self, planet: "Planet", top_left: pygame.Vector2) -> None:
        name_surface = self.text_font.render(planet.name, True, "white")
        planet_name_rect = pygame.Rect(top_left.x, top_left.y, 86, 27)
        pygame.draw.rect(self.screen, "purple", planet_name_rect, width=1)
        self.planet_rect[planet] = planet_name_rect
        self.screen.blit(name_surface, top_left)
        self.draw_population_sequence(
            top_left + pygame.Vector2(90, 0), self.images["farmer"], planet.jobs[PopulationJobs.FARMERS], 130
        )
        self.draw_population_sequence(
            top_left + pygame.Vector2(225, 0), self.images["worker"], planet.jobs[PopulationJobs.WORKERS], 130
        )
        self.draw_population_sequence(
            top_left + pygame.Vector2(370, 0), self.images["scientist"], planet.jobs[PopulationJobs.SCIENTISTS], 130
        )
        self.building_rect[planet] = pygame.Rect(512, top_left.y, 87, 25)
        pygame.draw.rect(self.screen, "purple", self.building_rect[planet], width=1)  # DBG
        if planet.build_queue:
            self.draw_building(planet, top_left)
            if planet.buy_cost() < planet.owner.money:
                rect = self.screen.blit(self.images["purchase_button"], top_left + pygame.Vector2(590, 0))
                self.buy_now_rects[planet] = rect
                pygame.draw.rect(self.screen, "purple", self.buy_now_rects[planet], width=1)  # DBG

    #####################################################################################################
    def draw_building(self, planet: "Planet", top_left: pygame.Vector2) -> None:
        building = planet.build_queue[0]
        text_surface = self.label_font.render(building.name, True, "white")
        self.screen.blit(text_surface, top_left + pygame.Vector2(510, 0))
        if turns := planet.turns_to_build():
            text_surface = self.label_font.render(f"{turns:,} t", True, "white")
            self.screen.blit(text_surface, top_left + pygame.Vector2(510, 12))

    #####################################################################################################
    def button_left_down(self) -> None:
        """Return True if changing mode"""
        if self.return_button.clicked():
            self.display_mode = DisplayMode.GALAXY
            return
        mouse = pygame.mouse.get_pos()

        # Buy the construction on planet
        for planet, rect in self.buy_now_rects.items():
            if rect.collidepoint(mouse[0], mouse[1]):
                print(f"DBG Buy on {planet}")

        # Change construction on planet
        for planet, rect in self.building_rect.items():
            if rect.collidepoint(mouse[0], mouse[1]):
                self.game.look_at_planet(planet)
                self.display_mode = DisplayMode.PLANET_BUILD
                return

        # Look at the planet
        for planet, rect in self.planet_rect.items():
            if rect.collidepoint(mouse[0], mouse[1]):
                self.game.look_at_planet(planet)
                self.display_mode = DisplayMode.PLANET
                return

    #####################################################################################################
    def loop(self) -> DisplayMode:
        self.display_mode = DisplayMode.COLONY_SUM
        while True:
            self.event_loop()

            match self.display_mode:
                case DisplayMode.COLONY_SUM:
                    pass
                case _:
                    return self.display_mode
