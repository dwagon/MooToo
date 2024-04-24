import pygame


#####################################################################################################
class Button:
    def __init__(
        self,
        surface: pygame.surface.Surface,
        text: str,
        tl_point: pygame.Vector2 | None = None,
        br_point: pygame.Vector2 | None = None,
        color="red",
        font="Ariel",
        font_size=24,
    ):
        self.surface = surface
        self.text = text
        self.tl_point = tl_point
        self.br_point = br_point
        self.color = color
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(self.text, True, self.color)
        text_size = self.text_surface.get_size()
        if self.tl_point:
            self.rect = pygame.Rect(self.tl_point[0], self.tl_point[1], text_size[0], text_size[1])
        elif self.br_point:
            self.rect = pygame.Rect(
                self.br_point[0] - text_size[0],
                self.br_point[1] - text_size[1],
                text_size[0],
                text_size[1],
            )
        else:
            raise NotImplemented

    #####################################################################################################
    def draw(self) -> None:

        pygame.draw.rect(
            self.surface,
            "white",
            self.rect,
        )
        self.surface.blit(self.text_surface, self.rect)

    #####################################################################################################
    def clicked(self) -> bool:
        mouse = pygame.mouse.get_pos()
        if mouse[0] < self.rect.left:
            return False
        if mouse[0] > self.rect.right:
            return False
        if mouse[1] < self.rect.top:
            return False
        if mouse[1] > self.rect.bottom:
            return False
        return True
