#!/usr/bin/env python

import math
from typing import Optional

import pygame
from enum import Enum, auto
from MooToo.config import Config
from MooToo.galaxy import Galaxy, get_distance
from MooToo.system import System
from MooToo.planet import Planet
from MooToo.constants import PlanetSize, PlanetCategory, PopulationJobs, PlanetClimate
from MooToo.gui_button import Button
from MooToo.lbx_image import LBXImage


#####################################################################################################
class DisplayMode(Enum):
    GALAXY = auto()
    SYSTEM = auto()
    PLANET = auto()


#####################################################################################################
IMAGE_CACHE: dict[tuple[str, int], pygame.Surface] = {}


#####################################################################################################
class Game:
    def __init__(self, galaxy: Galaxy, config: Config):
        self.galaxy = galaxy
        self.config = config
        pygame.init()
        self.label_font = pygame.font.SysFont("Ariel", 14)
        self.text_font = pygame.font.SysFont("Ariel", 18)
        self.title_font = pygame.font.SysFont("Ariel", 24)
        self.screen = pygame.display.set_mode((640, 480), flags=pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.display_mode = DisplayMode.GALAXY
        self.system = None  # System we are looking at
        self.planet = None  # Planet we are looking at
        self.images = self.load_images()
        self.size = self.screen.get_size()
        self.mid_point = (self.size[0] / 2, self.size[1] / 2)
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

        images["big_blue_star"] = self.load_image("BUFFER0.LBX", 83)
        images["big_white_star"] = self.load_image("BUFFER0.LBX", 154)
        images["big_yellow_star"] = self.load_image("BUFFER0.LBX", 160)
        images["big_orange_star"] = self.load_image("BUFFER0.LBX", 166)
        images["big_red_star"] = self.load_image("BUFFER0.LBX", 172)
        images["big_brown_star"] = self.load_image("BUFFER0.LBX", 178)

        images["gas_giant"] = self.load_image("BUFFER0.LBX", 142)

        index = 92
        for climate in [
            PlanetClimate.TOXIC,
            PlanetClimate.SWAMP,
            PlanetClimate.OCEAN,
            PlanetClimate.RADIATED,
            PlanetClimate.BARREN,
            PlanetClimate.DESERT,
            PlanetClimate.TOXIC,
            PlanetClimate.TUNDRA,
            PlanetClimate.TERRAN,
            PlanetClimate.GAIA,
        ]:
            for size in [PlanetSize.TINY, PlanetSize.SMALL, PlanetSize.MEDIUM, PlanetSize.LARGE, PlanetSize.HUGE]:
                images[f"planet_{climate.name}_{size.name}"] = self.load_image("BUFFER0.LBX", index)
                index += 1

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
            sys_coords = self.get_planet_position(planet)
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
                self.draw_system_view()
            case DisplayMode.PLANET:
                self.draw_planet_view()

    #####################################################################################################
    def draw_title(self, text: str) -> None:
        title_surface = self.title_font.render(text, True, "red")
        self.screen.blit(title_surface, (5, 5))

    #####################################################################################################
    def draw_system_view(self):
        """Draw a solar system"""
        system = self.system
        self.draw_title(system.name)
        # Draw Sun
        star_image = self.images[f"big_{system.draw_colour}_star"]
        img_size = star_image.get_size()
        img_coord = (self.mid_point[0] - img_size[0] / 2, self.mid_point[1] - img_size[1] / 2)
        self.screen.blit(star_image, img_coord)

        for orbit, planet in self.system.orbits.items():
            if planet is None:
                continue
            self.draw_planet_in_orbit(planet)

    #####################################################################################################
    def draw_planet_in_orbit(self, planet: Planet):
        radius = self.orbit_radius(planet.orbit)
        # Draw the orbit
        pygame.draw.circle(self.screen, self.system.draw_colour, self.mid_point, radius, width=1)
        position = self.get_planet_position(planet)
        match planet.category:
            case PlanetCategory.GAS_GIANT:
                self.draw_gas_giant(planet, position)
            case PlanetCategory.PLANET:
                self.draw_planet(planet, position)
            case PlanetCategory.ASTEROID:
                self.draw_asteroid(planet, position)

    #####################################################################################################
    def orbit_radius(self, orbit: int) -> int:
        return 40 * orbit + 50

    #####################################################################################################
    def get_planet_position(self, planet: Planet):
        """Return the planets position and radius"""
        radius = self.orbit_radius(planet.orbit)
        position = (
            radius * math.cos(planet.arc) + self.mid_point[0],
            radius * math.sin(planet.arc) + self.mid_point[1],
        )
        return position

    #####################################################################################################
    def draw_gas_giant(self, planet: Planet, position: tuple[float, float]) -> None:
        """Draw a gas giant"""
        image = self.images["gas_giant"]
        self.draw_label_planet(image, position, planet.name)

    #####################################################################################################
    def draw_planet(self, planet: Planet, position: tuple[float, float]) -> None:
        """Draw a specific planet"""
        image = self.images[f"planet_{planet.climate.name}_{planet.size.name}"]
        self.draw_label_planet(image, position, planet.name)

    #####################################################################################################
    def draw_label_planet(self, image: pygame.surface.Surface, position: tuple[float, float], name: str) -> None:
        """Draw a specific planet"""
        image_size = image.get_size()
        image_position = (position[0] - image_size[0] / 2, position[1] - image_size[1] / 2)
        self.screen.blit(image, image_position)
        # Label the planet
        text_surface = self.label_font.render(name, True, "white")
        text_size = text_surface.get_size()
        text_coord = (
            image_position[0] + image_size[0] / 2 - text_size[0] / 2,
            image_position[1] + image_size[1] - text_size[1] / 2,
        )
        self.screen.blit(text_surface, text_coord)

    #####################################################################################################
    def draw_asteroid(self, planet: Planet, position: tuple[float, float]) -> None:
        return
        """Draw an asteroid belt"""
        image_size = self.images["asteroid"].get_size()
        image_position = (position[0] - image_size[0] / 2, position[1] - image_size[1] / 2)
        self.screen.blit(self.images["asteroid"], image_position)
        # Label the planet
        text_surface = self.label_font.render(planet.name, True, "white")
        text_size = text_surface.get_size()
        text_coord = (
            image_position[0] + image_size[0] / 2 - text_size[0] / 2,
            image_position[1] + image_size[1] - text_size[1] / 2,
        )
        self.screen.blit(text_surface, text_coord)

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
    def load_image(self, lbx_file: str, lbx_index: int) -> pygame.Surface:
        img_key = (lbx_file, lbx_index)
        if img_key not in IMAGE_CACHE:
            pil_image = LBXImage(lbx_file, lbx_index, self.config["moo_path"]).png_image()
            IMAGE_CACHE[img_key] = pygame.image.load(pil_image, "foo.png")
        return IMAGE_CACHE[img_key]

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
