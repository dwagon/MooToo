from typing import Optional
import pygame


#####################################################################################################
class BaseButton:
    def __init__(self, rect: pygame.Rect, click_area: Optional[pygame.Rect] = None):
        self.rect = rect
        self.click_area = click_area or self.rect

    #####################################################################################################
    def clicked(self) -> bool:
        mouse = pygame.mouse.get_pos()
        return self.click_area.collidepoint(mouse[0], mouse[1])

    #####################################################################################################
    def move(self, top_left: pygame.Vector2) -> None:
        self.rect = pygame.Rect(top_left.x, top_left.y, self.rect.width, self.rect.height)


#####################################################################################################
class Button(BaseButton):
    def __init__(self, image: pygame.Surface, draw_top_left: pygame.Vector2, click_area: Optional[pygame.Rect] = None):
        self.image = image
        self.size = self.image.get_size()
        self.rect = pygame.Rect(draw_top_left[0], draw_top_left[1], self.size[0], self.size[1])

        super().__init__(self.rect, click_area)

    #####################################################################################################
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        pygame.draw.rect(surface, "purple", self.click_area, width=1)


#####################################################################################################
class InvisButton(BaseButton):
    """A click sensitive area that doesn't have any graphics"""

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)
        self.rect = rect

    #####################################################################################################
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "purple", self.click_area, width=1)


# EOF
