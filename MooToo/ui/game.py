#!/usr/bin/env python
import random
import sys
import time
from typing import Optional

import pygame
from enum import Enum, auto
from MooToo.ui.gui_button import Button, InvisButton
from MooToo.ui.orbit_window import OrbitWindow
from MooToo.ui.base_graphics import BaseGraphics
from MooToo.ui.planet_window import PlanetWindow
from MooToo.ui.science_window import ScienceWindow
from MooToo.ui.fleet_window import FleetWindow
from MooToo.ui.colony_window import ColonyWindow
from MooToo.galaxy import Galaxy, save, load
from MooToo.ship import Ship
from MooToo.system import System
from MooToo.utils import get_research
from MooToo.planet import Planet


#####################################################################################################
class DisplayMode(Enum):
    GALAXY = auto()
    PLANET = auto()
    ORBIT = auto()
    SCIENCE = auto()
    FLEET = auto()
    COLONIES = auto()


#####################################################################################################
class Game(BaseGraphics):
    def __init__(self, galaxy: Galaxy, empire_name: str):
        super().__init__(self)
        self.galaxy = galaxy
        self.display_mode = DisplayMode.GALAXY
        self.empire = galaxy.empires[empire_name]
        self.system = None  # System we are looking at
        self.planet = None  # Planet we are looking at
        self.orbit_window = OrbitWindow(self.screen, self)
        self.planet_window = PlanetWindow(self.screen, self)
        self.science_window = ScienceWindow(self.screen, self)
        self.fleet_window = FleetWindow(self.screen, self)
        self.colonies_window = ColonyWindow(self.screen, self)
        self.images = self.load_images()
        self.turn_button = Button(self.images["turn_button"], pygame.Vector2(540, 440))
        self.science_button = InvisButton(pygame.Rect(547, 346, 65, 69))
        self.colonies_button = Button(self.images["colonies_button"], pygame.Vector2(0, 428))
        self.ship_rects: list[tuple[pygame.Rect, list[Ship]]] = []
        self.system_rects: list[tuple[pygame.Rect, System]] = []

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.surface.Surface]:
        """Load all the images from disk"""
        start = time.time()
        images = {}
        images["base_window"] = self.load_image("BUFFER0.LBX", 0)

        images["small_blue_star"] = self.load_image("BUFFER0.LBX", 149)
        images["small_white_star"] = self.load_image("BUFFER0.LBX", 155)
        images["small_yellow_star"] = self.load_image("BUFFER0.LBX", 161)
        images["small_orange_star"] = self.load_image("BUFFER0.LBX", 167)
        images["small_red_star"] = self.load_image("BUFFER0.LBX", 173)
        images["small_brown_star"] = self.load_image("BUFFER0.LBX", 179)
        images["ship"] = self.load_image("BUFFER0.LBX", 205)
        images["turn_button"] = self.load_image("BUFFER0.LBX", 2)
        images["colonies_button"] = self.load_image("BUFFER0.LBX", 3)

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
                    self.mouse_pos(event)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.button_up()

            self.draw_screen()
            pygame.display.flip()

            self.clock.tick(60)

    #####################################################################################################
    def button_up(self):
        """Mouse button released"""
        match self.display_mode:
            case DisplayMode.GALAXY:
                pass
            case DisplayMode.ORBIT:
                pass
            case DisplayMode.PLANET:
                pass
            case DisplayMode.FLEET:
                self.fleet_window.button_up()

    #####################################################################################################
    def mouse_pos(self, event: pygame.event):
        """Display changes based on where the mouse is"""
        match self.display_mode:
            case DisplayMode.GALAXY:
                pass
            case DisplayMode.ORBIT:
                self.orbit_window.mouse_pos()
            case DisplayMode.PLANET:
                pass
            case DisplayMode.FLEET:
                self.fleet_window.mouse_pos(event)

    #####################################################################################################
    def button_right_down(self):
        """User has pressed the right button"""
        match self.display_mode:
            case DisplayMode.GALAXY:
                pass
            case DisplayMode.PLANET:
                pass
            case DisplayMode.ORBIT:
                self.display_mode = DisplayMode.PLANET
            case DisplayMode.COLONIES:
                self.display_mode = DisplayMode.GALAXY

    #####################################################################################################
    def button_left_down_galaxy_view(self):
        """In the galaxy view someone has clicked the left button"""
        mouse = pygame.mouse.get_pos()
        if self.turn_button.clicked():
            self.galaxy.turn()
            save(self.galaxy, "save")
        if self.colonies_button.clicked():
            self.display_mode = DisplayMode.COLONIES
        if self.science_button.clicked():
            self.display_mode = DisplayMode.SCIENCE
        for rect, ships in self.ship_rects:
            if rect.collidepoint(mouse[0], mouse[1]):
                self.display_mode = DisplayMode.FLEET
                self.fleet_window.reset(ships)

        if system := self.click_system():
            if self.empire.is_known_system(system):
                self.planet_window.loop(self.pick_planet(system))
            else:
                self.display_mode = DisplayMode.ORBIT
            self.system = system

    #####################################################################################################
    def click_system(self) -> Optional[System]:
        mouse = pygame.mouse.get_pos()
        for rect, system in self.system_rects:
            if rect.collidepoint(mouse[0], mouse[1]):
                return system
        return None

    #####################################################################################################
    def button_left_down(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.button_left_down_galaxy_view()
            case DisplayMode.ORBIT:
                if self.orbit_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.PLANET:
                pass  # Handled in the planet_window
            case DisplayMode.SCIENCE:
                if self.science_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.FLEET:
                if self.fleet_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
                if system := self.click_system():
                    self.fleet_window.select_destination(system)
            case DisplayMode.COLONIES:
                if self.colonies_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY

    #####################################################################################################
    def pick_planet(self, system: System) -> Planet:
        """When we look at a system which planet should we start with"""
        max_pop = -1
        pick_planet = None
        for planet in system.orbits:
            if not planet:
                continue
            if planet.current_population() > max_pop:
                max_pop = planet.current_population()
                pick_planet = planet
        return pick_planet

    #####################################################################################################
    def draw_screen(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.draw_galaxy_view()
            case DisplayMode.ORBIT:
                self.draw_galaxy_view()
                self.orbit_window.draw(self.system)
            case DisplayMode.PLANET:
                pass  # Handled in the planet_window
            case DisplayMode.SCIENCE:
                self.draw_galaxy_view()
                self.science_window.draw()
            case DisplayMode.FLEET:
                self.draw_galaxy_view()
                self.fleet_window.draw()
            case DisplayMode.COLONIES:
                self.colonies_window.draw()

    #####################################################################################################
    def draw_galaxy_view(self):
        self.screen.blit(self.images["base_window"], (0, 0))
        self.system_rects = []
        for system in self.galaxy.systems.values():
            self.draw_galaxy_view_system(system)
        self.turn_button.draw(self.screen)
        self.draw_research()
        self.draw_income()
        self.draw_date()
        self.draw_fleets()

    #####################################################################################################
    def draw_fleets(self):
        rects: dict[tuple[int, int, int, int], list[Ship]] = {}
        self.ship_rects = []
        for empire in self.galaxy.empires:
            for ship in self.galaxy.empires[empire].ships:
                ship_image = self.images["ship"]
                if system := ship.orbit:
                    sys_coord = system.position
                    star_image = self.images[f"small_{system.colour.name.lower()}_star"]
                    img_size = star_image.get_size()
                    img_coord = pygame.Vector2(sys_coord[0] - img_size[0] / 2, sys_coord[1] - img_size[1] / 2)
                    ship_coord = img_coord + pygame.Vector2(img_size[0] - 5, 0)
                else:
                    ship_coord = pygame.Vector2(ship.location[0], ship.location[1])
                    pygame.draw.line(
                        self.screen,
                        "purple",
                        ship.location + pygame.Vector2(ship_image.get_size()[0] / 2, ship_image.get_size()[1] / 2),
                        ship.destination.position,
                    )
                r = self.screen.blit(ship_image, ship_coord)
                rect_tuple = (r.x, r.y, r.h, r.w)
                if rect_tuple not in rects:
                    rects[rect_tuple] = [ship]
                else:
                    rects[rect_tuple].append(ship)
                pygame.draw.rect(self.screen, "purple", r, width=1)  # DBG
        self.ship_rects.extend((pygame.Rect(k[0], k[1], k[2], k[3]), v) for k, v in rects.items())

    #####################################################################################################
    def draw_date(self):
        date_year = 3500 + self.galaxy.turn_number // 10
        date_month = self.galaxy.turn_number % 10
        date_str = f"{date_year}.{date_month}"
        top_left = pygame.Vector2(557, 29)
        rp_text_surface = self.text_font.render(date_str, True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)

    #####################################################################################################
    def draw_income(self):
        """Draw money / income"""
        top_left = pygame.Vector2(555, 92)
        rp_text_surface = self.text_font.render(f"{self.empire.money} BC", True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)
        top_left.y += rp_text_surface.get_size()[1]
        if self.empire.income < 0:
            income_str = f"-{self.empire.income} BC"
        else:
            income_str = f"+{self.empire.income} BC"
        rp_text_surface = self.text_font.render(income_str, True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)

    #####################################################################################################
    def draw_research(self):
        """Draw what is being researched"""
        top_left = pygame.Vector2(550, 380)

        if not self.empire.researching:
            rp_text_surface = self.text_font.render("Nothing", True, "white", "black")
            self.screen.blit(rp_text_surface, top_left)
            return

        research = get_research(self.empire.researching)
        time_left = int((research.cost - self.empire.research_spent) / self.empire.get_research_points())

        words = [
            research.name,
            f"~{time_left} turns",
            f"{self.empire.get_research_points()} RP",
        ]

        for word in words:
            rp_text_surface = self.text_font.render(word, True, "white", "black")
            self.screen.blit(rp_text_surface, top_left)
            top_left.y += rp_text_surface.get_size()[1]

    #####################################################################################################
    def draw_galaxy_view_system(self, system):
        sys_coord = system.position
        star_image = self.images[f"small_{system.colour.name.lower()}_star"]
        img_size = star_image.get_size()
        img_coord = pygame.Vector2(sys_coord[0] - img_size[0] / 2, sys_coord[1] - img_size[1] / 2)
        planet_rect = self.screen.blit(star_image, img_coord)
        pygame.draw.rect(self.screen, "purple", planet_rect, width=1)  # DBG
        self.system_rects.append((planet_rect, system))

        if self.empire.is_known_system(system):
            text_surface = self.label_font.render(system.name, True, "red")
            text_size = text_surface.get_size()
            text_coord = (sys_coord[0] - text_size[0] / 2, sys_coord[1] + img_size[1] / 2)
            self.screen.blit(text_surface, text_coord)


#####################################################################################################
def main(load_file=""):
    galaxy = Galaxy()
    if load_file:
        galaxy = load(load_file)
    else:
        galaxy.populate()
        save(galaxy, "initial")

    empire_name = random.choice(list(galaxy.empires.keys()))

    g = Game(galaxy, empire_name)
    g.loop()
    pygame.quit()


#####################################################################################################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()

# EOF
