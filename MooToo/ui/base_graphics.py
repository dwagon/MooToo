""" Class to base all other pygame classes from"""

import pygame
from .lbx_image import LBXImage
from MooToo.constants import MOO_PATH
from .constants import DisplayMode


#####################################################################################################
IMAGE_CACHE: dict[tuple[str, int, int], pygame.Surface] = {}


#####################################################################################################
#####################################################################################################
class BaseGraphics:
    def __init__(self, game: "Game"):
        self.game = game
        self.galaxy = self.game.galaxy
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
        pass

    #####################################################################################################
    def button_right_down(self) -> None:
        pass

    #####################################################################################################
    def button_up(self) -> None:
        pass

    #####################################################################################################
    def mouse_pos(self, event: pygame.event):
        pass

    #####################################################################################################
    def event_loop(self) -> None:
        self.screen.fill("black")
        self.draw()

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

        pygame.display.flip()
        self.clock.tick(60)


#####################################################################################################
# Taken from https://codereview.stackexchange.com/a/70206
class Point:
    # constructed using a normal tuple
    def __init__(self, point_t=(0, 0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])

    # define all useful operators
    def __add__(self, other: Self) -> Self:
        return Point((self.x + other.x, self.y + other.y))

    def __sub__(self, other: Self) -> Self:
        return Point((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar: Any) -> Self:
        return Point((self.x * scalar, self.y * scalar))

    def __truediv__(self, scalar: Any) -> Self:
        return Point((self.x / scalar, self.y / scalar))

    def __len__(self) -> int:
        return int(math.sqrt(self.x**2 + self.y**2))

    # get back values in original tuple format
    def get(self):
        return self.x, self.y


#####################################################################################################
def draw_dashed_line(surf, color, start_pos, end_pos, width=1, dash_length=10):
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    if length == 0:
        return
    slope = displacement / length

    for index in range(0, int(length / dash_length), 2):
        start = origin + (slope * index * dash_length)
        end = origin + (slope * (index + 1) * dash_length)
        pygame.draw.line(surf, color, start.get(), end.get(), width)


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
