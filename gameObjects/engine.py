import pygame
from random import randint

from . import Drawable, Spleenicus, Dummy, Gremlin

from utils import vec, RESOLUTION, rectAdd, SoundManager

class GameEngine(object):
    import pygame

    def __init__(self):       
        self.spleenicus = Spleenicus((RESOLUTION[0]//2-96//2,(RESOLUTION[1]//2)-30))
        self.arenaX = [0, RESOLUTION[0]]
        self.arenaY = [RESOLUTION[1]//2-100, (RESOLUTION[1]//2)+100]
        self.waveCounter = 0
        self.waves = [[Dummy((randint(self.arenaX[0], self.arenaX[1]), randint(self.arenaY[0], self.arenaY[1]))) for x in range(y)] for y in range(50)]
        self.enemyList = []
        for enemy in self.waves[self.waveCounter]:
            self.enemyAdd(enemy)
        self.enemyListlength = len(self.enemyList)
        #for i in range(2):
            #self.enemyAdd(Dummy((randint(self.arenaX[0], self.arenaX[1]), randint(self.arenaY[0], self.arenaY[1]))))
        self.enemyAdd(Dummy((RESOLUTION[0]//2-20,(RESOLUTION[1]//2)-15)))
        self.enemyAdd(Dummy((RESOLUTION[0]//2, RESOLUTION[1]//2-20)))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "background.png")
        self.soundManager = SoundManager.getInstance()
        self.soundManager.playBGM("spleens_of_rage.wav")
        self.alreadyPlayed = False
        self.aggro = 0
        self.quitTimer = 400
    
    def enemyAdd(self, enemy):
        self.enemyList.append(enemy)

    def hitfx(self):
        self.soundManager.playSFX("punch"+str(randint(0,6))+".wav")

    def deathfx(self):
        self.soundManager.playSFX("oo" + str(randint(0,3) + ".wav"))

    def draw(self, drawSurface):        
        self.background.draw(drawSurface)

        entityList = [x for x in self.enemyList]
        entityList.append(self.spleenicus)
        
        while len(entityList) > 0:
            lowx = min(x.position[1] for x in entityList)
            for x in entityList:
                if lowx == x.position[1]:
                    x.draw(drawSurface)
                    entityList.remove(x)
                    break




        """if self.spleenicus.position[1] < self.dummy.position[1]:
            self.spleenicus.draw(drawSurface)
            self.dummy.draw(drawSurface)
        else:
            self.dummy.draw(drawSurface)
            self.spleenicus.draw(drawSurface)"""
        
        """pygame.draw.rect(drawSurface, (0, 0, 200), self.spleenicus.specialBox, 1)
        pygame.draw.rect(drawSurface, (200, 200, 0), self.spleenicus.closeBox, 1)
        pygame.draw.rect(drawSurface, (200, 0, 200), self.spleenicus.hurtBox, 1)
        pygame.draw.rect(drawSurface, (200, 0, 0), self.spleenicus.hitBox, 1)"""
        healthBar = pygame.Rect(10, 10, self.spleenicus.health*20, 20)
        pygame.draw.rect(drawSurface, (255, 0, 0), healthBar)
        healthMax = pygame.Rect(10, 10, 400, 20)
        pygame.draw.rect(drawSurface, (255, 0, 0), healthMax, 1)
        specialBar = pygame.Rect(RESOLUTION[0]-10-self.spleenicus.specialMeter, 10, self.spleenicus.specialMeter, 20)
        pygame.draw.rect(drawSurface, (255, 255, 0), specialBar)
        specialMax = pygame.Rect(RESOLUTION[0]-110, 10, 100, 20)
        pygame.draw.rect(drawSurface, (255, 255, 0), specialMax, 1)


        """for x in self.enemyList:
            pygame.draw.rect(drawSurface, (200, 0, 200), x.hurtBox, 1)
            pygame.draw.rect(drawSurface, (200, 0, 0), x.hitBox, 1)"""
            
    def handleEvent(self, event):
        self.spleenicus.handleEvent(event)
    
    def update(self, seconds):
        self.aggro = 0
        self.spleenicus.update(seconds)
        for enemy in self.enemyList:
            if self.spleenicus.hitBox.colliderect(enemy.hurtBox):
                if self.spleenicus.attacker == "attacking":
                    if enemy.damage == "neutral":
                        print("hit!")
                        if enemy.health > 0:
                            self.hitfx()
                        enemy.health -= 1
                        enemy.damage.on_taking_damage()
                        enemy.damage.hit()
                        self.spleenicus.specialMeter += 5
                        if self.spleenicus.specialMeter > 100:
                            self.spleenicus.specialMeter = 100
                elif self.spleenicus.attacker == "powerAttacking":
                    print("power hit!")
                    if enemy.health > 0:
                        self.hitfx()
                    enemy.health -= 3
                    enemy.damage.on_throw()
                    enemy.damage.throw()
                    self.spleenicus.specialMeter += 5
                    if self.spleenicus.specialMeter > 100:
                        self.spleenicus.specialMeter = 100
            if self.spleenicus.specialBox.colliderect(enemy.hurtBox) and self.spleenicus.attacker == "specialing":
                print("special hit!")
                if enemy.health > 0:
                    self.hitfx()
                enemy.health -= 5
                enemy.damage.on_taking_damage()
                enemy.damage.hit()
            if self.spleenicus.closeBox.colliderect(enemy.hurtBox):
                self.aggro += 1
            if enemy.health <= 0:
                if enemy.damage == "floored":
                    enemy.damage.on_kill()
                    enemy.damage.kill()
                elif enemy.damage == "neutral":
                    enemy.damage.on_throw()
                    enemy.damage.throw()
                if enemy.damage.corpseTimer <= 0:
                    print("b")
                    self.enemyList.remove(enemy)
            if enemy.hitBox.colliderect(self.spleenicus.hurtBox) and (enemy.attacker == "attacking" or enemy.attacker == "powerAttacking"):
                if self.spleenicus.damage == "neutral":
                    print("spleen hit")
                    self.hitfx()
                    self.spleenicus.health -= 1
                    self.spleenicus.damage.on_taking_damage()
                    self.spleenicus.damage.hit()
        for enemy in self.enemyList:
            enemy.update(seconds, self.spleenicus, self.aggro)
            if enemy.health <= 0:
                self.enemyList.pop(enemy)
                self.deathfx()
        
        if self.spleenicus.health <= 0 and not self.alreadyPlayed:
            self.soundManager.playBGM("game_over.wav")
            self.alreadyPlayed = True
            self.spleenicus.damage.kill()

        if self.spleenicus.health <=0:
            self.quitTimer -= 1
            print(self.quitTimer)
            if self.quitTimer == 0:
                pygame.quit()
        
        if self.waveCounter > len(self.waves):
            if not self.alreadyPlayed:
                self.soundManager.playBGM("game_over.wav")
                self.alreadyPlayed = True
            self.quitTimer -=1
            if self.quitTimer == 0:
                pygame.quit()
        if len(self.enemyList) == 0 and self.waveCounter <= len(self.waves):
            self.waveCounter +=1
            if self.waveCounter % 3 == 0:
                self.spleenicus.health = 20 + self.waveCounter
            for enemy in self.waves[self.waveCounter]:
                self.enemyAdd(enemy)

        
        
        Drawable.updateOffset(self.spleenicus, self.size)
    

