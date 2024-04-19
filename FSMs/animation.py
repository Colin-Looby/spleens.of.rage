from . import AbstractGameFSM
from utils import magnitude, EPSILON, SpriteManager

from statemachine import State

class AnimateFSM(AbstractGameFSM):
    """For anything that animates. Adds behavior on
       transitioning into a state to change animation."""
    def on_enter_state(self):
        state = self.current_state.id
        if self.obj.row != self.obj.rowList[state]:
            self.obj.nFrames = self.obj.nFramesList[state]
            self.obj.frame = 0
            self.obj.row = self.obj.rowList[state]
            self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
            self.obj.animationTimer = 0
            self.obj.image = SpriteManager.getInstance().getSprite(self.obj.imageName,
                                                                   (self.obj.frame, self.obj.row))
         
        
class WalkingFSM(AnimateFSM):
    """""Two-state FSM for walking / stopping in
       a top-down environment."""""
       
    standing = State(initial=True)
    moving   = State()

    
    move = standing.to(moving)
    stop = moving.to(standing)
        
    
    def updateState(self):
        if self.hasVelocity() and self != "moving":
            self.move()
        elif not self.hasVelocity() and self != "standing":
            self.stop()
    
    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON
    
    def noVelocity(self):
        return not self.hasVelocity()
    
class CharacterFSM(AnimateFSM):
       
    standing = State(initial=True)
    moving   = State()
    jumping = State()
    falling = State()
    attacking = State()
    specialing = State()
    stun = State()
    airAttacking = State()
    powerAttacking = State()
    floored = State()
        
    move = standing.to(moving)
    stop = moving.to(standing) | jumping.to(standing) | falling.to(standing) | attacking.to(standing) | standing.to.itself(internal = True) |  \
        specialing.to(standing) | stun.to(standing) | airAttacking.to(standing) | powerAttacking.to(standing) | floored.to.itself(internal = True)
    jump = standing.to(jumping) | moving.to(jumping) | attacking.to.itself(internal = True) | stun.to.itself(internal = True) | floored.to.itself(internal = True)
    fall = jumping.to(falling) | airAttacking.to.itself(internal = True) | floored.to.itself(internal = True)
    attack = standing.to(attacking) | moving.to(attacking) | specialing.to.itself(internal = True) | stun.to.itself(internal = True) | jumping.to(airAttacking) | falling.to(airAttacking) | floored.to.itself(internal = True)
    damaged = standing.to(stun) | moving.to(stun) | falling.to(stun) | specialing.to(stun) | jumping.to.itself(internal = True) | attacking.to(stun) | stun.to.itself(internal = True) | floored.to.itself(internal = True)
    special = standing.to(specialing) | moving.to(specialing) | attacking.to(specialing) | specialing.to.itself(internal = True) | stun.to(specialing) | floored.to.itself(internal = True)
    airAttack = jumping.to(airAttacking) | airAttacking.to.itself(internal = True) | falling.to(airAttacking) | standing.to(airAttacking) | floored.to.itself(internal = True) | moving.to(airAttacking)
    powerAttack = standing.to(powerAttacking) | attacking.to(powerAttacking) | powerAttacking.to.itself(internal = True) | moving.to(powerAttacking) | stun.to.itself(internal = True) | floored.to.itself(internal = True)
    floor = floored.to.itself(internal = True) | standing.to(floored) | stun.to(floored) | moving.to(floored) | attacking.to(floored)
    
    
    def updateState(self):
        if not self.hasVelocity() and self != "standing" and self.obj.jumper == "grounded" and self.obj.attacker == "neutral" and self.obj.damage == "neutral" :
            self.stop()
        elif self.obj.damage == "floored" or self.obj.damage == "killed":
            self.floor()
        elif self.obj.attacker == "powerAttacking":
            self.powerAttack()
        elif self.hasVelocity() and self != "moving" and self.obj.jumper == "grounded" and self.obj.damage == "neutral":
            self.move()
        elif self.obj.jumper == "falling" and self != "falling" and self != "stun" and self != "attacking" and self != "standing" and self != "moving" and self.obj.attacker == "neutral":
            self.fall()
        elif self.obj.jumper == "jumping" and self != "jumping" and self != "stun" and self.obj.attacker == "neutral":
            self.jump()
        elif (self.obj.jumper == "jumping" or self.obj.jumper == "falling") and self.obj.attacker == "attacking":
            self.airAttack()
        elif self.obj.attacker == "attacking" and self != "attacking" and self != "airAttacking" and self.obj.jumper == "grounded":
            self.attack()
        elif self.obj.attacker == "specialing" and self != "specialing":
            self.special()
        elif self.obj.damage == "stun" and self != "stun":
            self.damaged()
        
    
    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON
    
    def noVelocity(self):
        return not self.hasVelocity()