import time
import pygame
from .base_graphics import BaseGraphics, load_image
from .gui_button import Button
from MooToo.constants import Technology
from MooToo.research import TechCategory


#####################################################################################################
#####################################################################################################
class ScienceWindow(BaseGraphics):
    """Window to select research"""

    def __init__(self, screen: pygame.Surface, game: "Game"):
        super().__init__(game)
        self.screen = screen
        self.images = self.load_images()
        self.research_rects: dict[tuple[float, float, float, float], Technology] = {}
        self.cancel_button = Button(load_image("TECHSEL.LBX", 27), pygame.Vector2(274, 453))

    #####################################################################################################
    def draw_category(self, category: TechCategory, top_left: pygame.Vector2, rp_place: pygame.Vector2) -> None:
        technologies = self.game.empire.next_research(category)

        rp_text_surface = self.text_font.render(f"{get_research(technologies[0]).cost} RP", True, "white")
        self.screen.blit(rp_text_surface, rp_place)
        for tech in technologies:
            research = get_research(tech)
            text_surface = self.text_font.render(research.name, True, "white")
            r = self.screen.blit(text_surface, top_left)
            top_left.y += text_surface.get_size()[1]
            self.research_rects[(r.left, r.top, r.width, r.height)] = research.tag
            pygame.draw.rect(self.screen, "purple", r, width=1)  # DBG

    #####################################################################################################
    def load_images(self) -> dict[str, pygame.surface.Surface]:
        start = time.time()
        images = {}
        images["window"] = load_image("TECHSEL.LBX", 14)
        end = time.time()
        print(f"Science: Loaded {len(images)} in {end-start} seconds")
        return images

    #####################################################################################################
    def draw(self):
        self.draw_centered_image(self.images["window"])
        self.draw_category(TechCategory.CONSTRUCTION, pygame.Vector2(115, 55), pygame.Vector2(254, 33))
        self.draw_category(TechCategory.POWER, pygame.Vector2(345, 55), pygame.Vector2(475, 33))
        self.draw_category(TechCategory.CHEMISTRY, pygame.Vector2(115, 155), pygame.Vector2(254, 133))
        self.draw_category(TechCategory.SOCIOLOGY, pygame.Vector2(345, 155), pygame.Vector2(475, 133))
        self.draw_category(TechCategory.COMPUTERS, pygame.Vector2(115, 260), pygame.Vector2(254, 243))
        self.draw_category(TechCategory.BIOLOGY, pygame.Vector2(345, 260), pygame.Vector2(475, 243))
        self.draw_category(TechCategory.PHYSICS, pygame.Vector2(115, 368), pygame.Vector2(254, 345))
        self.draw_category(TechCategory.FORCE_FIELDS, pygame.Vector2(345, 368), pygame.Vector2(475, 345))
        self.cancel_button.draw(self.screen)

    #####################################################################################################
    def button_left_down(self) -> bool:
        """ """
        if self.cancel_button.clicked():
            return True
        for sys_rect, tech in self.research_rects.items():
            r = pygame.Rect(sys_rect[0], sys_rect[1], sys_rect[2], sys_rect[3])
            if r.collidepoint(pygame.mouse.get_pos()):
                self.game.empire.start_researching(tech)
                return True
        return False
