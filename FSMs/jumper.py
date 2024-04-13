from . import AbstractGameFSM
from statemachine import State
from utils import SoundManager

class JumperFSM(AbstractGameFSM):
    def __init__(self,obj):
        super().__init__(obj)
        self.jumpTimer = 0
        self.jumpSpeed = 2
        self.jumpTime = .3
        self.fallTimer = 0
        self.initLR = 0
        self.initSpriteOffset = self.obj.spriteOffset[1]
        self.soundManager = SoundManager.getInstance()

    grounded = State(initial=True)
    jumping = State()
    falling = State()
   
    jump = grounded.to(jumping) | \
        falling.to.itself(internal=True) | jumping.to.itself(internal=True)
    fall = jumping.to(falling)  | \
        grounded.to(falling)
    land = falling.to(grounded) | \
        jumping.to(grounded)

    
    def updateState(self):
        if self.canFall() and self == "jumping":
            self.fall()
    
    def canFall(self):
        return self.jumpTimer <= 0
    
    def on_enter_jumping(self):
        self.jumpTimer = self.jumpTime

    
    def update(self, seconds=0):

        if not self == "grounded": 
            self.obj.velocity[0], self.obj.velocity[1] = self.initLR, 0
            if self.obj.position[0]+self.obj.hurtBoxOffset[0] < self.obj.LR.bound[0]:
                self.obj.velocity[0] = max(self.obj.velocity[0], 0)
            if self.obj.position[0]+self.obj.hurtBoxOffset[0]+self.obj.hurtBoxOffset[2] > self.obj.LR.bound[1]:
                self.obj.velocity[0] = min(self.obj.velocity[0], 0)
        
        if self == "falling":
            self.obj.spriteOffset[1] += self.jumpSpeed
            self.fallTimer -= seconds
            if self.fallTimer <= 0:
                self.obj.spriteOffset[1] = self.initSpriteOffset
                self.land()
                self.obj.FSManimated.stop()
            
        elif self == "jumping":
            self.obj.spriteOffset[1] -= self.jumpSpeed
            self.jumpTimer -= seconds
            if self.canFall():
                self.fallTimer = self.jumpTime
                self.fall()


