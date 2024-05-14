""" Class to base all other pygame classes from"""

import pygame
from MooToo.lbx_image import LBXImage
from MooToo.config import Config


#####################################################################################################
IMAGE_CACHE: dict[tuple[str, int], pygame.Surface] = {}


#####################################################################################################
#####################################################################################################
class BaseGraphics:
    def __init__(self, config: Config):
        self.config = config
        pygame.init()
        self.label_font = pygame.font.SysFont("Ariel", 14)
        self.text_font = pygame.font.SysFont("Ariel", 18)
        self.title_font = pygame.font.SysFont("Ariel", 24)
        self.screen = pygame.display.set_mode((640, 480), flags=pygame.SCALED)
        self.size = self.screen.get_size()
        self.mid_point = pygame.Vector2(self.size[0] / 2, self.size[1] / 2)
        self.clock = pygame.time.Clock()

    #####################################################################################################
    def top_left(self, image: pygame.Surface, center: pygame.Vector2) -> pygame.Vector2:
        """Return the top left coords of an image around the center
        If you want to draw an image in the center you need the top left coords
        """
        img_size = image.get_size()
        return pygame.Vector2(center[0] - img_size[0] / 2, center[1] - img_size[1] / 2)

    #####################################################################################################
    def load_image(
        self, lbx_file: str, lbx_index: int, frame: int = 0, palette_file="FONTS.LBX", palette_index=1
    ) -> pygame.Surface:
        img_key = (lbx_file, lbx_index)
        if img_key not in IMAGE_CACHE:
            pil_image = LBXImage(
                lbx_file, lbx_index, self.config["moo_path"], frame, palette_file, palette_index
            ).png_image()
            IMAGE_CACHE[img_key] = pygame.image.load(pil_image, "_.png")
        return IMAGE_CACHE[img_key]

    #####################################################################################################
    def draw_centered_image(self, image: pygame.Surface) -> pygame.Rect:
        tl = self.top_left(image, self.mid_point)
        return self.screen.blit(image, tl)
