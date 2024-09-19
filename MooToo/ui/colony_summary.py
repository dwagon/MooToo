""" Colony Summary Window"""

import time
from enum import StrEnum, auto
from typing import TYPE_CHECKING, Optional
import pygame

from MooToo.constants import PopulationJobs
from .constants import DisplayMode
from .base_graphics import BaseGraphics, load_image
from .gui_button import Button
from ..utils import PlanetId

if TYPE_CHECKING:
    from .game import Game


#####################################################################################################
class ImageNames(StrEnum):
    WINDOW = auto()
    RETURN_BUTTON = auto()
    PURCHASE_BUTTON = auto()
    FARMER = auto()
    WORKER = auto()
    SCIENTIST = auto()


#####################################################################################################
#####################################################################################################
class ColonySummaryWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.images: dict[ImageNames, pygame.Surface] = load_images()
        self.return_button = Button(self.images[ImageNames.RETURN_BUTTON], pygame.Vector2(530, 445))
        self.buy_now_rects: dict[PlanetId, pygame.Rect] = {}
        self.building_rect: dict[PlanetId, pygame.Rect] = {}
        self.planet_rect: dict[PlanetId, pygame.Rect] = {}
        self.population_rects: dict[tuple[PlanetId, PopulationJobs], list[pygame.Rect]] = {}
        self.destination_rects: dict[tuple[PlanetId, PopulationJobs], pygame.Rect] = {}
        self.pop_selected: Optional[tuple[PlanetId, PopulationJobs, int]] = None

    #####################################################################################################
    def draw(self):
        """Draw the window"""
        self.screen.blit(self.images[ImageNames.WINDOW], pygame.Vector2(0, 0))
        self.return_button.draw(self.screen)
        self.buy_now_rects = {}
        self.building_rect = {}
        self.population_rects = {}
        self.destination_rects = {}
        top_left = pygame.Vector2(10, 37)
        empire = self.game.galaxy.empires[self.game.empire_id]
        for planet_id in empire.owned_planets:
            self.draw_planet(planet_id, top_left)
            top_left += pygame.Vector2(0, 31)

    #####################################################################################################
    def draw_planet(self, planet_id: PlanetId, top_left: pygame.Vector2) -> None:
        planet = self.game.galaxy.planets[planet_id]
        name_surface = self.text_font.render(planet.name, True, "white")
        planet_name_rect = pygame.Rect(top_left.x, top_left.y, 86, 27)
        pygame.draw.rect(self.screen, "purple", planet_name_rect, width=1)
        self.planet_rect[planet_id] = planet_name_rect
        self.screen.blit(name_surface, top_left)
        self.destination_rects[(planet_id, PopulationJobs.FARMERS)] = pygame.Rect(100, top_left[1], 133, 28)
        self.destination_rects[(planet_id, PopulationJobs.WORKERS)] = pygame.Rect(235, top_left[1], 133, 28)
        self.destination_rects[(planet_id, PopulationJobs.SCIENTISTS)] = pygame.Rect(375, top_left[1], 133, 28)

        pygame.draw.rect(self.screen, "purple", self.destination_rects[planet_id, PopulationJobs.FARMERS], width=1)
        pygame.draw.rect(self.screen, "purple", self.destination_rects[planet_id, PopulationJobs.WORKERS], width=1)
        pygame.draw.rect(self.screen, "purple", self.destination_rects[planet_id, PopulationJobs.SCIENTISTS], width=1)

        self.population_rects[(planet_id, PopulationJobs.FARMERS)] = self.draw_population_sequence(
            top_left + pygame.Vector2(90, 0), self.images[ImageNames.FARMER], planet.jobs[PopulationJobs.FARMERS], 130
        )
        self.population_rects[(planet_id, PopulationJobs.WORKERS)] = self.draw_population_sequence(
            top_left + pygame.Vector2(225, 0), self.images[ImageNames.WORKER], planet.jobs[PopulationJobs.WORKERS], 130
        )
        self.population_rects[(planet_id, PopulationJobs.SCIENTISTS)] = self.draw_population_sequence(
            top_left + pygame.Vector2(370, 0),
            self.images[ImageNames.SCIENTIST],
            planet.jobs[PopulationJobs.SCIENTISTS],
            130,
        )
        self.building_rect[planet_id] = pygame.Rect(512, top_left.y, 87, 25)
        pygame.draw.rect(self.screen, "purple", self.building_rect[planet_id], width=1)
        if planet.build_queue:
            self.draw_building(planet_id, top_left)
            if planet.buy_cost() < planet.owner.money:
                rect = self.screen.blit(self.images[ImageNames.PURCHASE_BUTTON], top_left + pygame.Vector2(590, 0))
                self.buy_now_rects[planet] = rect
                pygame.draw.rect(self.screen, "purple", self.buy_now_rects[planet], width=1)

    #####################################################################################################
    def draw_building(self, planet_id: PlanetId, top_left: pygame.Vector2) -> None:
        planet = self.game.galaxy.planets[planet_id]
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
        for planet_id, rect in self.building_rect.items():
            if rect.collidepoint(mouse[0], mouse[1]):
                self.game.look_at_planet(planet_id)
                self.display_mode = DisplayMode.PLANET_BUILD
                return

        # Look at the planet
        for planet_id, rect in self.planet_rect.items():
            if rect.collidepoint(mouse[0], mouse[1]):
                self.game.look_at_planet(planet_id)
                self.display_mode = DisplayMode.PLANET
                return

        if self.pop_selected:  # Select destination population
            for details, rect in self.destination_rects.items():
                planet_id, job = details
                if rect.collidepoint(mouse[0], mouse[1]):
                    self.move_population(planet_id, job)
                    self.pop_selected = {}
        else:  # Select population to move
            for key, rects in self.population_rects.items():
                planet_id, job = key
                for num, rect in enumerate(rects):
                    if rect.collidepoint(mouse[0], mouse[1]):
                        self.pop_selected = (planet_id, job, len(rects) - num)

    #####################################################################################################
    def move_population(self, dest_planet_id: PlanetId, dest_job: PopulationJobs) -> None:
        """Move population in {self.pop_selected} to new planet/job"""
        planet = self.game.galaxy.planets[dest_planet_id]
        planet_id, job, num = self.pop_selected
        if dest_planet_id == planet_id:
            planet.move_workers(num, job, dest_job)
            return
        empire = self.game.galaxy.empires[self.game.empire_id]
        empire.migrate(num, planet_id, job, dest_planet_id, dest_job)

    #####################################################################################################
    def mouse_pos(self, event: pygame.event):
        """If we are moving pops - change cursor"""
        if not self.pop_selected:
            return
        _, job, num = self.pop_selected
        match job:
            case PopulationJobs.FARMERS:
                image = self.images[ImageNames.FARMER]
            case PopulationJobs.WORKERS:
                image = self.images[ImageNames.WORKER]
            case PopulationJobs.SCIENTISTS:
                image = self.images[ImageNames.SCIENTIST]
            case _:
                image = None
        delta = 0
        mouse = pygame.mouse.get_pos()
        for _ in range(num):
            self.screen.blit(image, pygame.Vector2(mouse[0] + delta, mouse[1]))
            delta += image.get_size()[0]

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


#####################################################################################################
def load_images() -> dict[ImageNames, pygame.Surface]:
    images = {}
    start = time.time()
    images[ImageNames.WINDOW] = load_image("COLSUM.LBX", 0, palette_index=2)
    images[ImageNames.RETURN_BUTTON] = load_image("COLSUM.LBX", 1, palette_index=2)
    images[ImageNames.PURCHASE_BUTTON] = load_image("COLSUM.LBX", 11, palette_index=2)

    images[ImageNames.FARMER] = load_image("RACEICON.LBX", 0, palette_index=2)
    images[ImageNames.WORKER] = load_image("RACEICON.LBX", 3, palette_index=2)
    images[ImageNames.SCIENTIST] = load_image("RACEICON.LBX", 5, palette_index=2)
    end = time.time()
    print(f"Colonies: Loaded {len(images)} in {end-start} seconds")
    return images


# EOF
