""" Stuff relating to drawing the orbit window"""

import math
import time
from typing import Optional

import pygame
from MooToo.planet import Planet
from MooToo.base_graphics import BaseGraphics
from MooToo.system import System
from MooToo.galaxy import get_distance
from MooToo.gui_button import Button
from MooToo.config import Config
from MooToo.constants import PlanetCategory, PlanetClimate, PlanetSize


#####################################################################################################
class OrbitWindow(BaseGraphics):
    #####################################################################################################
    def __init__(self, screen: pygame.Surface, config: Config):
        super().__init__(config)
        self.screen = screen
        self.planet = None  # Which planet we are looking at
        self.system = None  # Which system we are looking at
        self.window: Optional[pygame.Rect] = None  # The window Rect
        self.images = self.load_images()
        self.close_button = Button(self.load_image("BUFFER0.LBX", 82), self.mid_point + pygame.Vector2(90, 100))

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        start = time.time()
        images = {}
        images["orbit_window"] = self.load_image("BUFFER0.LBX", 73)
        images["gas_giant"] = self.load_image("BUFFER0.LBX", 142)

        images["big_blue_star"] = self.load_image("BUFFER0.LBX", 83)
        images["big_white_star"] = self.load_image("BUFFER0.LBX", 154)
        images["big_yellow_star"] = self.load_image("BUFFER0.LBX", 160)
        images["big_orange_star"] = self.load_image("BUFFER0.LBX", 166)
        images["big_red_star"] = self.load_image("BUFFER0.LBX", 172)
        images["big_brown_star"] = self.load_image("BUFFER0.LBX", 178)

        index = 92
        for climate in [
            PlanetClimate.TOXIC,
            PlanetClimate.SWAMP,
            PlanetClimate.OCEAN,
            PlanetClimate.RADIATED,
            PlanetClimate.BARREN,
            PlanetClimate.DESERT,
            PlanetClimate.TUNDRA,
            PlanetClimate.ARID,
            PlanetClimate.TERRAN,
            PlanetClimate.GAIA,
        ]:
            for size in [PlanetSize.TINY, PlanetSize.SMALL, PlanetSize.MEDIUM, PlanetSize.LARGE, PlanetSize.HUGE]:
                images[f"planet_{climate.name}_{size.name}"] = self.load_image("BUFFER0.LBX", index, frame=0)
                index += 1

        index = 77
        for orbit in range(5):
            images[f"asteroid_{orbit}"] = self.load_image("BUFFER0.LBX", 91, frame=orbit)
            images[f"orbit_{orbit}"] = self.load_image("BUFFER0.LBX", index)
            index += 1
        end = time.time()
        print(f"Orbit: Loaded {len(images)} in {end-start} seconds")

        return images

    #####################################################################################################
    def draw_planet_details(self, window: pygame.Surface, planet: Planet):
        """Describe details of planet in text format"""
        text_list = (
            planet.name,
            f"{planet.size}, {planet.climate}",
            f"Max Pop: {int(planet.max_population()/1e6)}",
            f"{planet.richness}",
        )
        if planet.category == PlanetCategory.GAS_GIANT:
            text_list = (planet.name, "Gas Giant (uninhabitable)")
        top_left = self.window.topleft + pygame.Vector2(15, 50)
        for text in text_list:
            text_surface = self.label_font.render(text, True, "white")
            self.screen.blit(text_surface, top_left)
            top_left[1] += text_surface.get_size()[1] + 2

    #####################################################################################################
    def mouse_pos(self):
        """ """
        pos = pygame.mouse.get_pos()
        if self.window is None or not self.window.collidepoint(pos):
            return
        if planet := self.pick_planet(pos):
            self.planet = planet

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.close_button.clicked():
            self.system = None
            self.planet = None
            return True
        return False

    #####################################################################################################
    def get_planet_position(self, arc: float, orbit: int) -> pygame.Vector2:
        x = (91 / 2 + orbit * 47 / 2) * math.cos(math.radians(arc))
        y = (46 / 2 + orbit * 27 / 2) * math.sin(math.radians(arc))
        return pygame.Vector2(x, y)

    #####################################################################################################
    def pick_planet(self, coords: tuple[int, int]) -> Optional[Planet]:
        """Return which planet the mouse coords are close to"""
        for orbit, planet in self.system.orbits.items():
            if not planet:
                continue
            sys_coords = self.get_planet_position(planet.arc, planet.orbit)
            adjusted_coords = sys_coords + self.mid_point
            distance = get_distance(adjusted_coords[0], adjusted_coords[1], coords[0], coords[1])
            if distance < 20:
                return planet
        return None

    #####################################################################################################
    def draw_centered_image(self, image: pygame.Surface) -> pygame.Rect:
        tl = self.top_left(image, self.mid_point)
        return self.screen.blit(image, tl)

    #####################################################################################################
    def draw_asteroid(self, planet: Planet) -> None:
        """Draw an asteroid belt"""
        image = self.images[f"asteroid_{planet.orbit}"]
        self.draw_centered_image(image)

    #####################################################################################################
    def draw(self, system: System) -> None:
        """Draw a solar system"""
        image = self.images["orbit_window"]
        self.window = self.draw_centered_image(image)
        self.system = system

        # Draw Sun
        star_image = self.images[f"big_{system.draw_colour}_star"]
        self.draw_centered_image(star_image)

        # Draw orbits first so they are behind everything else
        for orbit, planet in system.orbits.items():
            if planet is None:
                continue
            orbit_image = self.images[f"orbit_{planet.orbit}"]
            self.draw_centered_image(orbit_image)

        for orbit, planet in system.orbits.items():
            if planet is None:
                continue
            self.draw_planet_in_orbit(planet)
        if self.planet:
            self.draw_planet_details(self.window, self.planet)
        self.close_button.draw(self.screen)

    #####################################################################################################
    def draw_planet_in_orbit(self, planet: Planet) -> None:
        position = self.get_planet_position(planet.arc, planet.orbit)
        match planet.category:
            case PlanetCategory.GAS_GIANT:
                self.draw_gas_giant(planet, position)
            case PlanetCategory.PLANET:
                self.draw_planet(planet, position)
            case PlanetCategory.ASTEROID:
                self.draw_asteroid(planet)

    #####################################################################################################
    def draw_gas_giant(self, planet: Planet, position: pygame.Vector2) -> None:
        """Draw a gas giant"""
        image = self.images["gas_giant"]
        image_position = self.top_left(image, position) + self.mid_point
        self.screen.blit(image, image_position)

    #####################################################################################################
    def draw_planet(self, planet: Planet, position: pygame.Vector2) -> None:
        """Draw a specific planet"""
        image = self.images[f"planet_{planet.climate.name}_{planet.size.name}"]
        image_position = self.top_left(image, position) + self.mid_point
        self.screen.blit(image, image_position)
