from . import AbstractGameFSM
from statemachine import State

class AttackerFSM(AbstractGameFSM):
    def __init__(self,obj):
        super().__init__(obj)
        self.attackTimer = 0
        self.attackTime = .25
        self.powerAttackTime = .5
        self.specialTimer = 0
        self.specialTime = .75
        self.initLR = 0
        self.comboTimer = 0
        self.comboCount = 0

    neutral = State(initial=True)
    attacking = State()
    #airAttacking = State()
    specialing = State()
    powerAttacking = State()

    attack = neutral.to(attacking) | \
        attacking.to.itself(internal=True) | specialing.to.itself(internal = True) | powerAttacking.to.itself(internal = True)
    powerAttack = attacking.to(powerAttacking) | powerAttacking.to.itself(internal = True) | neutral.to(powerAttacking)
    #airAttack = neutral.to(airAttacking) | \
        #attacking.to.itself(internal=True) | airAttacking.to.itself(internal=True) | specialing.to.itself(internal = True)
    special = neutral.to(specialing) | \
        attacking.to(specialing) | specialing.to.itself(internal = True) | powerAttacking.to(specialing)
    stop = attacking.to(neutral) | specialing.to(neutral) | powerAttacking.to(neutral)


    
    def on_enter_attack(self):
        pass
    
    def on_enter_special(self):
        self.specialTimer = self.specialTime
    
    def punch(self):
        if self.comboCount != 3:
            self.attackTimer = self.attackTime
            self.comboTimer = self.attackTime + 20
            self.attack()
        elif self.obj.jumper == "grounded":
            self.attackTimer = self.powerAttackTime
            self.comboTimer = self.attackTime + 20
            self.powerAttack()
            self.comboCount = 0
        else:
            self.attack
    
    
    def update(self, seconds=0):
        if self.comboTimer != 0:
            self.comboTimer -= 1
        if self.comboTimer < 0:
            self.comboCount = 0
        if self == "attacking" or self == "powerAttacking":
            self.attackTimer -= seconds
            if self.attackTimer <= 0:
                self.comboCount += 1
                self.stop()
                self.obj.FSManimated.stop()
            
        elif self == "specialing":
            self.specialTimer -= seconds
            if self.specialTimer <= 0:
                self.stop()
                self.obj.FSManimated.stop()

        elif self == "airAttacking":
            self.airAttackTimer -= seconds
            if self.obj.jumper == "grounded":
                self.stop()
                self.obj.FSManimated.stop()

                #collidelist? make a list of enemy hurtboxes and test against player hitbox