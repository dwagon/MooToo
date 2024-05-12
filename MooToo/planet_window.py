""" Display Planet Details"""

import time
import pygame
from MooToo.base_graphics import BaseGraphics
from MooToo.constants import PlanetClimate, PlanetCategory, PlanetSize
from MooToo.system import System, MAX_ORBITS
from MooToo.planet import Planet
from MooToo.config import Config
from MooToo.gui_button import Button


#####################################################################################################
#####################################################################################################
class PlanetWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, config: Config):
        """ """
        super().__init__(config)
        self.screen = screen
        self.planet = None
        self.images = self.load_images()
        self.return_button = Button(self.load_image("COLPUPS.LBX", 4), pygame.Vector2(555, 460))
        self.system_rects: dict[tuple[float, float, float, float], Planet] = {}
        self.colony_font = pygame.font.SysFont("Ariel", 18, bold=True)

    #####################################################################################################
    def load_images(self):
        # Toxic 0, 1
        # 2
        # 3
        # 4
        # 5 Radiated (Shielded)
        # 6 Barren
        # 7
        # 8
        # 9
        # 10
        # 11 Desert
        # Tundra 12, 14
        # 13
        # 15
        # 16
        # 17
        # 18
        # 19 Swamp
        # 20
        # 21
        # 22 Arid
        # 23
        # 24
        # 25 Terran
        # 26
        # 27
        # 28 Gaia
        # 29
        start = time.time()
        images = {}
        images["window"] = self.load_image("COLPUPS.LBX", 5, 0, "FONTS.LBX", 2)
        images["orbit_arrow"] = self.load_image("COLSYSDI.LBX", 64, 0, "FONTS.LBX", 2)
        index = 0
        for climate in [
            PlanetClimate.TOXIC,
            PlanetClimate.RADIATED,
            PlanetClimate.BARREN,
            PlanetClimate.DESERT,
            PlanetClimate.TUNDRA,
            PlanetClimate.OCEAN,
            PlanetClimate.SWAMP,
            PlanetClimate.ARID,
            PlanetClimate.TERRAN,
            PlanetClimate.GAIA,
        ]:
            for number in range(3):
                images[f"surface_{climate}_{number}"] = self.load_image("PLANETS.LBX", index)
                index += 1
        index = 6
        for climate in [
            PlanetClimate.TOXIC,
            PlanetClimate.RADIATED,
            PlanetClimate.BARREN,
            PlanetClimate.DESERT,
            PlanetClimate.TUNDRA,
            PlanetClimate.OCEAN,
            PlanetClimate.SWAMP,
            PlanetClimate.ARID,
            PlanetClimate.TERRAN,
            PlanetClimate.GAIA,
        ]:
            for size in [PlanetSize.TINY, PlanetSize.SMALL, PlanetSize.MEDIUM, PlanetSize.LARGE, PlanetSize.HUGE]:
                images[f"orbit_{climate}_{size}"] = self.load_image("COLSYSDI.LBX", index, 0, "FONTS.LBX", 2)
                index += 1
        images["orbit_gas_giant"] = self.load_image("COLSYSDI.LBX", 62, 0, "FONTS.LBX", 2)
        images["orbit_asteroid"] = self.load_image("COLSYSDI.LBX", 63, 0, "FONTS.LBX", 2)

        end = time.time()
        print(f"Planet: Loaded {len(images)} in {end-start} seconds")
        return images

    #####################################################################################################
    def draw(self, system: System):
        self.draw_centered_image(self.images[self.planet.climate_image])
        self.window = self.draw_centered_image(self.images["window"])
        self.draw_orbits(system)
        self.draw_pop_label(self.planet)
        label_surface = self.colony_font.render(f"{self.planet.name}", True, "white")
        self.screen.blit(
            label_surface,
            pygame.Rect(
                self.mid_point[0] - label_surface.get_size()[0] / 2,
                0,
                label_surface.get_size()[0],
                label_surface.get_size()[1],
            ),
        )

    #####################################################################################################
    def draw_pop_label(self, planet: Planet) -> None:
        text = f"Pop {int(planet.population/1000):,}k (+{int(planet.population_increment()/1000):,}k)"
        text_surface = self.label_font.render(text, True, "white")
        text_size = text_surface.get_size()
        self.screen.blit(text_surface, pygame.Rect(640 - text_size[0], 0, text_size[0], text_size[1]))

    #####################################################################################################
    def draw_orbits(self, system: System):
        """Draw the system summary"""
        height_of_a_row = 25
        top_left = pygame.Vector2(12, 25)
        arrow_col = top_left.x
        planet_col = arrow_col + 9
        label_col = planet_col + 33
        for orbit in range(MAX_ORBITS):
            row_middle = top_left.y + orbit * height_of_a_row + height_of_a_row / 2
            self.draw_orbit_arrow(arrow_col, row_middle)

            if planet := system.orbits[orbit]:
                self.draw_orbit_planet(planet, planet_col, row_middle)
                self.draw_orbit_text(planet, label_col, row_middle)

    #####################################################################################################
    def draw_orbit_arrow(self, arrow_col: float, row_middle: float) -> None:
        # Draw the arrow
        image_size = self.images["orbit_arrow"].get_size()
        arrow_dest = pygame.Rect(
            arrow_col,
            row_middle - image_size[1] / 2,
            image_size[0],
            image_size[1],
        )
        self.screen.blit(self.images["orbit_arrow"], arrow_dest)

    #####################################################################################################
    def draw_orbit_planet(self, planet: Planet, planet_col: float, row_middle: float) -> None:
        # Draw the planet image
        match planet.category:
            case PlanetCategory.ASTEROID:
                image = self.images["orbit_asteroid"]
            case PlanetCategory.GAS_GIANT:
                image = self.images["orbit_gas_giant"]
            case _:
                image = self.images[f"orbit_{planet.climate}_{planet.size}"]
        image_size = image.get_size()
        planet_dest = pygame.Rect(
            planet_col,
            row_middle - image_size[1] / 2,
            image_size[0],
            image_size[1],
        )
        self.screen.blit(image, planet_dest)
        if planet.category == PlanetCategory.PLANET:
            self.system_rects[(planet_dest.left, planet_dest.top, planet_dest.width, planet_dest.height)] = planet

    #####################################################################################################
    def draw_orbit_text(self, planet: Planet, label_col: float, row_middle: float) -> None:
        # Draw the text
        text = self.orbit_label(planet)
        label_surface = self.label_font.render(text, True, "white")
        image_size = label_surface.get_size()
        label_dest = pygame.Rect(
            label_col,
            row_middle - image_size[1] / 2,
            label_surface.get_size()[0],
            label_surface.get_size()[1],
        )
        self.screen.blit(label_surface, label_dest)
        # Have to convert to tuple as Rect is not hashable
        # TODO: Only add rect if we are the owner of the planet

    #####################################################################################################
    def orbit_label(self, planet: Planet) -> str:
        """Empire name (pop/max)"""
        owner = ""
        match planet.category:
            case PlanetCategory.PLANET:
                owner = planet.owner.name if planet.owner else planet.name
            case PlanetCategory.ASTEROID:
                owner = "Asteroids"
            case PlanetCategory.GAS_GIANT:
                owner = "Gas Giant"
        pop = f"({planet.current_population()}/{planet.max_population()})" if planet.current_population() else ""
        return f"{owner} {pop}"

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.return_button.clicked():
            self.planet = None
            return True
        for sys_rect, planet in self.system_rects.items():
            r = pygame.Rect(sys_rect[0], sys_rect[1], sys_rect[2], sys_rect[3])
            if r.collidepoint(pygame.mouse.get_pos()):
                self.planet = planet
        return False
