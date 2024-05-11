#!/usr/bin/env python
import random
import time
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
from MooToo.planet_window import PlanetWindow


#####################################################################################################
class DisplayMode(Enum):
    GALAXY = auto()
    SYSTEM = auto()
    ORBIT = auto()


#####################################################################################################
class Game(BaseGraphics):
    def __init__(self, galaxy: Galaxy, empire_name: str, config: Config):
        super().__init__(config)
        self.display_mode = DisplayMode.GALAXY
        self.galaxy = galaxy
        self.empire = galaxy.empires[empire_name]
        self.system = None  # System we are looking at
        self.planet = None  # Planet we are looking at
        self.orbit_window = OrbitWindow(self.screen, config)
        self.planet_window = PlanetWindow(self.screen, config)
        self.images = self.load_images()
        self.turn_button = Button(self.load_image("BUFFER0.LBX", 2), pygame.Vector2(540, 440))

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.surface.Surface]:
        """Load all the images from disk"""
        start = time.time()
        images = {}
        images["small_blue_star"] = self.load_image("BUFFER0.LBX", 149)
        images["small_white_star"] = self.load_image("BUFFER0.LBX", 155)
        images["small_yellow_star"] = self.load_image("BUFFER0.LBX", 161)
        images["small_orange_star"] = self.load_image("BUFFER0.LBX", 167)
        images["small_red_star"] = self.load_image("BUFFER0.LBX", 173)
        images["small_brown_star"] = self.load_image("BUFFER0.LBX", 179)
        end = time.time()
        print(f"Main: Loaded {len(images)} in {end-start} seconds")

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
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_pos()

            # fill the screen with a color to wipe away anything from last frame
            self.draw_screen()
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    #####################################################################################################
    def mouse_pos(self):
        """Display changes based on where the mouse is"""
        match self.display_mode:
            case DisplayMode.GALAXY:
                pass
            case DisplayMode.ORBIT:
                self.orbit_window.mouse_pos()
            case DisplayMode.SYSTEM:
                pass

    #####################################################################################################
    def button_right_down(self):
        """User has pressed the right button"""
        match self.display_mode:
            case DisplayMode.GALAXY:
                pass
            case DisplayMode.SYSTEM:
                pass
            case DisplayMode.ORBIT:
                self.display_mode = DisplayMode.SYSTEM

    #####################################################################################################
    def button_left_down(self):
        mouse = pygame.mouse.get_pos()
        match self.display_mode:
            case DisplayMode.GALAXY:
                if system := self.pick_system(mouse):
                    if self.empire.is_known(system):
                        self.planet_window.planet = self.pick_planet(system)
                        self.display_mode = DisplayMode.SYSTEM
                    else:
                        self.display_mode = DisplayMode.ORBIT
                    self.system = system
                if self.turn_button.clicked():
                    self.galaxy.turn()
            case DisplayMode.ORBIT:
                if self.orbit_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.SYSTEM:
                if self.planet_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY

    #####################################################################################################
    def pick_planet(self, system: System) -> Planet:
        """When we look at a system which planet should we start with"""
        max_pop = -1
        pick_planet = None
        for planet in system.orbits.values():
            if not planet:
                continue
            if planet.population > max_pop:
                max_pop = planet.population
                pick_planet = planet
        return pick_planet

    #####################################################################################################
    def pick_system(self, coords: tuple[int, int]) -> Optional[System]:
        """Return which system the mouse coords are close to"""
        for sys_coord, system in self.galaxy.systems.items():
            distance = get_distance(sys_coord[0], sys_coord[1], coords[0], coords[1])
            if distance < 20:
                return system
        return None

    #####################################################################################################
    def draw_screen(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.draw_galaxy_view()
            case DisplayMode.ORBIT:
                self.draw_galaxy_view()
                self.orbit_window.draw(self.system)
            case DisplayMode.SYSTEM:
                self.planet_window.draw(self.system)

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
        img_size = star_image.get_size()
        img_coord = (sys_coord[0] - img_size[0] / 2, sys_coord[1] - img_size[1] / 2)
        self.screen.blit(star_image, img_coord)

        if self.empire.is_known(system):
            text_surface = self.label_font.render(system.name, True, "red")
            text_size = text_surface.get_size()
            text_coord = (sys_coord[0] - text_size[0] / 2, sys_coord[1] + img_size[1] / 2)
            self.screen.blit(text_surface, text_coord)


#####################################################################################################
def main():
    config = Config("config.json")
    galaxy = Galaxy(config)
    galaxy.populate()

    empire_name = random.choice(list(galaxy.empires.keys()))

    g = Game(galaxy, empire_name, config)
    g.loop()
    pygame.quit()


#####################################################################################################
if __name__ == "__main__":
    main()

# EOF
