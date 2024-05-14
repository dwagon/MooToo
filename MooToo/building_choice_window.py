""" Select what to build next"""

import pygame
from MooToo.base_graphics import BaseGraphics
from MooToo.config import Config
from MooToo.planet import Planet
from MooToo.gui_button import Button


#####################################################################################################
#####################################################################################################
class BuildingChoiceWindow(BaseGraphics):
    def __init__(self, screen: pygame.Surface, config: Config):
        super().__init__(config)
        self.screen = screen
        self.planet = None
        self.images = self.load_images()
        self.ok_button = Button(self.load_image("COLBLDG.LBX", 3), pygame.Vector2(564, 450))
        self.cancel_button = Button(self.load_image("COLBLDG.LBX", 1), pygame.Vector2(495, 450))
        self.to_build_rects: dict[str, pygame.Rect] = {}

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.Surface]:
        images = {}
        images["window"] = self.load_image("COLBLDG.LBX", 0, palette_index=2)
        return images

    #####################################################################################################
    def draw(self, planet: Planet):
        self.planet = planet
        self.draw_centered_image(self.images["window"])
        self.draw_currently_building()
        self.draw_available_buildings()
        self.draw_building_queue()

    #####################################################################################################
    def draw_currently_building(self) -> None:
        if not self.planet.build_queue:
            return
        top_left = pygame.Vector2(205, 10)
        building = self.planet.build_queue[0]
        for word in building.name.split():
            text = self.text_font.render(word, True, "purple")
            self.screen.blit(text, top_left)
            top_left.y += text.get_size()[1]

    #####################################################################################################
    def draw_available_buildings(self) -> None:
        buildings = list(self.planet.buildings_available.keys())
        if not buildings:
            buildings = self.planet.available_to_build()

        top_left = pygame.Vector2(12, 12)
        for building in sorted(buildings):
            text = self.text_font.render(building, True, "white")
            rect = self.screen.blit(text, top_left)
            top_left.y += text.get_size()[1]
            self.to_build_rects[building] = rect

    #####################################################################################################
    def draw_building_queue(self) -> None:
        top_left = pygame.Vector2(209, 330)

        for bld in self.planet.build_queue:
            text = self.text_font.render(bld.name, True, "white")
            self.screen.blit(text, top_left)
            top_left.y += 20

    #####################################################################################################
    def button_left_down(self) -> bool:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for name, rect in self.to_build_rects.items():
            if rect.collidepoint(mouse_x, mouse_y):
                self.planet.toggle_build_queue_by_name(name)
        if self.ok_button.clicked():
            return True
        if self.cancel_button.clicked():
            return True
        return False
