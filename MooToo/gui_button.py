import pygame


#####################################################################################################
class BaseButton:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect

    #####################################################################################################
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, "purple", self.rect, width=1)

    #####################################################################################################
    def clicked(self) -> bool:
        mouse = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse[0], mouse[1])

    #####################################################################################################
    def move(self, top_left: pygame.Vector2) -> None:
        self.rect = pygame.Rect(top_left.x, top_left.y, self.rect.width, self.rect.height)


#####################################################################################################
class Button(BaseButton):
    def __init__(self, image: pygame.Surface, tl_point: pygame.Vector2):
        self.image = image
        self.size = self.image.get_size()
        self.rect = pygame.Rect(tl_point[0], tl_point[1], self.size[0], self.size[1])
        super().__init__(self.rect)

    #####################################################################################################
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


#####################################################################################################
class InvisButton(BaseButton):
    """A click sensitive area that doesn't have any graphics"""

    def __init__(self, rect: pygame.Rect):
        super().__init__(rect)
        self.rect = rect
