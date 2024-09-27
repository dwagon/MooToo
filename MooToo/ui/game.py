#!/usr/bin/env python
import random
import sys
import time
from typing import Optional
from requests.exceptions import ConnectionError

import pygame

from enum import StrEnum, auto

from MooToo.utils import get_research, SystemId, PlanetId, ShipId

from MooToo.ui.constants import DisplayMode
from MooToo.ui.gui_button import Button, InvisButton
from MooToo.ui.orbit_window import OrbitWindow
from MooToo.ui.base_graphics import BaseGraphics, load_image
from MooToo.ui.planet_window import PlanetWindow
from MooToo.ui.science_window import ScienceWindow
from MooToo.ui.fleet_window import FleetWindow
from MooToo.ui.colony_summary import ColonySummaryWindow
from MooToo.ui.planet_summary import PlanetSummaryWindow
from MooToo.ui.proxy.galaxy_proxy import GalaxyProxy as Galaxy


MAX_NEBULAE = 5


#####################################################################################################
class MainButtons(StrEnum):
    TURN = auto()
    SCIENCE = auto()
    COLONY_SUMMARY = auto()
    PLANET_SUMMARY = auto()


#####################################################################################################
class Game(BaseGraphics):
    def __init__(self, empire_id: int = 1):
        try:
            self.galaxy = Galaxy()
        except ConnectionError:
            print("Couldn't initiate galaxy - backend running?")
            sys.exit(1)
        except Exception:
            raise
        super().__init__(self)
        self.display_mode = DisplayMode.GALAXY
        self.empire_id = empire_id
        self.system_id: Optional[SystemId] = None  # System we are looking at
        self.planet_id: Optional[PlanetId] = None  # Planet we are looking at
        self.orbit_window = OrbitWindow(self.screen, self)
        self.planet_window = PlanetWindow(self.screen, self)
        self.science_window = ScienceWindow(self.screen, self)
        self.fleet_window = FleetWindow(self.screen, self)
        self.colonies_window = ColonySummaryWindow(self.screen, self)
        self.planet_summary_window = PlanetSummaryWindow(self.screen, self, self.empire_id)
        self.images = load_images()
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
        self.ship_rects: list[tuple[pygame.Rect, list[ShipId]]] = []
        self.system_rects: list[tuple[pygame.Rect, SystemId]] = []

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
    def loop(self):
        running = True

        while running:
            self.event_loop()

            match self.display_mode:
                case DisplayMode.PLANET:
                    self.display_mode = self.planet_window.loop(self.planet_id)
                case DisplayMode.PLANET_SUM:
                    self.display_mode = self.planet_summary_window.loop()
                case DisplayMode.COLONY_SUM:
                    self.display_mode = self.colonies_window.loop()
                case DisplayMode.PLANET_BUILD:
                    self.display_mode = self.planet_window.building_choice_window.loop(self.planet_id)
                case _:
                    pass

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
                self.orbit_window.mouse_pos(event)
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
            # save(self.galaxy, "save")
        elif self.buttons[MainButtons.COLONY_SUMMARY].clicked():
            self.display_mode = DisplayMode.COLONY_SUM
        elif self.buttons[MainButtons.PLANET_SUMMARY].clicked():
            self.display_mode = DisplayMode.PLANET_SUM
        elif self.buttons[MainButtons.SCIENCE].clicked():
            self.display_mode = DisplayMode.SCIENCE
        for rect, ship_ids in self.ship_rects:
            if rect.collidepoint(mouse[0], mouse[1]):
                self.display_mode = DisplayMode.FLEET
                self.fleet_window.reset(ship_ids)

        if system_id := self.click_system():
            self.system_id = system_id
            empire = self.galaxy.empires[self.empire_id]
            if empire.has_interest_in(system_id):
                self.display_mode = DisplayMode.PLANET
                self.planet_id = self.pick_planet(system_id)
            elif system_id in empire.known_systems:
                self.display_mode = DisplayMode.ORBIT

    #####################################################################################################
    def pick_planet(self, system_id: SystemId) -> PlanetId:
        """When we look at a system which planet should we start with"""
        max_pop = -1
        system = self.galaxy.systems[system_id]
        picked_planet = None
        for planet_id in system.orbits:
            if not planet_id:
                continue
            planet = self.galaxy.planets[planet_id]
            if planet.current_population() > max_pop:
                max_pop = planet.current_population()
                picked_planet = planet
        return picked_planet.id

    #####################################################################################################
    def click_system(self) -> Optional[SystemId]:
        mouse = pygame.mouse.get_pos()
        for rect, system_id in self.system_rects:
            if rect.collidepoint(mouse[0], mouse[1]):
                return system_id
        return None

    #####################################################################################################
    def look_at_planet(self, planet_id: PlanetId) -> None:
        self.display_mode = DisplayMode.PLANET
        self.planet_id = planet_id

    #####################################################################################################
    def button_left_down(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.button_left_down_galaxy_view()
            case DisplayMode.ORBIT:
                if self.orbit_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.SCIENCE:
                if self.science_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
            case DisplayMode.FLEET:
                if self.fleet_window.button_left_down():
                    self.display_mode = DisplayMode.GALAXY
                elif system_id := self.click_system():
                    self.fleet_window.select_destination(system_id)
            case DisplayMode.PLANET_SUM | DisplayMode.PLANET | DisplayMode.COLONY_SUM:
                pass  # Handled in the window

    #####################################################################################################
    def draw(self):
        match self.display_mode:
            case DisplayMode.GALAXY:
                self.draw_galaxy_view()
            case DisplayMode.ORBIT:
                self.draw_galaxy_view()
                self.orbit_window.draw(self.system_id)
            case DisplayMode.SCIENCE:
                self.draw_galaxy_view()
                self.science_window.draw()
            case DisplayMode.FLEET:
                self.draw_galaxy_view()
                self.fleet_window.draw()
            case DisplayMode.PLANET_SUM | DisplayMode.PLANET | DisplayMode.COLONY_SUM:
                pass  # Handled in the window

    #####################################################################################################
    def draw_galaxy_view(self):
        self.draw_background()
        self.system_rects = []
        for system_id in self.galaxy.systems.keys():
            self.draw_galaxy_view_system(system_id)
        for button in self.buttons.values():
            button.draw(self.screen)
        self.draw_research()
        self.draw_income()
        self.draw_date()
        self.draw_food()
        self.draw_fleets()
        self.draw_freighters()

    #####################################################################################################
    def draw_freighters(self):
        """Draw freighters"""
        empire = self.galaxy.empires[self.empire_id]
        freighter_str = f"{empire.freighters - empire.freighters_used()} ({empire.freighters})"
        top_left = pygame.Vector2(570, 320)
        rp_text_surface = self.text_font.render(freighter_str, True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)

    #####################################################################################################
    def draw_background(self):
        """Draw the background"""
        self.screen.blit(self.images["star_bg"], (0, 0))

        for image_name, location in self.nebulae:
            self.screen.blit(self.images[image_name], location)
        self.screen.blit(self.images["base_window"], (0, 0))

    #####################################################################################################
    def draw_fleets(self):
        rects: dict[tuple[int, int, int, int], list[ShipId]] = {}
        self.ship_rects = []
        empire = self.galaxy.empires[self.empire_id]
        for ship_id in empire.ships:
            ship = self.galaxy.ships[ship_id]
            ship_image = self.images["ship"]
            if system_id := ship.orbit:
                system = self.galaxy.systems[system_id]
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
            else:  # Ship is in space with a destination
                ship_coord = ship.location

            if ship.destination:
                mid_pos = ship_coord + pygame.Vector2(ship_image.get_size()[0] / 2, ship_image.get_size()[1] / 2)
                destination = self.galaxy.systems[ship.destination]
                pygame.draw.line(
                    self.screen,
                    "purple",
                    mid_pos,
                    destination.position,
                )

            try:
                r = self.screen.blit(ship_image, ship_coord)
            except TypeError:
                print(f"{ship_id=} {ship_image=} {ship_coord=}")
                raise
            rect_tuple = (r.x, r.y, r.h, r.w)
            if rect_tuple not in rects:
                rects[rect_tuple] = [ship_id]
            else:
                rects[rect_tuple].append(ship_id)
            pygame.draw.rect(self.screen, "purple", r, width=1)
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
        empire = self.galaxy.empires[self.empire_id]
        food = empire.food()
        top_left = pygame.Vector2(580, 250)
        rp_text_surface = self.text_font.render(f"{food}", True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)

    #####################################################################################################
    def draw_income(self):
        """Draw money / income"""
        top_left = pygame.Vector2(555, 92)
        empire = self.galaxy.empires[self.empire_id]
        rp_text_surface = self.text_font.render(f"{empire.money} BC", True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)
        top_left.y += rp_text_surface.get_size()[1]
        if empire.income < 0:
            income_str = f"-{empire.income} BC"
        else:
            income_str = f"+{empire.income} BC"
        rp_text_surface = self.text_font.render(income_str, True, "white", "black")
        self.screen.blit(rp_text_surface, top_left)

    #####################################################################################################
    def draw_research(self):
        """Draw what is being researched"""
        top_left = pygame.Vector2(550, 380)
        empire = self.galaxy.empires[self.empire_id]

        if not empire.researching:
            rp_text_surface = self.text_font.render("Nothing", True, "white", "black")
            self.screen.blit(rp_text_surface, top_left)
            return

        research = get_research(empire.researching)
        try:
            time_left = int((research.cost - empire.research_spent) / empire.get_research_points())
        except ZeroDivisionError:
            time_left = 10000

        words = [
            research.name,
            f"~{time_left} turns",
            f"{empire.get_research_points()} RP",
        ]

        for word in words:
            rp_text_surface = self.text_font.render(word, True, "white", "black")
            self.screen.blit(rp_text_surface, top_left)
            top_left.y += rp_text_surface.get_size()[1]

    #####################################################################################################
    def system_colour(self, system_id: SystemId) -> str:
        colours = []
        system = self.galaxy.systems[system_id]
        for planet_id in system:
            if not planet_id:
                continue
            planet = self.galaxy.planets[planet_id]
            if planet.owner:
                colour = self.galaxy.empires[planet.owner].colour
                colours.append(colour)
        return colours[0] if colours else "grey"

    #####################################################################################################
    def draw_galaxy_view_system(self, system_id: SystemId):
        system = self.galaxy.systems[system_id]
        sys_coord = system.position
        star_image = self.images[f"small_{system.colour.name.lower()}_star"]
        img_size = star_image.get_size()
        img_coord = pygame.Vector2(sys_coord[0] - img_size[0] / 2, sys_coord[1] - img_size[1] / 2)
        planet_rect = self.screen.blit(star_image, img_coord)
        pygame.draw.rect(self.screen, "purple", planet_rect, width=1)
        self.system_rects.append((planet_rect, system_id))

        empire = self.galaxy.empires[self.empire_id]
        if empire.is_known_system(system_id):
            colour = self.system_colour(system_id)
            text_surface = self.label_font.render(f"{system.name}", True, colour)
        else:
            text_surface = self.label_font.render(f"{system.id} @ {sys_coord}", True, "purple")
        text_size = text_surface.get_size()
        text_coord = (sys_coord[0] - text_size[0] / 2, sys_coord[1] + img_size[1] / 2)
        self.screen.blit(text_surface, text_coord)


#####################################################################################################
def load_images() -> dict[str, pygame.surface.Surface]:
    """Load all the images from disk"""
    start = time.time()
    images = {}
    images["base_window"] = load_image("BUFFER0.LBX", 0)
    images["star_bg"] = load_image("STARBG.LBX", 0, palette_index=2)
    for neb in range(6, 52):
        try:
            images[f"nebula_{neb}"] = load_image("STARBG.LBX", neb)
        except IndexError:
            pass

    images["small_blue_star"] = load_image("BUFFER0.LBX", 149)
    images["small_white_star"] = load_image("BUFFER0.LBX", 155)
    images["small_yellow_star"] = load_image("BUFFER0.LBX", 161)
    images["small_orange_star"] = load_image("BUFFER0.LBX", 167)
    images["small_red_star"] = load_image("BUFFER0.LBX", 173)
    images["small_brown_star"] = load_image("BUFFER0.LBX", 179)
    images["ship"] = load_image("BUFFER0.LBX", 205)
    images["turn_button"] = load_image("BUFFER0.LBX", 2)
    images["colonies_button"] = load_image("BUFFER0.LBX", 3)
    images["planets_button"] = load_image("BUFFER0.LBX", 4)

    end = time.time()
    print(f"Main: Loaded {len(images)} in {end-start} seconds")

    return images


#####################################################################################################
def main():
    g = Game(1)
    g.loop()
    pygame.quit()


#####################################################################################################
if __name__ == "__main__":
    main()

# EOF
