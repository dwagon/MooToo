#!/usr/bin/env python

from typing import Optional

import pygame
from enum import Enum, auto
from MooToo.config import Config
from MooToo.galaxy import Galaxy, get_distance
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.constants import PlanetCategory, PopulationJobs
from MooToo.gui_button import Button
from MooToo.orbit_window import OrbitWindow
from MooToo.base_graphics import BaseGraphics


#####################################################################################################
class DisplayMode(Enum):
    GALAXY = auto()
    SYSTEM = auto()
    PLANET = auto()


#####################################################################################################
class Game(BaseGraphics):
    def __init__(self, galaxy: Galaxy, config: Config):
        super().__init__(config)
        self.display_mode = DisplayMode.GALAXY
        self.galaxy = galaxy
        self.system = None  # System we are looking at
        self.planet = None  # Planet we are looking at
        self.orbit_window = OrbitWindow(self.screen, config)
        self.images = self.load_images()
        self.turn_button = Button(self.load_image("BUFFER0.LBX", 2), pygame.Vector2(540, 440))

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.surface.Surface]:
        """Load all the images from disk"""
        images = {}
        images["small_blue_star"] = self.load_image("BUFFER0.LBX", 149)
        images["small_white_star"] = self.load_image("BUFFER0.LBX", 155)
        images["small_yellow_star"] = self.load_image("BUFFER0.LBX", 161)
        images["small_orange_star"] = self.load_image("BUFFER0.LBX", 167)
        images["small_red_star"] = self.load_image("BUFFER0.LBX", 173)
        images["small_brown_star"] = self.load_image("BUFFER0.LBX", 179)
        return images

    #####################################################################################################
    def loop(self):
        running = True

        while running:
            self.screen.fill("black")
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    buttons = pygame.mouse.get_pressed()
                    if buttons[0]:
                        self.button_left_down()
                    elif buttons[2]:
                        self.button_right_down()

            # fill the screen with a color to wipe away anything from last frame
            self.draw_screen()
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    #####################################################################################################
    def button_right_down(self):
        """User has pressed the right button"""
        match self.display_mode:
            case DisplayMode.GALAXY:
                pass
            case DisplayMode.SYSTEM:
                self.display_mode = DisplayMode.GALAXY
            case DisplayMode.PLANET:
                self.display_mode = DisplayMode.SYSTEM

    #####################################################################################################
    def button_left_down(self):
        mouse = pygame.mouse.get_pos()
        match self.display_mode:
            case DisplayMode.GALAXY:
                if system := self.pick_system(mouse):
                    self.display_mode = DisplayMode.SYSTEM
                    self.system = system
                if self.turn_button.clicked():
                    self.galaxy.turn()
            case DisplayMode.SYSTEM:
                if planet := self.pick_planet(mouse):
                    self.display_mode = DisplayMode.PLANET
                    self.planet = planet
            case DisplayMode.PLANET:
                pass

    #####################################################################################################
    def pick_system(self, coords: tuple[int, int]) -> Optional[System]:
        """Return which system the mouse coords are close to"""
        for sys_coord, system in self.galaxy.systems.items():
            distance = get_distance(sys_coord[0], sys_coord[1], coords[0], coords[1])
            if distance < 20:
                return system
        return None

    #####################################################################################################
    def pick_planet(self, coords: tuple[int, int]) -> Optional[Planet]:
        """Return which planet the mouse coords are close to"""
        for orbit, planet in self.system.orbits.items():
            if not planet:
                continue
            sys_coords = self.get_planet_position(planet.arc, planet.orbit)
            distance = get_distance(sys_coords[0], sys_coords[1], coords[0], coords[1])
            if distance < 20:
                return planet
        return None

    #####################################################################################################
    def draw_screen(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.draw_galaxy_view()
            case DisplayMode.SYSTEM:
                self.draw_galaxy_view()
                self.orbit_window.draw(self.system)
            case DisplayMode.PLANET:
                self.draw_planet_view()

    #####################################################################################################
    def draw_title(self, text: str) -> None:
        title_surface = self.title_font.render(text, True, "red")
        self.screen.blit(title_surface, (5, 5))

    #####################################################################################################
    def draw_planet_view(self) -> None:
        self.draw_title(self.planet.name)
        if self.planet.category != PlanetCategory.PLANET:
            return

        self.draw_text("Population:", 1, 1)
        self.draw_text(f"Current: {self.planet.current_population()} / Max: {self.planet.max_population()}", 2, 1)
        self.draw_text(
            f"Farmers: {self.planet.population[PopulationJobs.FARMER]} Food={self.planet.food_production()}-{self.planet.food_consumption()}={self.planet.food_production()-self.planet.food_consumption()}",
            3,
            1,
        )
        self.draw_text(
            f"Workers: {self.planet.population[PopulationJobs.WORKERS]} Producing={self.planet.work_production()}",
            4,
            1,
        )
        self.draw_text(
            f"Scientists: {self.planet.population[PopulationJobs.SCIENTISTS]} Science={self.planet.science_production()}",
            5,
            1,
        )

        self.draw_text("Buildings:", 7, 1)
        down = 8
        for building in self.planet.buildings:
            self.draw_text(building, down, 1)
            down += 1
        if self.planet.under_construction:
            self.draw_text(
                f"Under Construction: {self.planet.under_construction} {self.planet.construction_cost}/{self.planet.under_construction.cost}",
                down,
                1,
            )

        self.draw_text(f"Size: {self.planet.size}", 1, 3)
        self.draw_text(f"Gravity: {self.planet.gravity}", 2, 3)
        self.draw_text(f"Richness: {self.planet.richness}", 3, 3)
        self.draw_text(f"Climate: {self.planet.climate}", 4, 3)

    #####################################################################################################
    def draw_text(self, text: str, row: int, col: int) -> None:
        title_surface = self.text_font.render(text, True, "white")
        self.screen.blit(title_surface, (col * 150, row * 20))

    #####################################################################################################
    def draw_galaxy_view(self):
        image = self.load_image("BUFFER0.LBX", 0)
        self.screen.blit(image, (0, 0))
        for sys_coord, system in self.galaxy.systems.items():
            self.draw_galaxy_view_system(sys_coord, system)
        self.turn_button.draw(self.screen)

    #####################################################################################################
    def draw_galaxy_view_system(self, sys_coord, system):
        star_image = self.images[f"small_{system.draw_colour}_star"]

        text_surface = self.label_font.render(system.name, True, "red")
        text_size = text_surface.get_size()

        img_size = star_image.get_size()
        img_coord = (sys_coord[0] - img_size[0] / 2, sys_coord[1] - img_size[1] / 2)
        self.screen.blit(star_image, img_coord)
        text_coord = (sys_coord[0] - text_size[0] / 2, sys_coord[1] + img_size[1] / 2)

        self.screen.blit(text_surface, text_coord)


#####################################################################################################
def main():
    config = Config("config.json")
    galaxy = Galaxy(config)
    galaxy.populate()

    g = Game(galaxy, config)
    g.loop()
    pygame.quit()


#####################################################################################################
if __name__ == "__main__":
    main()

# EOF
