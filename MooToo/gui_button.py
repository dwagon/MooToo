import pygame


#####################################################################################################
class Button:
    def __init__(
        self,
        image: pygame.Surface,
        tl_point: pygame.Vector2,
    ):
        self.image = image
        self.size = self.image.get_size()
        self.rect = pygame.Rect(tl_point[0], tl_point[1], self.size[0], self.size[1])

    #####################################################################################################
    def draw(self, surface) -> None:
        surface.blit(self.image, self.rect)

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
