import pygame
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, ancho, altura, scale, color):
        image = pygame.Surface((ancho, altura)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * ancho), 0, ancho, altura))
        image = pygame.transform.scale(image, (ancho * scale, altura * scale))
        image.set_colorkey(color)
        return image