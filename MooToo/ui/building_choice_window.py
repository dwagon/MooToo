""" Select what to build next"""

from typing import TYPE_CHECKING
import pygame
from MooToo.ui.base_graphics import BaseGraphics
from MooToo.planet import Planet
from MooToo.ui.gui_button import Button
from MooToo.ship import ShipType
from MooToo.constants import Building
from MooToo.utils import get_building

if TYPE_CHECKING:
    from MooToo.ui.game import Game


#####################################################################################################
#####################################################################################################
class BuildingChoiceWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.planet = None
        self.images = self.load_images()
        self.ok_button = Button(self.images["ok_button"], pygame.Vector2(564, 450))
        self.cancel_button = Button(self.images["cancel_button"], pygame.Vector2(495, 450))
        self.to_build_rects: dict[Building | ShipType, pygame.Rect] = {}
        self.build_queue_rects: dict[int, pygame.Rect] = {}

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        images["window"] = self.load_image("COLBLDG.LBX", 0, palette_index=2)
        images["ok_button"] = self.load_image("COLBLDG.LBX", 3)
        images["cancel_button"] = self.load_image("COLBLDG.LBX", 1)
        return images

    #####################################################################################################
    def draw(self, planet: Planet):
        self.planet = planet
        self.draw_centered_image(self.images["window"])
        self.draw_currently_building()
        self.draw_available_buildings()
        self.draw_available_ships()
        self.draw_building_queue()

    #####################################################################################################
    def draw_available_ships(self) -> None:
        """ """
        # Colony Base
        # Freighter Fleet
        # Colony Ship
        # Outpost Ship
        # Transport Ship
        # Ships
        top_left = pygame.Vector2(486, 14)
        for ship_type in list(ShipType):
            if self.planet.can_build_ship(ship_type):
                text_surface = self.text_font.render(ship_type.name, True, "white")
                rect = self.screen.blit(text_surface, top_left)
                top_left.y += text_surface.get_size()[1]
                self.to_build_rects[ship_type] = rect
                pygame.draw.rect(self.screen, "purple", rect, width=1)  # DBG

    #####################################################################################################
    def draw_currently_building(self) -> None:
        if not self.planet.build_queue:
            return
        top_left = pygame.Vector2(205, 10)
        construct = self.planet.build_queue[0]
        text = self.label_font.render(construct.name, True, "purple")
        self.screen.blit(text, top_left)

    #####################################################################################################
    def draw_available_buildings(self) -> None:
        buildings: dict[str, Building] = {get_building(_).name: _ for _ in self.planet.buildings_available}

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

        for num, construct in enumerate(self.planet.build_queue):
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
    def button_left_down(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for bld, rect in self.to_build_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                self.planet.build_queue.toggle(bld)
        for num, rect in self.build_queue_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                self.planet.build_queue.pop(num)
        if self.ok_button.clicked():
            return True
        if self.cancel_button.clicked():
            return True
        return False
