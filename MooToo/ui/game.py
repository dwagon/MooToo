#!/usr/bin/env python
import random
import sys
import time
from typing import Optional

import pygame
from enum import Enum, StrEnum, auto
from MooToo.ui.gui_button import Button, InvisButton
from MooToo.ui.orbit_window import OrbitWindow
from MooToo.ui.base_graphics import BaseGraphics
from MooToo.ui.planet_window import PlanetWindow
from MooToo.ui.science_window import ScienceWindow
from MooToo.ui.fleet_window import FleetWindow
from MooToo.ui.colony_window import ColonySummaryWindow
from MooToo.ui.planet_summary import PlanetSummaryWindow
from MooToo.galaxy import Galaxy, save, load
from MooToo.ship import Ship
from MooToo.system import System
from MooToo.utils import get_research
from MooToo.planet import Planet
from MooToo.food import empire_food
from MooToo.constants import Technology

MAX_NEBULAE = 5


#####################################################################################################
class DisplayMode(Enum):
    GALAXY = auto()
    PLANET = auto()
    ORBIT = auto()
    SCIENCE = auto()
    FLEET = auto()
    COLONY_SUM = auto()
    PLANET_SUM = auto()


#####################################################################################################
class MainButtons(StrEnum):
    TURN = auto()
    SCIENCE = auto()
    COLONY_SUMMARY = auto()
    PLANET_SUMMARY = auto()


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
        self.colonies_window = ColonySummaryWindow(self.screen, self)
        self.planet_summary_window = PlanetSummaryWindow(self.screen, self, self.empire)
        self.images = self.load_images()
        self.nebulae: list[tuple[str, pygame.Vector2]] = self.calculate_nebulae()
        self.buttons = {
            MainButtons.TURN: Button(self.images["turn_button"], pygame.Vector2(540, 440)),
            MainButtons.SCIENCE: InvisButton(pygame.Rect(547, 346, 65, 69)),
            MainButtons.COLONY_SUMMARY: Button(
                self.images["colonies_button"], pygame.Vector2(0, 428), click_area=pygame.Rect(0, 434, 74, 52)
            ),
            MainButtons.PLANET_SUMMARY: Button(
                self.images["planets_button"],
                pygame.Vector2(0, 428),
                pygame.Rect(82, 434, 74, 52),
            ),
        }
        self.ship_rects: list[tuple[pygame.Rect, list[Ship]]] = []
        self.system_rects: list[tuple[pygame.Rect, System]] = []

    #####################################################################################################
    def calculate_nebulae(self) -> list[tuple[str, pygame.Vector2]]:
        nebulae = []
        num_nebulae = random.randint(1, MAX_NEBULAE)
        neb_images = [_ for _ in self.images if _.startswith("nebula")]
        for _ in range(num_nebulae):
            x = random.randint(0, 520)
            y = random.randint(0, 400)
            nebula = random.choice(neb_images)
            neb_images.remove(nebula)
            nebulae.append((nebula, pygame.Vector2(x, y)))
        return nebulae

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.surface.Surface]:
        """Load all the images from disk"""
        start = time.time()
        images = {}
        images["base_window"] = self.load_image("BUFFER0.LBX", 0)
        images["star_bg"] = self.load_image("STARBG.LBX", 0, palette_index=2)
        for neb in range(6, 52):
            try:
                images[f"nebula_{neb}"] = self.load_image("STARBG.LBX", neb)
            except IndexError:
                pass

        images["small_blue_star"] = self.load_image("BUFFER0.LBX", 149)
        images["small_white_star"] = self.load_image("BUFFER0.LBX", 155)
        images["small_yellow_star"] = self.load_image("BUFFER0.LBX", 161)
        images["small_orange_star"] = self.load_image("BUFFER0.LBX", 167)
        images["small_red_star"] = self.load_image("BUFFER0.LBX", 173)
        images["small_brown_star"] = self.load_image("BUFFER0.LBX", 179)
        images["ship"] = self.load_image("BUFFER0.LBX", 205)
        images["turn_button"] = self.load_image("BUFFER0.LBX", 2)
        images["colonies_button"] = self.load_image("BUFFER0.LBX", 3)
        images["planets_button"] = self.load_image("BUFFER0.LBX", 4)

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
            case DisplayMode.COLONY_SUM:
                self.display_mode = DisplayMode.GALAXY

    #####################################################################################################
    def button_left_down_galaxy_view(self):
        """In the galaxy view someone has clicked the left button"""
        mouse = pygame.mouse.get_pos()
        if self.buttons[MainButtons.TURN].clicked():
            self.galaxy.turn()
            save(self.galaxy, "save")
        elif self.buttons[MainButtons.COLONY_SUMMARY].clicked():
            self.display_mode = DisplayMode.COLONY_SUM
        elif self.buttons[MainButtons.PLANET_SUMMARY].clicked():
            self.planet_summary_window.loop()
        elif self.buttons[MainButtons.SCIENCE].clicked():
            self.display_mode = DisplayMode.SCIENCE
        for rect, ships in self.ship_rects:
            if rect.collidepoint(mouse[0], mouse[1]):
                self.display_mode = DisplayMode.FLEET
                self.fleet_window.reset(ships)

        if system := self.click_system():
            if self.empire.is_known_system(system):
                self.planet_window.loop(pick_planet(system))
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
                elif system := self.click_system():
                    self.fleet_window.select_destination(system)
            case DisplayMode.COLONY_SUM:
                if self.colonies_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.PLANET_SUM:
                pass  # Handled in the planet summary window

    #####################################################################################################
    def draw_screen(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.draw_galaxy_view()
            case DisplayMode.ORBIT:
                self.draw_galaxy_view()
                self.orbit_window.draw(self.system)
            case DisplayMode.SCIENCE:
                self.draw_galaxy_view()
                self.science_window.draw()
            case DisplayMode.FLEET:
                self.draw_galaxy_view()
                self.fleet_window.draw()
            case DisplayMode.COLONY_SUM:
                self.colonies_window.draw()
            case DisplayMode.PLANET_SUM | DisplayMode.PLANET:
                pass  # Handled in the window

    #####################################################################################################
    def draw_galaxy_view(self):
        self.draw_background()
        self.system_rects = []
        for system in self.galaxy.systems.values():
            self.draw_galaxy_view_system(system)
        for button in self.buttons.values():
            button.draw(self.screen)
        self.draw_research()
        self.draw_income()
        self.draw_date()
        self.draw_food()
        self.draw_fleets()

    #####################################################################################################
    def draw_background(self):
        """Draw the background"""
        self.screen.blit(self.images["star_bg"], (0, 0))

        for image_name, location in self.nebulae:
            self.screen.blit(self.images[image_name], location)
        self.screen.blit(self.images["base_window"], (0, 0))

    #####################################################################################################
    def draw_fleets(self):
        rects: dict[tuple[int, int, int, int], list[Ship]] = {}
        self.ship_rects = []
        for empire in self.galaxy.empires:
            for ship in self.galaxy.empires[empire].ships:
                ship_image = self.images["ship"]
                if system := ship.orbit:
                    star_img_size = self.images[f"small_{system.colour.name.lower()}_star"].get_size()

                    if ship.destination:  # Ship is in orbit with a destination (top-left of star)
                        delta = pygame.Vector2(
                            -star_img_size[0] / 2 - ship_image.get_size()[0],
                            -star_img_size[1] / 2 - ship_image.get_size()[1],
                        )
                    else:  # Ship is in orbit with no destination (top-right of star)
                        delta = pygame.Vector2(
                            star_img_size[0] / 2 - ship_image.get_size()[0] / 2,
                            -star_img_size[1] / 2 - ship_image.get_size()[1],
                        )
                    ship_coord = system.position + delta
                    pygame.draw.line(
                        self.screen,
                        "purple",
                        system.position,
                        system.position + delta,
                    )
                else:  # Ship is in space with a destination
                    ship_coord = ship.location

                if ship.destination:
                    mid_pos = ship_coord + pygame.Vector2(ship_image.get_size()[0] / 2, ship_image.get_size()[1] / 2)
                    pygame.draw.line(
                        self.screen,
                        "purple",
                        mid_pos,
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
    def draw_date(self) -> None:
        date_year = 3500 + self.galaxy.turn_number // 10
        date_month = self.galaxy.turn_number % 10
        date_str = f"{date_year}.{date_month}"
        top_left = pygame.Vector2(557, 29)
        rp_text_surface = self.text_font.render(date_str, True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)

    #####################################################################################################
    def draw_food(self) -> None:
        food = empire_food(self.empire)
        top_left = pygame.Vector2(580, 250)
        rp_text_surface = self.text_font.render(f"{food}", True, "white", "black")
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
        try:
            time_left = int((research.cost - self.empire.research_spent) / self.empire.get_research_points())
        except ZeroDivisionError:
            time_left = 10000

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
def pick_planet(system: System) -> Planet:
    """When we look at a system which planet should we start with"""
    max_pop = -1
    picked_planet = None
    for planet in system.orbits:
        if not planet:
            continue
        if planet.current_population() > max_pop:
            max_pop = planet.current_population()
            picked_planet = planet
    return picked_planet


#####################################################################################################
def main(load_file=""):
    galaxy = Galaxy()
    if load_file:
        galaxy = load(load_file)
    else:
        galaxy.populate()
        save(galaxy, "initial")

        # Jumpstart tech for debugging purposes
        for empire in galaxy.empires.values():
            empire.learnt(Technology.STANDARD_FUEL_CELLS)
            empire.learnt(Technology.NUCLEAR_DRIVE)

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
