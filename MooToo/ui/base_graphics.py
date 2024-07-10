""" Class to base all other pygame classes from"""

import pygame
from MooToo.ui.lbx_image import LBXImage
from MooToo.ui.constants import DisplayMode
from MooToo.constants import MOO_PATH


#####################################################################################################
IMAGE_CACHE: dict[tuple[str, int, int], pygame.Surface] = {}


#####################################################################################################
#####################################################################################################
class BaseGraphics:
    def __init__(self, game: "Game"):
        self.game = game
        pygame.init()
        self.label_font = pygame.font.SysFont("Ariel", 14)
        self.label_font_bold = pygame.font.SysFont("Ariel", 14, bold=True)

        self.text_font = pygame.font.SysFont("Ariel", 18)
        self.text_font_bold = pygame.font.SysFont("Ariel", 18, bold=True)

        self.title_font = pygame.font.SysFont("Ariel", 24)
        self.screen = pygame.display.set_mode((640, 480), flags=pygame.SCALED)
        self.size = self.screen.get_size()
        self.mid_point = pygame.Vector2(self.size[0] / 2, self.size[1] / 2)
        self.clock = pygame.time.Clock()
        self.display_mode = DisplayMode.GALAXY

    #####################################################################################################
    def top_left(self, image: pygame.Surface, center: pygame.Vector2) -> pygame.Vector2:
        """Return the top left coords of an image around the center
        If you want to draw an image in the center you need the top left coords
        """
        img_size = image.get_size()
        return pygame.Vector2(center[0] - img_size[0] / 2, center[1] - img_size[1] / 2)

    #####################################################################################################
    def draw_centered_image(self, image: pygame.Surface) -> pygame.Rect:
        tl = self.top_left(image, self.mid_point)
        return self.screen.blit(image, tl)

    #####################################################################################################
    def debug_text(self, value: int, top_left: pygame.Vector2) -> pygame.Rect:
        out_string = f"{value}"  # DBG
        text_rect = self.text_font.render(out_string, True, "purple")
        return self.screen.blit(text_rect, top_left)

    #####################################################################################################
    def draw_population_sequence(
        self, top_left: pygame.Vector2, worker_image: pygame.Surface, value: int, max_width=200
    ) -> list[pygame.Rect]:
        """Display a sequence of population images"""
        delta = worker_image.get_size()[0]
        total_width = delta * value
        if total_width > max_width:
            delta = max_width / value
        rects = []
        for _ in range(value):
            rect = self.screen.blit(worker_image, top_left)
            pygame.draw.rect(self.screen, "purple", rect, width=1)  # DBG
            top_left.x += delta
            rects.append(rect)
        return rects

    #####################################################################################################
    def draw(self):
        raise NotImplemented

    #####################################################################################################
    def button_left_down(self) -> None:
        raise NotImplemented

    #####################################################################################################
    def button_right_down(self) -> None:
        raise NotImplemented

    #####################################################################################################
    def button_up(self) -> None:
        raise NotImplemented

    #####################################################################################################
    def mouse_pos(self, event: pygame.event):
        raise NotImplemented

    #####################################################################################################
    def event_loop(self) -> None:
        self.screen.fill("black")
        self.draw()
        pygame.display.flip()
        self.clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(1)
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


#####################################################################################################
def load_image(
    lbx_file: str, lbx_index: int, frame: int = 0, palette_file="FONTS.LBX", palette_index=1
) -> pygame.Surface:
    img_key = (lbx_file, lbx_index, frame)
    if img_key not in IMAGE_CACHE:
        pil_image = LBXImage(lbx_file, lbx_index, MOO_PATH, frame, palette_file, palette_index).png_image()
        IMAGE_CACHE[img_key] = pygame.image.load(pil_image, "_.png")
    return IMAGE_CACHE[img_key]


# EOF
