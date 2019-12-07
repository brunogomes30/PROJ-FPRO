import pygame
import variables

class Label:
    def __init__(self, text, y = 0, x = 0):
        self.y = y
        self.x = x
        self.ticks = variables.FPS * 3
        self.ticksLeft = self.ticks
        self.text = text
        
    def draw_self(self):
        self.y -= 0.2
        var_alpha = int(self.ticksLeft/self.ticks*255)
        self.display = variables.font.render(self.text, 1, (255, 255, 255))
        arr = pygame.surfarray.pixels_alpha(self.display)
        arr[:,:] = (arr[:,:] * (var_alpha/255)).astype(arr.dtype)
        del arr
        variables.screen.blit(self.display, (self.x, self.y))