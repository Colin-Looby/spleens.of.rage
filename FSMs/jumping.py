from statemachine import State
from animation import AnimateFSM
from . import magnitude, EPSILON

class JumpingFSM(AnimateFSM):
    EPSILON
    standing = State(initial=True)
    moving   = State()
    falling  = State()
    jumping  = State()

    def hasVelocity(self):
        return magnitude(self.obj.velocity) > EPSILON
    
    def noVelocity(self):
        return not self.hasVelocity()
    
    def isFalling(self):
        return self.obj.velocity[1] > EPSILON
    
    def isJumping(self):
        return self.obj.velocity[1] < -EPSILON
    
    def isGrounded(self):
        return not self.isFalling() and not self.isJumping()
    
    move = standing.to(moving)
    
    stop = moving.to(standing)
         
    jump = standing.to(jumping) | moving.to(jumping) | falling.to.itself(internal=True)
    
    fall = standing.to(falling) | moving.to(falling) | jumping.to(falling)
    
    land = falling.to(moving, cond="hasVelocity")  | \
           falling.to(standing, cond="noVelocity") | \
           jumping.to(moving, cond="hasVelocity")  | \
           jumping.to(standing, cond="noVelocity")
    
    def updateState(self):        
        if self.isJumping() and self != "jumping":
            self.jump()
        elif self.isFalling() and self != "falling":
            self.fall()
        elif self.isGrounded() and self not in ["standing", "moving"]:
            self.land()
        elif self.hasVelocity() and self not in ["moving", "falling", "jumping"]:
            self.move()
        elif self.noVelocity() and self not in ["standing", "falling", "jumping"]:
            self.stop()