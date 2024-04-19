from . import Fighter
from FSMs import VelocityFSM, JumperFSM, CharacterFSM, AttackerFSM, DamageFSM
from utils import vec, RESOLUTION
from . import Drawable
from pygame.locals import *

import pygame
import numpy as np
import random

class Dummy(Fighter):
    def __init__(self, position, flip = False):
        super().__init__(position, "dummy.png", (0, 120, 60, 30))

        self.spriteOffset = vec(-200,-75)

        self.hitBoxRect = pygame.Rect(self.hurtBoxOffset[0]+10, self.hurtBoxOffset[1], self.hurtBoxOffset[2]+6, self.hurtBoxOffset[3])
        self.hitBoxRectFlipped = pygame.Rect(self.hurtBoxOffset[0]-16, self.hurtBoxOffset[1], self.hurtBoxOffset[2]+6, self.hurtBoxOffset[3])

        self.nFramesList = {
            "standing" : 22,
            "stun" : 10,
            "moving" :  19,
            "attacking" : 7,
            "powerAttacking" : 10,
            "floored" : 10
        }

        self.rowList = {
            "standing" : 0,
            "stun" : 4,
            "moving" : 3,
            "attacking" : 1,
            "powerAttacking" : 2,
            "floored" :10
        }

        self.framesPerSecondList = {
            "standing" : 15,
            "stun" : 33,
            "moving" : 20,
            "attacking" : 10,
            "powerAttacking" : 10,
            "floored" : 10
        }

        self.FSManimated = CharacterFSM(self)
        self.LR = VelocityFSM(self, axis=0, bound = (0, RESOLUTION[0]), accel = 60)
        self.UD = VelocityFSM(self, axis=1, bound = (RESOLUTION[1]//2-135, (RESOLUTION[1]//2)+175), accel = 40)
        self.jumper = JumperFSM(self)
        self.attacker = AttackerFSM(self)
        self.damage = DamageFSM(self)
        self.plan = "idle"
        self.wanderTimer = 0
        self.wanderDirection = (0,0)
        self.waitTimer = 0
    
    def draw(self, drawSurface):
      super().draw(drawSurface, offset = self.spriteOffset)

    
    def update(self, seconds, spleenicus, aggro): 
        if self.plan == "idle":
            self.LR.stop_all()
            self.UD.stop_all()
            wheel = []
            for i in range(10):
                wheel.append("wander")
            for i in range(200):
                wheel.append("idle")
            for x in range(30//(aggro+2)):
                wheel.append("attack")
            descision = random.sample(wheel, 1)
            if descision[0] == "wander":
                self.wanderDirection = (random.randint(-1,1), random.randint(-1,1))
                self.wanderTimer = random.randint(0, 70)
                self.plan = "wander"
            if descision[0] == "attack":
                self.waitTimer = random.randint(5, 20)
                self.plan = "attack"

        elif self.plan == "attack":
            if self.damage == "stun":
                self.plan = "idle"
            if self.hitBox.colliderect(spleenicus.hurtBox):
                if self.waitTimer < 0:
                    self.attacker.on_enter_attack()
                    self.attacker.punch()
                    self.plan = "punch"
                else:
                    self.waitTimer -= 1
            else:
                if abs(self.position[0] - spleenicus.position[0]) > 20 and self.position[0] > spleenicus.position[0]:
                    self.LR.decrease()
                elif abs(self.position[0] - spleenicus.position[0]) > 20 and self.position[0] < spleenicus.position[0]:
                    self.LR.increase()
                if abs(self.position[1] - (spleenicus.position[1]+spleenicus.hurtBoxOffset[1])) > 20 and self.position[1] > spleenicus.position[1]:
                    self.UD.decrease()
                elif abs(self.position[1] - (spleenicus.position[1]+spleenicus.hurtBoxOffset[1])) > 20 and self.position[1] < spleenicus.position[1]:
                    self.UD.increase()
                if self.FSManimated == "stun":
                    self.LR.stop_all()
                    self.UD.stop_all()

        elif self.plan == "punch":
            if self.attacker == "neutral":
                coin = random.randint(0,1)
                if coin == 0:
                    self.plan = "idle"
                else:
                    self.attacker.on_enter_attack()
                    self.attacker.punch()

        elif self.plan == "wander":
            self.wanderTimer -= 1
            if self.wanderTimer < 0:
                self.plan = "idle"
                self.LR.stop_all()
                self.UD.stop_all()
            if self.wanderDirection[0] == -1 and self.LR != "negative":
                self.LR.decrease()
            elif self.wanderDirection[0] == 0 and self.LR != "not_moving":
                self.LR.stop_all()
            elif self.wanderDirection[0] == 1 and self.LR != "positive":
                self.LR.increase()
            if self.wanderDirection[1] == -1 and self.UD != "negative":
                self.UD.decrease()
            elif self.wanderDirection[1] == 0 and self.UD != "not_moving":
                self.UD.stop_all()
            elif self.wanderDirection[1] == 1 and self.UD != "positive":
                self.UD.increase()
            if self.FSManimated == "stun":
                self.LR.stop_all()
                self.UD.stop_all()
            
            

        self.LR.update(seconds)
        self.UD.update(seconds)
        self.jumper.update(seconds)
        self.attacker.update(seconds)
        self.damage.update(seconds)
        if self.attacker != "neutral" and self.attacker != "airAttack":
            self.velocity[0], self.velocity[1] = 0, 0
        if self.LR == "negative" and self.flip == False:
             self.flip = True
             self.spriteOffset[0] = -250
        if self.LR == "positive" and self.flip:
             self.flip = False
             self.spriteOffset[0] = -200
        #self.hat.position = self.hatOffset + self.position
        super().update(seconds)