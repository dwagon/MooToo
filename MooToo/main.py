#!/usr/bin/env python

import math
from typing import Optional

import pygame
from enum import Enum, auto
from MooToo.config import Config
from MooToo.galaxy import Galaxy, get_distance
from MooToo.system import System
from MooToo.planet import Planet


class DisplayMode(Enum):
    GALAXY = auto()
    SYSTEM = auto()
    PLANET = auto()


#####################################################################################################
class Game:
    def __init__(self, galaxy: Galaxy, config: Config):
        self.galaxy = galaxy
        self.config = config
        pygame.init()
        self.font = pygame.font.SysFont("Ariel", 14)
        self.screen = pygame.display.set_mode((config["display"]["screen_width"], config["display"]["screen_height"]))
        self.clock = pygame.time.Clock()
        self.display_mode = DisplayMode.GALAXY
        self.system = None

    def loop(self):
        running = True

        while running:
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
            self.screen.fill("black")
            self.draw_screen()
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    def button_right_down(self):
        """User has pressed the right button"""
        self.display_mode = DisplayMode.GALAXY

    def button_left_down(self):
        mouse = pygame.mouse.get_pos()
        match self.display_mode:
            case DisplayMode.GALAXY:
                system = self.pick_system(mouse)
                if system:
                    self.display_mode = DisplayMode.SYSTEM
                    self.system = system
            case DisplayMode.SYSTEM:
                pass
            case DisplayMode.PLANET:
                pass

    def pick_system(self, coords: tuple[int, int]) -> Optional[System]:
        """Return which system the coords are close to"""
        for sys_coord, system in self.galaxy.systems.items():
            game_coords = self.screen_to_game(sys_coord)
            distance = get_distance(game_coords[0], game_coords[1], coords[0], coords[1])
            if distance < 20:
                return system
        return None

    def draw_screen(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.draw_galaxy()
            case DisplayMode.SYSTEM:
                self.draw_system()
            case DisplayMode.PLANET:
                self.draw_planet()

    def draw_system(self):
        """Draw a solar system"""
        size = self.screen.get_size()
        mid_point = (size[0] / 2, size[1] / 2)
        # Draw Sun
        pygame.draw.circle(
            self.screen,
            self.system.draw_colour,
            mid_point,
            20,
        )
        for orbit, planet in self.system.orbits.items():
            if planet is None:
                continue
            self.draw_planet_in_orbit(orbit, planet)

    def draw_planet_in_orbit(self, orbit: int, planet: Planet):
        size = self.screen.get_size()
        mid_point = (size[0] / 2, size[1] / 2)
        radius = 50 * orbit + 100
        pygame.draw.circle(self.screen, self.system.draw_colour, mid_point, radius, width=1)
        pos_x = radius * math.cos(planet.arc) + mid_point[0]
        pos_y = radius * math.sin(planet.arc) + mid_point[1]
        pygame.draw.circle(self.screen, "blue", (pos_x, pos_y), 10)
        text_surface = self.font.render(planet.name, True, "white")
        text_size = text_surface.get_size()
        text_coord = (pos_x - text_size[0] / 2, pos_y + text_size[1] / 2)
        self.screen.blit(text_surface, text_coord)

    def draw_planet(self):
        pass

    def draw_galaxy(self):
        for sys_coord, system in self.galaxy.systems.items():
            self.draw_galaxy_view_system(sys_coord, system)

    def draw_galaxy_view_system(self, sys_coord, system):
        screen_coord = self.game_to_screen(sys_coord)
        pygame.draw.circle(self.screen, system.draw_colour, screen_coord, 5.0)

        text_surface = self.font.render(system.name, True, "white")
        text_size = text_surface.get_size()
        text_coord = (screen_coord[0] - text_size[0] / 2, screen_coord[1] + text_size[1] / 2)
        self.screen.blit(text_surface, text_coord)

    def game_to_screen(self, game_coord: tuple[int, int]) -> tuple[float, float]:
        x = game_coord[0] * self.config["galaxy"]["max_x"] / self.config["display"]["screen_width"]
        y = game_coord[1] * self.config["galaxy"]["max_y"] / self.config["display"]["screen_height"]
        return x, y

    def screen_to_game(self, screen_coord: tuple[float, float]) -> tuple[int, int]:
        x = screen_coord[0] * self.config["display"]["screen_width"] / self.config["galaxy"]["max_x"]
        y = screen_coord[1] * self.config["display"]["screen_height"] / self.config["galaxy"]["max_y"]
        return x, y


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
