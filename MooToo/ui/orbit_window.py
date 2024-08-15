""" Stuff relating to drawing the orbit window"""

import math
import time
from typing import Optional, TYPE_CHECKING

import pygame
from MooToo.constants import PlanetClimate, PlanetSize, PlanetCategory
from MooToo.utils import PlanetId, SystemId
from MooToo.ui.proxy.proxy_util import get_distance_tuple
from MooToo.ui.base_graphics import BaseGraphics, load_image
from MooToo.ui.gui_button import Button

if TYPE_CHECKING:
    from MooToo.ui.game import Game


#####################################################################################################
class OrbitWindow(BaseGraphics):
    #####################################################################################################
    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.planet_id: Optional[PlanetId] = None  # Which planet we are looking at
        self.system_id: Optional[SystemId] = None  # Which system we are looking at
        self.window: Optional[pygame.Rect] = None  # The window Rect
        self.images = self.load_images()
        self.close_button = Button(load_image("BUFFER0.LBX", 82), self.mid_point + pygame.Vector2(90, 100))

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        start = time.time()
        images = {}
        images["orbit_window"] = load_image("BUFFER0.LBX", 73)
        images["gas_giant"] = load_image("BUFFER0.LBX", 142)

        images["big_BLUE_star"] = load_image("BUFFER0.LBX", 83)
        images["big_WHITE_star"] = load_image("BUFFER0.LBX", 154)
        images["big_YELLOW_star"] = load_image("BUFFER0.LBX", 160)
        images["big_ORANGE_star"] = load_image("BUFFER0.LBX", 166)
        images["big_RED_star"] = load_image("BUFFER0.LBX", 172)
        images["big_BROWN_star"] = load_image("BUFFER0.LBX", 178)

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
                images[f"planet_{climate.name}_{size.name}"] = load_image("BUFFER0.LBX", index, frame=0)
                index += 1

        for orbit in range(5):
            images[f"orbit_{orbit}"] = load_image("BUFFER0.LBX", 90, frame=orbit)
            images[f"asteroid_{orbit}"] = load_image("BUFFER0.LBX", 91, frame=orbit)

        end = time.time()
        print(f"Orbit: Loaded {len(images)} in {end-start} seconds")

        return images

    #####################################################################################################
    def draw_planet_details(self, planet_id: PlanetId):
        """Describe details of planet in text format"""
        planet = self.game.galaxy.planets[planet_id]
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
    def mouse_pos(self, event: pygame.event):
        """ """
        pos = pygame.mouse.get_pos()
        if self.window is None or not self.window.collidepoint(pos):
            return
        if planet := self.pick_planet(pos):
            self.planet_id = planet

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.close_button.clicked():
            self.system_id = None
            self.planet_id = None
            return True
        return False

    #####################################################################################################
    def pick_planet(self, coords: tuple[int, int]) -> Optional[PlanetId]:
        """Return which planet the mouse coords are close to"""
        system = self.game.galaxy.systems[self.system_id]
        if not system.orbits:
            return None
        for orbit, planet_id in enumerate(system.orbits):
            if not planet_id:
                continue

            planet = self.game.galaxy.planets[planet_id]
            sys_coords = get_planet_position(planet.arc, orbit)
            adjusted_coords = sys_coords + self.mid_point
            distance = get_distance_tuple(adjusted_coords, coords)
            if distance < 20:
                return planet.id
        return None

    #####################################################################################################
    def draw_asteroid(self, orbit: int) -> None:
        """Draw an asteroid belt"""
        image = self.images[f"asteroid_{orbit}"]
        self.draw_centered_image(image)

    #####################################################################################################
    def draw(self, system_id: SystemId) -> None:
        """Draw a solar system"""
        image = self.images["orbit_window"]
        self.window = self.draw_centered_image(image)
        self.system_id = system_id
        system = self.game.galaxy.systems[self.system_id]

        # Draw Sun
        star_image = self.images[f"big_{system.colour.name}_star"]
        self.draw_centered_image(star_image)

        for orbit, planet in enumerate(system.orbits):
            if not planet:
                continue
            self.draw_planet_in_orbit(orbit, planet)
        if self.planet_id:
            self.draw_planet_details(self.planet_id)
        self.close_button.draw(self.screen)

    #####################################################################################################
    def draw_planet_in_orbit(self, orbit: int, planet_id: PlanetId) -> None:
        planet = self.game.galaxy.planets[planet_id]
        position = get_planet_position(planet.arc, orbit)
        orbit_image = self.images[f"orbit_{orbit}"]

        match planet.category:
            case PlanetCategory.GAS_GIANT:
                self.draw_centered_image(orbit_image)
                self.draw_gas_giant(position)
            case PlanetCategory.PLANET:
                self.draw_centered_image(orbit_image)
                self.draw_planet(planet_id, position)
            case PlanetCategory.ASTEROID:
                self.draw_asteroid(orbit)

    #####################################################################################################
    def draw_gas_giant(self, position: pygame.Vector2) -> None:
        """Draw a gas giant"""
        image = self.images["gas_giant"]
        image_position = self.top_left(image, position) + self.mid_point
        self.screen.blit(image, image_position)

    #####################################################################################################
    def draw_planet(self, planet_id: PlanetId, position: pygame.Vector2) -> None:
        """Draw a specific planet"""
        planet = self.game.galaxy.planets[planet_id]
        image = self.images[f"planet_{planet.climate.name}_{planet.size.name}"]
        image_position = self.top_left(image, position) + self.mid_point
        self.screen.blit(image, image_position)


#####################################################################################################
def get_planet_position(arc: float, orbit: int) -> pygame.Vector2:
    x = (91 / 2 + orbit * 47 / 2) * math.cos(math.radians(arc))
    y = (46 / 2 + orbit * 27 / 2) * math.sin(math.radians(arc))
    return pygame.Vector2(x, y)


# EOF
