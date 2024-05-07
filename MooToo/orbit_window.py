""" Stuff relating to drawing the orbit window"""

import pygame
from MooToo.planet import Planet
from MooToo.base_graphics import BaseGraphics
from MooToo.system import System
from MooToo.gui_button import Button
from MooToo.config import Config
from MooToo.constants import PlanetCategory, PlanetClimate, PlanetSize


#####################################################################################################
class OrbitWindow(BaseGraphics):
    #####################################################################################################
    def __init__(self, screen: pygame.Surface, config: Config):
        super().__init__(config)
        self.screen = screen
        self.images = self.load_images()
        self.close_button = Button(self.load_image("BUFFER0.LBX", 82), self.mid_point + pygame.Vector2(90, 100))

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
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
        return images

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.close_button.clicked():
            return True
        return False

    #####################################################################################################
    def draw_centered_image(self, image):
        tl = self.top_left(image, self.mid_point)
        self.screen.blit(image, tl)

    #####################################################################################################
    def draw_asteroid(self, planet: Planet) -> None:
        """Draw an asteroid belt"""
        image = self.images[f"asteroid_{planet.orbit}"]
        self.draw_centered_image(image)

    #####################################################################################################
    def draw(self, system: System):
        """Draw a solar system"""
        window = self.images["orbit_window"]
        self.draw_centered_image(window)

        # Draw Sun
        star_image = self.images[f"big_{system.draw_colour}_star"]
        self.draw_centered_image(star_image)

        for orbit, planet in system.orbits.items():
            if planet is None:
                continue
            self.draw_planet_in_orbit(planet)
        self.close_button.draw(self.screen)

    #####################################################################################################
    def draw_planet_in_orbit(self, planet: Planet) -> None:
        # Draw the orbit
        orbit_image = self.images[f"orbit_{planet.orbit}"]
        self.draw_centered_image(orbit_image)

        # Draw the planet
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
        self.draw_label_planet(image, position, planet.name)

    #####################################################################################################
    def draw_planet(self, planet: Planet, position: pygame.Vector2) -> None:
        """Draw a specific planet"""
        image = self.images[f"planet_{planet.climate.name}_{planet.size.name}"]
        self.draw_label_planet(image, position, planet.name)

    #####################################################################################################
    def draw_label_planet(self, image: pygame.surface.Surface, position: pygame.Vector2, name: str) -> None:
        """Draw a specific planet"""
        image_size = image.get_size()
        image_position = self.top_left(image, position) + self.mid_point
        self.screen.blit(image, image_position)
        # Label the planet
        text_surface = self.label_font.render(name, True, "white")
        text_size = text_surface.get_size()
        text_coord = (
            image_position[0] + image_size[0] / 2 - text_size[0] / 2,
            image_position[1] + image_size[1] - text_size[1] / 2,
        )
        self.screen.blit(text_surface, text_coord)
