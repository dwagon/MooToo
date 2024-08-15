""" Popup window with ships"""

import time
from typing import TYPE_CHECKING
import pygame
from MooToo.ui.proxy.proxy_util import get_distance_tuple
from .base_graphics import BaseGraphics, load_image
from .gui_button import Button, InvisButton
from ..utils import SystemId, ShipId

if TYPE_CHECKING:
    from MooToo.ui.game import Game

ALL_OFFSET = pygame.Vector2(18, 206)
CLOSE_OFFSET = pygame.Vector2(0, 238)
TITLE_OFFSET = pygame.Vector2(195, 35)


#####################################################################################################
#####################################################################################################
class FleetWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.ship_ids: list[ShipId] = []
        self.images = self.load_images()
        self.reset([])

    #####################################################################################################
    def reset(self, ships: list[ShipId]):
        self.top_left = pygame.Vector2(640 / 2 - self.images["top_window"].get_size()[0] / 2, 100)
        self.all_button = Button(self.images["all_button"], self.top_left + ALL_OFFSET)
        self.close_button = Button(self.images["close_button"], self.top_left + CLOSE_OFFSET)
        self.title_bar = InvisButton(pygame.Rect(self.top_left.x, self.top_left.y, TITLE_OFFSET.x, TITLE_OFFSET.y))
        self.ship_ids = ships
        self.selected_ships = set(self.ship_ids)
        self.ship_rects = []
        self.selected = False

    #####################################################################################################
    def button_up(self):
        self.selected = False

    #####################################################################################################
    def button_left_down(self) -> bool:
        if self.close_button.clicked():
            return True
        if self.title_bar.clicked():
            self.selected = True
            return False
        # Selecting a ship in the fleet window
        mouse = pygame.mouse.get_pos()
        for rect, ship in self.ship_rects:
            if rect.collidepoint(mouse[0], mouse[1]):
                if ship in self.selected_ships:
                    self.selected_ships.remove(ship)
                else:
                    self.selected_ships.add(ship)
        # Clicking the "All" button
        if self.all_button.clicked():
            if len(self.selected_ships) < len(self.ship_ids):
                self.selected_ships = set(self.ship_ids)
            else:
                self.selected_ships = set()
        return False

    #####################################################################################################
    def select_destination(self, dest_system: SystemId):
        """Tell ships to move to selected system"""
        for ship_id in self.selected_ships:
            ship = self.game.galaxy.ships[ship_id]
            ship.set_destination(dest_system)

    #####################################################################################################
    def mouse_pos(self, event: pygame.event):
        if not self.selected:
            return
        self.top_left = pygame.Vector2(event.pos[0], event.pos[1])
        self.all_button.move(self.top_left + ALL_OFFSET)
        self.close_button.move(self.top_left + CLOSE_OFFSET)
        self.title_bar.move(self.top_left + TITLE_OFFSET)

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        start = time.time()
        images["top_window"] = load_image("BUFFER0.LBX", 52)
        images["middle_window"] = load_image("BUFFER0.LBX", 54)
        images["bottom_window"] = load_image("BUFFER0.LBX", 56)
        for num, idx in enumerate(range(8)):
            images[f"frigate_{num}"] = load_image("SHIPS.LBX", idx, palette_index=2)
        for num, idx in enumerate(range(8, 16)):
            images[f"destroyer_{num}"] = load_image("SHIPS.LBX", idx, palette_index=2)
        for num, idx in enumerate(range(16, 24)):
            images[f"cruiser_{num}"] = load_image("SHIPS.LBX", idx, palette_index=2)
        for num, idx in enumerate(range(24, 32)):
            images[f"battleship_{num}"] = load_image("SHIPS.LBX", idx, palette_index=2)
        for num, idx in enumerate(range(32, 40)):
            images[f"titan_{num}"] = load_image("SHIPS.LBX", idx, palette_index=2)
        for num, idx in enumerate(range(40, 44)):
            images[f"doomstar_{num}"] = load_image("SHIPS.LBX", idx, palette_index=2)
        images["guardian"] = load_image("SHIPS.LBX", 44, palette_index=2)
        images["colony"] = load_image("SHIPS.LBX", 45, palette_index=2)
        images["outpost"] = load_image("SHIPS.LBX", 46, palette_index=2)
        images["transport"] = load_image("SHIPS.LBX", 47, palette_index=2)
        images["freighter"] = load_image("SHIPS.LBX", 48, palette_index=2)
        images["close_button"] = load_image("BUFFER0.LBX", 72)
        images["blue_bg"] = load_image("BUFFER0.LBX", 11)
        images["all_button"] = load_image("BUFFER0.LBX", 60)

        end = time.time()
        print(f"ShipUIs: Loaded {len(images)} in {end-start} seconds")

        return images

    #####################################################################################################
    def draw(self):
        self.ship_rects = []
        v = pygame.Vector2(self.top_left.x, self.top_left.y)
        self.screen.blit(self.images["top_window"], v)
        text_surface = self.text_font.render(f"{self.game.empire_id.name}'s Fleet", True, "white")
        self.screen.blit(text_surface, pygame.Vector2(v.x + 15, v.y + 13))
        v.y += self.images["top_window"].get_size()[1]
        ship_display_top_left = pygame.Vector2(v.x, v.y)
        self.screen.blit(self.images["middle_window"], v)
        v.y += self.images["middle_window"].get_size()[1]
        self.screen.blit(self.images["bottom_window"], v)
        v.y += self.images["bottom_window"].get_size()[1]
        ship = self.game.galaxy.ships[self.ship_ids[0]]
        if dest := ship.destination:
            turns = int(get_distance_tuple(dest.position, ship.location) / ship.speed())
            distance_surface = self.text_font.render(f"{turns} turns", True, "white")
            self.screen.blit(distance_surface, pygame.Vector2(v.x + 70, v.y - 28))

        for index, ship_id in enumerate(self.ship_ids):
            v_idx = index // 3
            h_idx = index % 3
            self.draw_ship(ship_id, h_idx, v_idx, ship_display_top_left)

        self.screen.blit(self.images["close_button"], v)
        self.all_button.draw(self.screen)
        self.close_button.draw(self.screen)

    #####################################################################################################
    def draw_ship(self, ship_id: ShipId, h_idx: int, v_idx: int, top_left: pygame.Vector2):
        ship_top_left = top_left + pygame.Vector2(16 + h_idx * 58, 3 + v_idx * 56)
        ship = self.game.galaxy.ships[ship_id]
        if ship_id in self.selected_ships:
            self.screen.blit(self.images["blue_bg"], ship_top_left)
        rect = self.screen.blit(self.images[ship.icon], ship_top_left)
        self.ship_rects.append((rect, ship_id))


# EOF
