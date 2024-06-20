""" Colony Summary Window"""

import time
from typing import TYPE_CHECKING
import pygame

from MooToo.constants import PopulationJobs
from MooToo.ui.base_graphics import BaseGraphics
from MooToo.ui.gui_button import Button


if TYPE_CHECKING:
    from MooToo.ui.game import Game
    from MooToo.planet import Planet


#####################################################################################################
#####################################################################################################
class ColonyWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.images = self.load_images()
        self.return_button = Button(self.images["return_button"], pygame.Vector2(530, 445))

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        start = time.time()
        images["window"] = self.load_image("COLSUM.LBX", 0, palette_index=2)
        images["return_button"] = self.load_image("COLSUM.LBX", 1, palette_index=2)
        images["farmer"] = self.load_image("RACEICON.LBX", 0, palette_index=2)
        images["worker"] = self.load_image("RACEICON.LBX", 3, palette_index=2)
        images["scientist"] = self.load_image("RACEICON.LBX", 5, palette_index=2)
        end = time.time()
        print(f"Colonies: Loaded {len(images)} in {end-start} seconds")
        return images

    #####################################################################################################
    def draw(self):
        """Draw the window"""
        self.screen.blit(self.images["window"], pygame.Vector2(0, 0))
        self.return_button.draw(self.screen)
        top_left = pygame.Vector2(10, 40)
        for planet in self.game.empire.owned_planets:
            self.draw_planet(planet, top_left)
            top_left += pygame.Vector2(0, 32)

    #####################################################################################################
    def draw_planet(self, planet: "Planet", top_left: pygame.Vector2) -> None:
        name_surface = self.text_font.render(planet.name, True, "white")
        self.screen.blit(name_surface, top_left)
        self.draw_population_sequence(
            top_left + pygame.Vector2(100, 0),
            self.images["farmer"],
            planet.jobs[PopulationJobs.FARMER],
        )
        self.draw_population_sequence(
            top_left + pygame.Vector2(230, 0),
            self.images["worker"],
            planet.jobs[PopulationJobs.WORKERS],
        )
        self.draw_population_sequence(
            top_left + pygame.Vector2(370, 0),
            self.images["scientist"],
            planet.jobs[PopulationJobs.SCIENTISTS],
        )
        if planet.build_queue:
            self.draw_building(planet, top_left)

    #####################################################################################################
    def draw_building(self, planet: "Planet", top_left: pygame.Vector2) -> None:
        building = planet.build_queue[0]
        text_surface = self.label_font.render(building.name, True, "white")
        self.screen.blit(text_surface, top_left + pygame.Vector2(510, 0))
        if turns := planet.turns_to_build():
            text_surface = self.label_font.render(f"{turns} t", True, "white")
            self.screen.blit(text_surface, top_left + pygame.Vector2(510, 12))

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.return_button.clicked():
            return True
        return False
