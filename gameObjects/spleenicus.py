from . import Fighter
from FSMs import WalkingFSM, AccelerationFSM, VelocityFSM, JumperFSM, CharacterFSM, AttackerFSM, DamageFSM
from utils import vec, RESOLUTION
from . import Drawable

from pygame.locals import *

import pygame
import numpy as np


class Spleenicus(Fighter):
   def __init__(self, position):
      super().__init__(position, "spleenicus.png", (0, 120, 60, 30), health = 20)

      #self.hat = Drawable(position, "hat.png")
      self.spriteOffset = vec(-158, -55)
      #self.hatOffset = vec(-1, -5)
      #self.hat.image = pygame.transform.flip(self.hat.image, True, False)

      """self.hurtBoxOffset = (34, 50, -70, -49)
      self.hurtBox = pygame.Rect(0+self.hurtBoxOffset[0],0+self.hurtBoxOffset[1], self.getSize()[0]+self.hurtBoxOffset[2], self.getSize()[1]+self.hurtBoxOffset[3])"""
      
      # Animation variables specific to Kirby
      self.framesPerSecond = 2 
      self.nFrames = 2

      self.specialMeterMax = 100
      self.specialMeter = 100

      self.hitBoxRect = pygame.Rect(self.hurtBoxOffset[0]+15, self.hurtBoxOffset[1], self.hurtBoxOffset[2]+25, self.hurtBoxOffset[3])
      self.closeBoxRect = pygame.Rect(-70, 60, 200, 160)
      self.hitBoxRectFlipped = pygame.Rect(self.hurtBoxOffset[0]-40, self.hurtBoxOffset[1], self.hurtBoxOffset[2]+25, self.hurtBoxOffset[3])
      
      self.nFramesList = {
         "moving"   : 18,
         "standing" : 12,
         "jumping" : 4,
         "falling" : 5,
         "attacking" : 8,
         "specialing" : 23,
         "down" : 13,
         "airAttacking" : 9,
         "powerAttacking" : 15,
         "thrown": 4,
         "floored" : 4,
         "killed" : 4,
         "stun" : 8
      }
      
      self.rowList = {
         "moving"   : 8,
         "standing" : 2,
         "jumping" : 6,
         "falling" : 11,
         "attacking" : 3,
         "specialing" : 12,
         "down" : 0,
         "airAttacking" : 13,
         "powerAttacking" : 5,
         "thrown" : 10,
         "floored" : 0,
         "killed" : 1,
         "stun" : 9
      }
      
      self.framesPerSecondList = {
         "moving"   : 15,
         "standing" : 10,
         "jumping" : 10,
         "falling" : 10,
         "attacking" : 20,
         "specialing" : 30,
         "down" : 10,
         "airAttacking" : 20,
         "powerAttacking" : 20,
         "thrown": 2,
         "floored" : 4,
         "killed" : 4,
         "stun" : 10
      }
            
      self.FSManimated = CharacterFSM(self)
      self.LR = VelocityFSM(self, axis=0, bound = (150, RESOLUTION[0]-150), accel = 90)
      self.UD = VelocityFSM(self, axis=1, bound = (RESOLUTION[1]//2-135, (RESOLUTION[1]//2)+175), accel = 60)
      self.jumper = JumperFSM(self)
      self.attacker = AttackerFSM(self)
      self.damage = DamageFSM(self)
      
      
   def handleEvent(self, event):
      if event.type == KEYDOWN:
         if self.damage == "neutral":
            if event.key == K_UP:
               self.UD.decrease()
               
            elif event.key == K_DOWN:
               self.UD.increase()
               
            elif event.key == K_LEFT:
               self.LR.decrease()
               
            elif event.key == K_RIGHT:
               self.LR.increase()
         
         if event.key == K_c:
            if self.attacker == "neutral" and self.jumper == "grounded" and self.damage == "neutral":
               self.jumper.on_enter_jumping()
               self.jumper.initLR = self.velocity[0]
               self.jumper.jump()
         
         elif event.key == K_x:
            if self.damage == "neutral":
               print("standard attack")
               self.attacker.on_enter_attack()
               self.attacker.punch()
         
         elif event.key == K_z and self.jumper == "grounded" and self.specialMeter == self.specialMeterMax:
            print("special attack")
            self.attacker.on_enter_special()
            self.attacker.special()
            self.specialMeter = 1
            
      elif event.type == KEYUP:
         if event.key == K_UP:
            self.UD.stop_decrease()
             
         elif event.key == K_DOWN:
            self.UD.stop_increase()
             
            
         elif event.key == K_LEFT:
            self.LR.stop_decrease()
            
         elif event.key == K_RIGHT:
            self.LR.stop_increase()
      
      if event.type == pygame.JOYAXISMOTION:
         if self.damage == "neutral":
            if event.axis == 0 and event.value > 0.1:
               self.LR.stop_decrease()
               self.LR.increase()
            elif event.axis == 0 and event.value < -0.1:
               self.LR.stop_increase()
               self.LR.decrease()
            elif event.axis == 0:
               self.LR.stop_all()
            if event.axis == 1 and event.value > 0.1:
               self.UD.stop_decrease()
               self.UD.increase()
            elif event.axis == 1 and event.value < -0.1:
               self.UD.stop_increase()
               self.UD.decrease()
            elif event.axis == 1:
               self.UD.stop_all()
         
         if event.type == pygame.JOYHATMOTION:
            if event.value[0] > 0.1:
               self.LR.stop_decrease()
               self.LR.increase()
            elif event.value[0] < -0.1:
               self.LR.stop_increase()
               self.LR.decrease()
            else:
               self.LR.stop_all()
            
            if event.value[1] < -0.1:
               self.UD.stop_decrease()
               self.UD.increase()
            elif event.value[1] > 0.1:
               self.UD.stop_increase()
               self.UD.decrease()
            else:
               self.UD.stop_all()
      
      if event.type == pygame.JOYBUTTONDOWN:
         if event.button == 0:
            if self.attacker == "neutral" and self.jumper == "grounded" and self.damage == "neutral":
               self.jumper.on_enter_jumping()
               self.jumper.initLR = self.velocity[0]
               self.jumper.jump()
         if event.button == 2:
            if self.damage == "neutral":
               print("standard attack")
               self.attacker.on_enter_attack()
               self.attacker.punch()
         if event.button == 3 and self.jumper == "grounded" and self.specialMeter == self.specialMeterMax:
            print("special attack")
            self.attacker.on_enter_special()
            self.attacker.special()
            self.specialMeter = 0

            
   def draw(self, drawSurface):
      super().draw(drawSurface, offset = self.spriteOffset)
      #self.hat.draw(drawSurface, offset = self.spriteOffset)
      
      
   
   def update(self, seconds): 
      self.LR.update(seconds)
      self.UD.update(seconds)
      self.jumper.update(seconds)
      self.attacker.update(seconds)
      self.damage.update(seconds)
      if self.attacker != "neutral" and self.attacker != "airAttack":
         self.velocity[0], self.velocity[1] = 0, 0
      if self.velocity[0] < 0:
         self.flip = True
         self.spriteOffset[0] = -295
      if self.velocity[0] > 0:
         self.spriteOffset[0] = -158
         self.flip = False
      
      #self.hat.position = self.hatOffset + self.position
      super().update(seconds)

   
   
  