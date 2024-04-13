from . import Animated
from utils import vec, magnitude, scale, rectAdd
import pygame

class Fighter(Animated):
    def __init__(self, position, fileName="", hurtBoxOffset = (0, 0, 0, 0), hitBoxOffset = (0, 0, 0, 0), closeBoxOffset = (0, 0, 0, 0), flip = 0, health = 7):
        super().__init__(position, fileName)
        self.velocity = vec(0,0)
        self.maxVelocity = 200
        self.hurtBoxOffset = hurtBoxOffset
        self.hurtBoxRect = pygame.Rect(self.hurtBoxOffset)
        self.hurtBox = rectAdd(self.position, self.hurtBoxRect)

        self.closeBoxOffset = closeBoxOffset
        self.closeBoxRect = pygame.Rect(self.closeBoxOffset)
        self.closeBox = rectAdd(self.position, self.closeBoxRect)

        self.hitBoxOffset = hitBoxOffset
        self.hitBoxRect = pygame.Rect(self.hitBoxOffset)
        self.hitBoxRectFlipped = pygame.Rect(self.hitBoxOffset)
        self.hitBox = rectAdd(self.position, self.hitBoxRect)

        self.specialBoxRect = pygame.Rect(self.hurtBoxOffset[0]-50, self.hurtBoxOffset[1]-10, self.hurtBoxOffset[2]+100, self.hurtBoxOffset[3]+20)
        self.specialBox = rectAdd(self.position, self.specialBoxRect)

        self.health = health
    
    def update(self, seconds):
        super().update(seconds)
        if magnitude(self.velocity) > self.maxVelocity:
            self.velocity = scale(self.velocity, self.maxVelocity)
        self.position += self.velocity * seconds
        self.updateHurtBox()
        self.updateHitBox()
        self.updateCloseBox()
        self.updateSpecialBox()
    
    def updateHurtBox(self):
        self.hurtBox = rectAdd(self.position, self.hurtBoxRect)
    
    def updateSpecialBox(self):
        self.specialBox = rectAdd(self.position, self.specialBoxRect)

    def updateCloseBox(self):
        self.closeBox = rectAdd(self.position, self.closeBoxRect)

    def updateHitBox(self):
        if self.flip:
            self.hitBox = rectAdd(self.position, self.hitBoxRectFlipped)
        else:
            self.hitBox = rectAdd(self.position, self.hitBoxRect)