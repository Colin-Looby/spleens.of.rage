import pygame

from . import Drawable, Dummy

from utils import vec, RESOLUTION, rectAdd

class GameEngine2(object):
    import pygame

    def __init__(self):       
        self.dummy = Dummy((RESOLUTION[0]//2-60//2,(RESOLUTION[1]//2)-63))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        self.dummy.draw(drawSurface)

        pygame.draw.rect(drawSurface, (200, 0, 200), self.dummy.hurtBox, 1)
        pygame.draw.rect(drawSurface, (200, 0, 0), self.dummy.hitBox, 1)
            
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        self.dummy.update(seconds)
        
        Drawable.updateOffset(self.dummy, self.size)
    

