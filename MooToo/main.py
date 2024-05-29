#!/usr/bin/env python
import sys
import time
import pygame
from enum import Enum, auto
from MooToo.galaxy import Galaxy, load, save
from MooToo.system import System
from MooToo.ship import Ship
from MooToo.planet import Planet
from MooToo.gui_button import Button, InvisButton
from MooToo.orbit_window import OrbitWindow
from MooToo.base_graphics import BaseGraphics
from MooToo.planet_window import PlanetWindow
from MooToo.science_window import ScienceWindow
from MooToo.fleet_window import FleetWindow


#####################################################################################################
class DisplayMode(Enum):
    GALAXY = auto()
    SYSTEM = auto()
    ORBIT = auto()
    SCIENCE = auto()
    FLEET = auto()


#####################################################################################################
class Game(BaseGraphics):
    def __init__(self, galaxy: Galaxy, empire_name: str):
        super().__init__(self)
        self.display_mode = DisplayMode.GALAXY
        self.galaxy = galaxy
        self.empire = galaxy.empires[empire_name]
        self.system = None  # System we are looking at
        self.planet = None  # Planet we are looking at
        self.orbit_window = OrbitWindow(self.screen, self)
        self.planet_window = PlanetWindow(self.screen, self)
        self.science_window = ScienceWindow(self.screen, self)
        self.fleet_window = FleetWindow(self.screen, self)
        self.images = self.load_images()
        self.turn_button = Button(self.load_image("BUFFER0.LBX", 2), pygame.Vector2(540, 440))
        self.science_button = InvisButton(pygame.Rect(547, 346, 65, 69))
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

            # fill the screen with a color to wipe away anything from last frame
            self.draw_screen()
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

    #####################################################################################################
    def button_up(self):
        """Mouse button released"""
        match self.display_mode:
            case DisplayMode.GALAXY:
                pass
            case DisplayMode.ORBIT:
                pass
            case DisplayMode.SYSTEM:
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
            case DisplayMode.SYSTEM:
                pass
            case DisplayMode.FLEET:
                self.fleet_window.mouse_pos(event)

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
                if self.turn_button.clicked():
                    self.galaxy.turn()
                    save(self.galaxy, "test")
                if self.science_button.clicked():
                    self.display_mode = DisplayMode.SCIENCE
                for rect, ships in self.ship_rects:
                    if rect.collidepoint(mouse[0], mouse[1]):
                        self.display_mode = DisplayMode.FLEET
                        self.fleet_window.reset(ships)
                for rect, system in self.system_rects:
                    if rect.collidepoint(mouse[0], mouse[1]):
                        if self.empire.is_known_system(system):
                            self.planet_window.planet = self.pick_planet(system)
                            self.display_mode = DisplayMode.SYSTEM
                        else:
                            self.display_mode = DisplayMode.ORBIT
                        self.system = system
            case DisplayMode.ORBIT:
                if self.orbit_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.SYSTEM:
                if self.planet_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.SCIENCE:
                if self.science_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.FLEET:
                if self.fleet_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY

    #####################################################################################################
    def pick_planet(self, system: System) -> Planet:
        """When we look at a system which planet should we start with"""
        max_pop = -1
        pick_planet = None
        for planet in system.orbits:
            if not planet:
                continue
            if planet.population > max_pop:
                max_pop = planet.population
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
            case DisplayMode.SYSTEM:
                self.planet_window.draw(self.system)
            case DisplayMode.SCIENCE:
                self.draw_galaxy_view()
                self.science_window.draw()
            case DisplayMode.FLEET:
                self.draw_galaxy_view()
                self.fleet_window.draw()

    #####################################################################################################
    def draw_galaxy_view(self):
        self.screen.blit(self.images["base_window"], (0, 0))
        self.ship_rects = []
        self.system_rects = []
        for system in self.galaxy.systems.values():
            self.draw_galaxy_view_system(system)
        self.turn_button.draw(self.screen)
        self.draw_research()
        self.draw_income()

    #####################################################################################################
    def draw_income(self):
        """Draw money / income"""
        top_left = pygame.Vector2(555, 72)
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
        if self.empire.researching:
            words = self.empire.researching.name
        else:
            words = "Nothing"

        top_left = pygame.Vector2(550, 360)
        for word in words.split():
            rp_text_surface = self.text_font.render(word, True, "white", "black")
            self.screen.blit(rp_text_surface, top_left)
            top_left.x = 570
            top_left.y += rp_text_surface.get_size()[1]

        if self.empire.researching:
            words = (
                f"{self.empire.research_spent}/{self.empire.researching.cost} (+{self.empire.get_research_points()}) RP"
            )
        else:
            words = f"+{self.empire.get_research_points()} RP"
        rp = self.text_font.render(words, True, "white", "black")
        self.screen.blit(rp, pygame.Vector2(550, top_left.y + 10))

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

            if ships := system.ships_in_orbit():
                ship_image = self.images["ship"]
                ship_coord = img_coord + pygame.Vector2(img_size[0] - 5, 0)
                r = self.screen.blit(ship_image, ship_coord)
                self.ship_rects.append((r, ships))
                dbg_rect = pygame.draw.rect(self.screen, "purple", r, width=1)  # DBG


#####################################################################################################
def main(load_file=""):
    if load_file:
        galaxy = load(load_file)
    else:
        galaxy = Galaxy()
        galaxy.populate()

    empire_name = list(galaxy.empires.keys())[0]

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
