""" Select what to build next"""

from typing import TYPE_CHECKING, Optional
import pygame
from .base_graphics import BaseGraphics, load_image
from .gui_button import Button
from .constants import DisplayMode
from ..constants import Building
from ..construct import ConstructType
from ..ship import ShipType
from ..utils import get_building, PlanetId

if TYPE_CHECKING:
    from MooToo.ui.game import Game


#####################################################################################################
#####################################################################################################
class BuildingChoiceWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.planet_id: Optional[PlanetId] = None
        self.images = load_images()
        self.ok_button = Button(self.images["ok_button"], pygame.Vector2(564, 450))
        self.cancel_button = Button(self.images["cancel_button"], pygame.Vector2(495, 450))
        self.to_build_rects: dict[Building | ShipType | ConstructType, pygame.Rect] = {}
        self.build_queue_rects: dict[int, pygame.Rect] = {}

    #####################################################################################################
    def draw(self):
        self.draw_centered_image(self.images["window"])
        self.draw_currently_building()
        self.draw_available_buildings()
        self.draw_available_ships()
        self.draw_building_queue()

    #####################################################################################################
    def draw_available_ships(self) -> None:
        """Non-building construction"""
        top_left = pygame.Vector2(486, 14)
        planet = self.game.galaxy.planets[self.planet_id]
        if planet.can_build(ConstructType.FREIGHTER):
            top_left = self.build_freighter(top_left)
        for ship_type in ShipType:
            if planet.can_build_ship(ship_type):
                text_surface = self.text_font.render(ship_type.name, True, "white")
                rect = self.screen.blit(text_surface, top_left)
                top_left.y += text_surface.get_size()[1]
                self.to_build_rects[ship_type] = rect
                pygame.draw.rect(self.screen, "purple", rect, width=1)  # DBG
            else:
                text_surface = self.text_font.render(ship_type.name, True, "grey")
                self.screen.blit(text_surface, top_left)
                top_left.y += text_surface.get_size()[1]

    #####################################################################################################
    def build_freighter(self, top_left: pygame.Vector2):
        text_surface = self.text_font.render("Freighter", True, "white")
        rect = self.screen.blit(text_surface, top_left)
        top_left.y += text_surface.get_size()[1]
        self.to_build_rects[ConstructType.FREIGHTER] = rect
        pygame.draw.rect(self.screen, "purple", rect, width=1)  # DBG
        return top_left

    #####################################################################################################
    def draw_currently_building(self) -> None:
        planet = self.game.galaxy.planets[self.planet_id]
        if not planet.build_queue:
            return
        top_left = pygame.Vector2(205, 10)
        construct = planet.build_queue[0]
        text = self.label_font.render(construct.name, True, "purple")
        self.screen.blit(text, top_left)

    #####################################################################################################
    def draw_available_buildings(self) -> None:
        planet = self.game.galaxy.planets[self.planet_id]
        buildings: dict[str, Building] = {get_building(_).name: _ for _ in planet.available_to_build()}

        top_left = pygame.Vector2(12, 12)
        for building in sorted(buildings.keys()):
            text = self.text_font.render(building, True, "white")
            rect = self.screen.blit(text, top_left)
            top_left.y += text.get_size()[1]
            self.to_build_rects[buildings[building]] = rect
            pygame.draw.rect(self.screen, "purple", rect, width=1)  # DBG

    #####################################################################################################
    def draw_building_queue(self) -> None:
        top_left = pygame.Vector2(209, 330)
        planet = self.game.galaxy.planets[self.planet_id]
        for num, construct in enumerate(planet.build_queue):
            if isinstance(construct, Building):
                name = get_building(construct).name
            else:
                name = construct.name
            text = self.text_font.render(name, True, "white", "black")
            rect = self.screen.blit(text, top_left)
            pygame.draw.rect(self.screen, "purple", rect, width=1)  # DBG
            self.build_queue_rects[num] = rect
            top_left.y += 20

    #####################################################################################################
    def loop(self, planet_id: PlanetId) -> DisplayMode:
        self.planet_id = planet_id
        self.display_mode = DisplayMode.PLANET_BUILD
        while True:
            self.event_loop()

            match self.display_mode:
                case DisplayMode.PLANET_BUILD:
                    pass
                case _:
                    return self.display_mode

    #####################################################################################################
    def button_left_down(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        planet = self.game.galaxy.planets[self.planet_id]
        for con, rect in self.to_build_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                planet.build_queue.toggle(con)
        for num, rect in self.build_queue_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                planet.build_queue.pop(num)
        if self.ok_button.clicked():
            self.display_mode = DisplayMode.PLANET
        if self.cancel_button.clicked():
            self.display_mode = DisplayMode.PLANET


#####################################################################################################
def load_images() -> dict[str, pygame.Surface]:
    images = {}
    images["window"] = load_image("COLBLDG.LBX", 0, palette_index=2)
    images["ok_button"] = load_image("COLBLDG.LBX", 3)
    images["cancel_button"] = load_image("COLBLDG.LBX", 1)
    return images
