from utils import SpriteManager, SCALE, RESOLUTION, vec

import pygame

class Drawable(object):
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None, flip=False):
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
        
        self.position=vec(*position)
        self.imageName = fileName
        self.rotate = False
        self.flip = False
    
    def draw(self, drawSurface):
        """if self.flipped:
          drawSurface.blit(pygame.transform.flip(self.image), list(map(int, self.position - Drawable.CAMERA_OFFSET)))
        else:"""
        drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
            
    def getSize(self):
        return vec(*self.image.get_size())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass

    def setDrawPosition(self, offset):
        if self.rotate:
            self.image = pygame.transform.rotate(self.original, self.angle)
            center = vec(*self.unrotatedImage.get_rect().center)
            rotatedCenter = vec(*self.image.get_rect().center)
            self.drawPosition = self.position - center - rotatedCenter
            
        else:
            self.drawPosition = self.position + offset

    def draw(self, drawSurface, offset = (0,0)):
        self.setDrawPosition(offset)
        if self.flip:
            drawSurface.blit(pygame.transform.flip(self.image, True, False), list(map(int, self.drawPosition)))
        else:
            drawSurface.blit(self.image, list(map(int, self.drawPosition)))
