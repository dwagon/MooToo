""" PlanetUI Summary Window"""

import time
from typing import TYPE_CHECKING, Any, Optional
from enum import StrEnum, auto
import pygame

from MooToo.constants import FOOD_CLIMATE_MAP, GRAVITY_MAP, PROD_RICHNESS_MAP
from .base_graphics import BaseGraphics, load_image
from .constants import DisplayMode
from .gui_button import Button
from ..utils import PlanetId, EmpireId

if TYPE_CHECKING:
    from .game import Game


#####################################################################################################
class PlanetDataColumn(StrEnum):
    NAME = auto()
    CLIMATE = auto()
    GRAVITY = auto()
    MINERALS = auto()
    SIZE = auto()
    PLANET_ID = auto()
    COLONISER_EN_ROUTE = auto()
    MAX_POP = auto()


#####################################################################################################
class SummaryButtons(StrEnum):
    RETURN = auto()
    CLIMATE = auto()
    MINERALS = auto()
    SIZE = auto()
    NO_ENEMY = auto()
    GRAVITY = auto()
    HOSTILE = auto()
    ABUNDANCE = auto()
    IN_RANGE = auto()
    SEND_COLONY = auto()
    SEND_OUTPOST = auto()
    UP = auto()
    DOWN = auto()


#####################################################################################################
#####################################################################################################
class PlanetSummaryWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game", empire_id: EmpireId):
        super().__init__(game)
        self.screen = screen
        self.empire_id = empire_id
        self.data = []
        self.images = load_images()
        self.sorting = PlanetDataColumn.NAME
        self.planet_clicked: Optional[PlanetId] = None
        self.button_clicked: Optional[SummaryButtons] = None
        self.planet_rects: dict[PlanetId, pygame.Rect] = {}
        self.buttons = {
            SummaryButtons.CLIMATE: Button(self.images["climate_button"], pygame.Vector2(441, 201)),
            SummaryButtons.RETURN: Button(self.images["return_button"], pygame.Vector2(454, 440)),
            SummaryButtons.MINERALS: Button(self.images["minerals_button"], pygame.Vector2(502, 201)),
            SummaryButtons.SIZE: Button(self.images["size_button"], pygame.Vector2(567, 201)),
            SummaryButtons.NO_ENEMY: Button(
                self.images["no_enemy_button"],
                pygame.Vector2(440, 266),
            ),
            SummaryButtons.GRAVITY: Button(
                self.images["normal_gravity_button"],
                pygame.Vector2(440, 289),
            ),
            SummaryButtons.HOSTILE: Button(
                self.images["non_hostile_button"],
                pygame.Vector2(440, 311),
            ),
            SummaryButtons.ABUNDANCE: Button(
                self.images["abundance_button"],
                pygame.Vector2(440, 335),
            ),
            SummaryButtons.IN_RANGE: Button(
                self.images["in_range_button"],
                pygame.Vector2(440, 358),
            ),
            # SummaryButtons.SEND_COLONY: Button(self.images["send_colony_button_disabled"], pygame.Vector2(454, 385)),
            SummaryButtons.SEND_OUTPOST: Button(
                self.images["send_outpost_button_disabled"],
                pygame.Vector2(454, 413),
            ),
            SummaryButtons.UP: Button(self.images["up_button"], pygame.Vector2(420, 15)),
            SummaryButtons.DOWN: Button(self.images["down_button"], pygame.Vector2(420, 448)),
        }

    #####################################################################################################
    def draw(self):
        """Draw the window"""
        self.screen.blit(self.images["window"], pygame.Vector2(0, 0))
        for button in self.buttons.values():
            button.draw(self.screen)
        top_left = pygame.Vector2(20, 39)
        self.data.sort(key=lambda x: x[self.sorting])

        for planet_data in self.data:
            self.draw_planet(planet_data, top_left)
            rect = pygame.Rect(top_left.x, top_left.y, 400, 48)
            pygame.draw.rect(self.screen, "purple", rect, width=1)
            self.planet_rects[planet_data[PlanetDataColumn.PLANET_ID]] = rect
            top_left += pygame.Vector2(0, 54)

    #####################################################################################################
    def draw_planet(self, planet_data: dict[PlanetDataColumn, Any], top_left: pygame.Vector2):
        highlight = self.planet_clicked == planet_data[PlanetDataColumn.PLANET_ID]

        tl = top_left.copy()
        self.draw_text(planet_data[PlanetDataColumn.NAME], tl, highlight)

        if planet_data[PlanetDataColumn.COLONISER_EN_ROUTE]:
            self.screen.blit(self.images["colony_ship"], tl + pygame.Vector2(71, 38))

        tl += pygame.Vector2(92, 0)
        food = FOOD_CLIMATE_MAP[planet_data[PlanetDataColumn.CLIMATE]]
        self.draw_text(planet_data[PlanetDataColumn.CLIMATE], tl, highlight, f"{food} Food")

        tl += pygame.Vector2(75, 0)
        grav = GRAVITY_MAP[planet_data[PlanetDataColumn.GRAVITY]]
        self.draw_text(planet_data[PlanetDataColumn.GRAVITY], tl, highlight, f"{display_percent(grav)} prod")

        tl += pygame.Vector2(90, 0)
        prod = PROD_RICHNESS_MAP[planet_data[PlanetDataColumn.MINERALS]]
        self.draw_text(planet_data[PlanetDataColumn.MINERALS], tl, highlight, f"{prod} prod/worker")

        tl += pygame.Vector2(90, 0)
        max_pop = planet_data[PlanetDataColumn.MAX_POP]
        self.draw_text(planet_data[PlanetDataColumn.SIZE], tl, highlight, f"{max_pop} max pop")

    #####################################################################################################
    def draw_text(self, text: str, top_left: pygame.Vector2, highlight: bool = False, subtext: str = "") -> None:
        if highlight:
            big_font = self.text_font_bold
            small_font = self.label_font_bold
        else:
            big_font = self.text_font
            small_font = self.label_font

        text_surface = big_font.render(text, True, "white", "black")
        self.screen.blit(text_surface, top_left)
        if subtext:
            text_surface = small_font.render(subtext, True, "white", "black")
            self.screen.blit(text_surface, top_left + pygame.Vector2(0, text_surface.get_size()[1] + 1))

    #####################################################################################################
    def define_colony_button(self) -> None:
        colony_button_location = pygame.Vector2(454, 385)
        if self.has_colony_ship_available():
            self.buttons[SummaryButtons.SEND_COLONY] = Button(
                self.images["send_colony_button_enabled"], colony_button_location
            )

        else:
            self.buttons[SummaryButtons.SEND_COLONY] = Button(
                self.images["send_colony_button_disabled"], colony_button_location
            )

    #####################################################################################################
    def collect_data(self) -> list[dict[PlanetDataColumn, Any]]:
        """Gather all the information required"""
        self.define_colony_button()
        data = []
        empire = self.game.galaxy.empires[self.empire_id]
        for system_id in empire.known_systems:
            system = self.game.galaxy.systems[system_id]
            for planet_id in system.orbits:
                if not planet_id:
                    continue
                planet = self.game.galaxy.planets[planet_id]
                if planet.owner:
                    continue

                planet_data = {
                    PlanetDataColumn.NAME: planet.name,
                    PlanetDataColumn.CLIMATE: planet.climate,
                    PlanetDataColumn.GRAVITY: planet.gravity,
                    PlanetDataColumn.MINERALS: planet.richness,
                    PlanetDataColumn.SIZE: planet.size,
                    PlanetDataColumn.PLANET_ID: planet_id,
                    PlanetDataColumn.COLONISER_EN_ROUTE: self.has_coloniser_en_route(planet_id),
                    PlanetDataColumn.MAX_POP: planet.max_population(),
                }
                data.append(planet_data)
        return data

    #####################################################################################################
    def has_coloniser_en_route(self, planet_id: PlanetId) -> bool:
        empire = self.game.galaxy.empires[self.empire_id]
        for ship_id in empire.ships:
            ship = self.game.galaxy.ships[ship_id]
            if ship.coloniser and ship.target_planet_id == planet_id:
                return True
        return False

    #####################################################################################################
    def has_colony_ship_available(self) -> bool:
        """Does the empire have a colony ship"""
        empire = self.game.galaxy.empires[self.empire_id]
        for ship_id in empire.ships:
            ship = self.game.galaxy.ships[ship_id]
            if ship.coloniser and not ship.destination:
                return True
        return False

    #####################################################################################################
    def loop(self) -> DisplayMode:
        self.display_mode = DisplayMode.PLANET_SUM
        self.data = self.collect_data()
        while True:
            self.event_loop()

            match self.display_mode:
                case DisplayMode.PLANET_SUM:
                    pass
                case _:
                    return self.display_mode

    #####################################################################################################
    def button_left_down(self):
        if self.buttons[SummaryButtons.SIZE].clicked():
            self.sorting = PlanetDataColumn.SIZE
        elif self.buttons[SummaryButtons.GRAVITY].clicked():
            self.sorting = PlanetDataColumn.GRAVITY
        elif self.buttons[SummaryButtons.CLIMATE].clicked():
            self.sorting = PlanetDataColumn.CLIMATE
        elif self.buttons[SummaryButtons.MINERALS].clicked():
            self.sorting = PlanetDataColumn.MINERALS
        elif self.buttons[SummaryButtons.SEND_COLONY].clicked():
            self.button_clicked = SummaryButtons.SEND_COLONY
        elif self.buttons[SummaryButtons.RETURN].clicked():
            self.display_mode = DisplayMode.GALAXY
            return
        else:
            mouse = pygame.mouse.get_pos()
            for planet_id, rect in self.planet_rects.items():
                if rect.collidepoint(mouse):
                    if self.planet_clicked == planet_id:
                        self.planet_clicked = None
                    else:
                        self.planet_clicked = planet_id

        if self.planet_clicked and self.button_clicked:
            if self.button_clicked == SummaryButtons.SEND_COLONY:
                empire = self.game.galaxy.empires[self.empire_id]
                empire.send_coloniser(self.planet_clicked)
                self.planet_clicked = None
                self.button_clicked = None
                self.data = self.collect_data()


#####################################################################################################
def display_percent(num: float) -> str:
    if num < 1.0:
        frac = int(100 - num * 100)
        return f"-{frac} %"
    elif num > 1.0:
        frac = int(100 + num * 100)
        return f"+{frac} %"
    else:
        return "100%"


#####################################################################################################
def load_images() -> dict[str, pygame.Surface]:
    images = {}
    start = time.time()
    images["window"] = load_image("PLNTSUM.LBX", 0, palette_index=7)
    images["climate_button"] = load_image("PLNTSUM.LBX", 1, palette_index=7)
    images["minerals_button"] = load_image("PLNTSUM.LBX", 2, palette_index=7)
    images["size_button"] = load_image("PLNTSUM.LBX", 3, palette_index=7)
    images["no_enemy_button"] = load_image("PLNTSUM.LBX", 4, palette_index=7)
    images["normal_gravity_button"] = load_image("PLNTSUM.LBX", 5, palette_index=7)
    images["non_hostile_button"] = load_image("PLNTSUM.LBX", 6, palette_index=7)
    images["abundance_button"] = load_image("PLNTSUM.LBX", 7, palette_index=7)
    images["in_range_button"] = load_image("PLNTSUM.LBX", 8, palette_index=7)
    images["send_colony_button_disabled"] = load_image("PLNTSUM.LBX", 9, palette_index=7)
    images["send_colony_button_enabled"] = load_image("PLNTSUM.LBX", 9, palette_index=7, frame=2)
    images["send_outpost_button_disabled"] = load_image("PLNTSUM.LBX", 10, palette_index=7)
    images["send_outpost_button_enabled"] = load_image("PLNTSUM.LBX", 10, palette_index=7, frame=2)
    images["up_button"] = load_image("PLNTSUM.LBX", 11, palette_index=7)
    images["down_button"] = load_image("PLNTSUM.LBX", 12, palette_index=7)
    images["return_button"] = load_image("PLNTSUM.LBX", 14, palette_index=7)
    images["colony_ship"] = load_image("PLNTSUM.LBX", 76, palette_index=7)

    end = time.time()
    print(f"PlanetSummary: Loaded {len(images)} in {end-start} seconds")
    return images


# EOF
