from . import AbstractGameFSM
from statemachine import State

class DamageFSM(AbstractGameFSM):
    def __init__(self,obj):
        super().__init__(obj)
        self.totalHealth = 200
        self.hitStun = .3
        self.hitStunTimer = 0
        self.throwTimer = 0
        self.throwTime = 2.5
        self.corpseTimer = 0
        self.corpseTime = 100
        self.flooredTimer = 0
        self.flooredTime = 20
    
    neutral = State(initial=True)
    stun = State()
    killed = State()
    thrown = State()
    floored = State()

    hit = neutral.to(stun) | killed.to.itself(internal = True) | stun.to.itself(internal = True) | thrown.to.itself(internal = True)
    stop = stun.to(neutral) | neutral.to.itself(internal=True) | floored.to(neutral)
    floor = stun.to(floored) | neutral.to(floored) | floored.to.itself(internal = True) | thrown.to(floored)
    throw = stun.to(thrown) | neutral.to(thrown) | killed.to.itself(internal = True) | thrown.to.itself(internal = True) | neutral.to(thrown)
    kill = floored.to(killed) | stun.to(killed) | thrown.to(killed)

    def on_taking_damage(self):
        self.hitStunTimer = self.hitStun
    
    def on_throw(self):
        self.throwTimer = self.throwTime
    
    def on_kill(self):
        self.corpseTimer = self.corpseTime

    def update(self, seconds=0):
        if self == "stun":
            self.hitStunTimer -= seconds
            if self.hitStunTimer <= 0:
                self.stop()
                self.obj.FSManimated.stop()
        if self == "thrown":
            self.throwTimer -= seconds
            if self.throwTimer <= 0:
                self.flooredTimer = self.flooredTime
                self.floor()
        if self == "floored":
            self.flooredTimer -= seconds
            if self.flooredTimer <= 0:
                self.stop()
                self.obj.FSManimated.stop()
        if self == "killed":
            self.corpseTimer -= seconds