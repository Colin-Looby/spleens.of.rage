from . import AbstractGameFSM
from statemachine import State

class GravityFSM(AbstractGameFSM):
    def __init__(self,obj):
        super().__init__(obj)
        self.jumpTimer = 0
        self.gravity = 10
        self.jumpSpeed = 10
        self.jumpTime = 0.2
        self.fallTimer = 0

    grounded = State(initial=True)
    jumping = State()
    falling = State()
   
    jump = grounded.to(jumping) | \
        falling.to.itself(internal=True)
    fall = jumping.to(falling)  | \
        grounded.to(falling)
    land = falling.to(grounded) | \
        jumping.to(grounded)
    
    def updateState(self):
        if self.canFall() and self == "jumping":
            self.fall()
    
    def canFall(self):
        return self.jumpTimer < 0
    
    def on_enter_jumping(self):
        self.jumpTimer = self.jumpTime
    
    def update(self, seconds=0):
        if self.canFall() and not self == "grounded":
            self.fallTimer = self.jumpTime
            self == "falling"
        
        if self == "falling":
            self.obj.spriteOffset[1] += self.gravity
            self.fallTimer -= seconds
        
        elif self == "jumping":
            self.obj.spriteOffset[1] = -self.jumpSpeed
            self.jumpTimer -= seconds
        else:
            self.obj.spriteOffset[1] = 0
        


