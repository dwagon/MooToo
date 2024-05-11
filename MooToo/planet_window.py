""" Display Planet Details"""

import time
import pygame
from MooToo.base_graphics import BaseGraphics
from MooToo.constants import PlanetClimate
from MooToo.system import System
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
        self.system = None
        self.images = self.load_images()
        self.return_button = Button(self.load_image("COLPUPS.LBX", 4), pygame.Vector2(555, 460))

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
        end = time.time()
        print(f"Planet: Loaded {len(images)} in {end-start} seconds")
        return images

    #####################################################################################################
    def draw(self, system: System):
        climate = self.images[self.planet.climate_image]
        self.draw_centered_image(climate)
        image = self.images["window"]
        self.window = self.draw_centered_image(image)
        self.system = system

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.return_button.clicked():
            self.system = None
            self.planet = None
            return True
        return False

    #####################################################################################################
    def draw_centered_image(self, image: pygame.Surface) -> pygame.Rect:
        tl = self.top_left(image, self.mid_point)
        return self.screen.blit(image, tl)
