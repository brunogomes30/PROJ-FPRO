import variables
import pygame

class Button:
    
    def __init__(self, x = 0, y = 0, width = 0, height = 0, text ="Text", hover_color = (255, 255, 255), color = (0, 0, 255)):
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.text = text
        self.onclick = None
        self.color = color
        self.hover_color = hover_color
        self.hover_state = False
        
    
    def draw_self(self):
        color = self.hover_color if self.hover_state else self.color
        pygame.draw.rect(variables.screen, color, (self.x, self.y, self.width, self.height))
        
        text = variables.font.render(self.text, 1, (0, 0, 0))
        text_x = self.x + (self.width - text.get_width()) // 2
        text_y = self.y + (self.height - text.get_height()) //2
        variables.screen.blit(text, (text_x, text_y))
        
    def check_collision(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height
        