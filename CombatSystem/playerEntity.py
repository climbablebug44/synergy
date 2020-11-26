import math
import pygame
import random
from CombatSystem import projectiles, collectibles, screenElements, currentConfigurations
from common import gameConstants as gc, keyBinding
from pygame import mixer


class deltaTime:
    def __init__(self):
        self.prevTime = pygame.time.get_ticks()

    def delta(self, delta, change=True):
        ticks = pygame.time.get_ticks()
        if ticks - self.prevTime >= delta:
            if change:
                self.prevTime = ticks
            return True
        else:
            return False

    def updateTicks(self):
        self.prevTime = pygame.time.get_ticks()


class attackCooldown:
    def __init__(self, maxCapacity):
        self.time = deltaTime()
        self.maxCapacity = maxCapacity
        self.currLevel = maxCapacity

    def increase(self, increaseBy, delta):
        if self.time.delta(delta):
            self.currLevel += increaseBy
            if self.currLevel > self.maxCapacity:
                self.currLevel = self.maxCapacity

    def decrease(self, decreaseBy):
        self.currLevel -= decreaseBy
        if self.currLevel <= 0:
            self.currLevel = 0
            self.time.updateTicks()

    def currentLevel(self, x=-1):
        if x != -1:
            if self.currLevel == x:
                return True
            else:
                return False
        else:
            return self.currLevel

    def fill(self):
        self.currLevel = self.maxCapacity


class combatEntity(pygame.sprite.Sprite):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups)
        self.rect = pygame.Rect(0, 0, gc.playerSize[0], gc.playerSize[1])
        # print(self.size[0], self.rect.width) # 75
        # print(self.size[1], self.rect.height) # 150
        self.clock = time
        self.gravity = 1
        self.sSManager = ssmanager
        self.velocity = [0, 0]
        self.health = 375
        self.jumping = True
        self.blocking = False
        self.facing = True
        self.tangible = True
        self.platform = platform
        self.group = groups
        self.stunBar = attackCooldown(100)  # MAX Capacity, units
        self.stunTime = 1500  # ms

    def transform(self, vect, vel):
        x = (vect[0] - self.rect.x) // 10
        y = (vect[1] - self.rect.y) // 10
        try:
            x_ = int(vel * x / ((x ** 2 + y ** 2) ** 0.5))
            y_ = int(vel * y / ((x ** 2 + y ** 2) ** 0.5))
        except ZeroDivisionError:
            return None
        return x_, y_

    def update(self, *args):
        """Stun Cooldown"""
        if self.stunBar.currentLevel(0) and self.stunBar.time.delta(self.stunTime):
            self.stunBar.fill()
        ''' Gravity Code'''
        if self.rect.colliderect(self.platform) and self.rect.y >= self.platform.y - self.rect.height:
            self.jumping = False
            self.rect.y = self.platform.y - self.rect.height
            self.velocity[1] = 0
        elif self.jumping:
            self.velocity[1] += self.gravity
        '''/Gravity code'''

        '''L-R bounds'''
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > gc.screenSize[0] - self.rect.width:
            self.rect.x = gc.screenSize[0] - self.rect.width
        '''/bounds'''

        if self.health <= 0:
            self.kill()

    def damage(self, hit, stun=0):
        if not self.stunBar.currentLevel(0):
            self.stunBar.decrease(stun)
        if not self.blocking or self.stunBar.currentLevel(0):
            self.health -= hit
            if self.health > 375:
                self.health = 375
            elif self.health < 0:
                self.health = 0

    def eventHandle(self, event=None):
        """
            will be overrided in player class
            to update only when an event occurs
            Has no use here
        """


class player(combatEntity):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        self.keyBindings = keyBinding.keyBinding().get()
        '''
        keybinding help: 
        [0] : Walk-Left
        [1] : Walk-right
        [2] : Block
        [3] : Light attack   sound done
        [4] : Heavy attack   sound done
        [5], [6] : slot-toggle
        [7] : jump
        [8] : Reload   sound done
        [9] : special
        [10]: magic push
        [11]: auto-aim-shoot
        ~[12]: toggle auto aim
        [13]: toggle selected enemy
        '''
        self.data = currentConfigurations.playerConfig('player.pkl').read()
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pressed()
        self.bulletCount = self.data.gunSlots
        self.image = pygame.transform.scale(pygame.image.load('assets/player.png'), self.rect.size)
        self.magicBar = attackCooldown(self.data.maxCapacityMagicBar)  # Max Capacity
        self.enemy = []
        self.attacks = [self.dashAttack, self.chargedAttack, self.whirlWindStrike]
        self.slot = 0
        self.dashing = False
        self.lockedEnemy = 0
        self.lock = [self.data.autoAim, self.lockedEnemy]
        self.healthBar = screenElements.healthBar(self.group, entity=self,
                                                  position=(gc.screenSize[0] // 10, 10),
                                                  colors=(gc.color['GREEN'], gc.color["RED"]),
                                                  size=(gc.screenSize[0] // 2, 10), maxL=self.health)
        self.stunDisplay = screenElements.stunBar(self.group, entity=self, position=(gc.screenSize[0] // 10, 20),
                                                  size=(gc.screenSize[0] // 2, 10),
                                                  maxlevel=self.stunBar.currentLevel())

    def update(self):
        self.rect = self.rect.move(self.velocity)
        # cheat code
        if pygame.key.get_pressed()[pygame.K_F1]:
            self.health = 375
        for i in self.group[0]:
            if i != self and isinstance(i, EnemyAI):
                if i not in self.enemy:
                    self.enemy.append(i)
                elif i.health <= 0:
                    try:
                        self.enemy.remove(i)
                        self.lockedEnemy = 0
                    except ValueError:
                        continue
        self.magicBar.increase(1, 200)
        if not self.velocity[0]:
            self.movement()
            self.tangible = True
            self.dashing = False
        elif self.velocity[0] > 0:
            self.velocity[0] -= 1
        else:
            self.velocity[0] += 1

        for i in self.enemy:
            if self.dashing and self.rect.colliderect(i):
                i.damage(20, 5)
                self.dashing = False
                print('[Player]: Dash Special Attack Success')
        '''Super Call'''
        super(player, self).update()

    def movement(self):
        if self.stunBar.currentLevel(0):
            return
        # player stunned
        moveFr, moveBa = True, True
        if self.tangible:
            for i in self.enemy:
                if isinstance(i, EnemyAI) and i.tangible:
                    if i.rect.colliderect(self.rect):
                        if self.rect.x > i.rect.x:
                            moveBa = False
                        elif self.rect.x < i.rect.x:
                            moveFr = False

        if self.keys[self.keyBindings[2]]:
            x = 2
            '''Walking slowly when blocking'''
            self.blocking = True
        else:
            x = 1
            self.blocking = False
            ''' attack only when not blocking'''
            if self.keys[self.keyBindings[7]] and not self.jumping:
                self.velocity[1] -= self.data.moveY
                self.jumping = True

        if self.keys[self.keyBindings[1]] and moveFr:
            self.rect.x += self.data.moveX // x
            self.facing = True
        if self.keys[self.keyBindings[0]] and moveBa:
            self.rect.x -= self.data.moveX // x
            self.facing = False

    def eventHandle(self, event=None):
        if self.stunBar.currentLevel(0):
            return
        # player stunned
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == self.keyBindings[10] and self.magicBar.currentLevel() >= 20:
                # Force Field
                projectiles.forceField(self.group[1], creator=self, direction=self.facing)
                projectiles.forceField(self.group[1], creator=self, direction=not self.facing)
                self.magicBar.decrease(20)
            if event.key == self.keyBindings[8] and self.bulletCount == 0:
                # sound for reload
                mixer.init()
                pygame.mixer.music.load('assets/sounds/Reload.mp3')
                pygame.mixer.music.play(1)
                # newly added
                pygame.mixer.music.load('assets/sounds/Deal.mp3')
                pygame.mixer.music.play(-1)
                self.bulletCount = self.data.gunSlots

            if event.key == self.keyBindings[3]:
                # adding shooting sound
                mixer.init()
                pygame.mixer.music.load('assets/sounds/Gun1.mp3')
                pygame.mixer.music.play(1)
                # newly added
                pygame.mixer.music.load('assets/sounds/Deal.mp3')
                pygame.mixer.music.play(-1)
                self.meleeAttack(False)

            if event.key == self.keyBindings[4]:
                # adding shooting sound 
                mixer.init()
                pygame.mixer.music.load('assets/sounds/Gun2.mp3')
                pygame.mixer.music.play(1)
                # newly added
                pygame.mixer.music.load('assets/sounds/Deal.mp3')
                pygame.mixer.music.play(-1)
                self.meleeAttack(True)

            if self.lock[0] and self.keys[self.keyBindings[11]] and self.bulletCount > 0:
                # TODO: DO changes here
                projectiles.bullets(self.group[1], creator=self,
                                    vel=(self.transform(
                                        (self.enemy[self.lockedEnemy].rect.x, self.enemy[self.lockedEnemy].rect.y),
                                        30.0)))
                self.bulletCount -= 1
            '''temp code'''
            if event.key == self.keyBindings[13]:
                self.lockedEnemy = (self.lockedEnemy + 1) % len(self.enemy)
            '''temp code'''
            if event.key == self.keyBindings[9]:
                self.attacks[self.slot]()
            '''Change - Slot'''
            if event.key == self.keyBindings[5]:
                self.slot = (self.slot + 1) % len(self.attacks)
            elif event.key == self.keyBindings[6]:
                self.slot = (self.slot - 1) % len(self.attacks)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Bullet
            if self.mouse[2] and not self.lock[0] and self.bulletCount > 0:
                projectiles.bullets(self.group[1], creator=self, vel=(self.transform(pygame.mouse.get_pos(), 30.0)))
                self.bulletCount -= 1

    def meleeAttack(self, aType: bool):
        # aType true means heavy attack false means light attack
        for i in self.enemy:
            if self.facing and 0 < i.rect.x - self.rect.x < 100 and abs(self.rect.y - i.rect.y) < 200:
                if aType:
                    i.damage(int(30 * self.data.damageMultiplier))
                    print('[player]: heavy')
                else:
                    i.damage(int(10 * self.data.damageMultiplier))
                    print('[player]: light')
            elif not self.facing and 0 > i.rect.x - self.rect.x > -100 and abs(self.rect.y - i.rect.y) < 200:
                if aType:
                    i.damage(int(30 * self.data.damageMultiplier))
                    print('[player]: heavy')
                else:
                    i.damage(int(10 * self.data.damageMultiplier))
                    print('[player]: light')

    def dashAttack(self):
        if self.magicBar.currentLevel() >= 30:
            self.tangible = False
            self.dashing = True
            self.velocity[0] = (lambda x: 20 if x else -20)(self.facing)
            self.magicBar.decrease(30)

    def chargedAttack(self):
        if self.magicBar.currentLevel() >= 40:
            if abs(self.rect.x - self.enemy[self.lockedEnemy].rect.x) < 100:
                self.enemy[self.lockedEnemy].damage(int(30 * self.data.damageMultiplier) * 2)
            print('[Player]: Charged Attack Success')
            self.magicBar.decrease(40)

    def whirlWindStrike(self):
        if self.magicBar.currentLevel() >= 30:
            for i in self.group[0]:
                if isinstance(i, EnemyAI) and abs(self.rect.x - i.rect.x) < 150:
                    i.damage(int(30 * self.data.damageMultiplier), int(10 * self.data.stunMultiplier))
            print('[Player]: Whirl Wind Attack Success')
            self.magicBar.decrease(30)


class EnemyAI(combatEntity):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        # self.image = pygame.transform.scale(pygame.image.load('assets/enemy.png'), self.rect.size)
        self.idleAnimate = ssmanager.getOther('assets/Enemy-Dark_Wraith/idle.png', (255, 255, 255), (500, 100), 4,
                                              gc.playerSize, True)
        # somewhat working animation
        self.image = self.idleAnimate[0]
        self.i = 0
        self.rect.x = 500
        self.walking = False
        self.invisibleRect = pygame.rect.Rect(self.rect.x - 50, self.rect.y, 225, self.rect.height)
        self.player = None

        self.healthBar = screenElements.healthBar(self.group, entity=self,
                                                  position=(),
                                                  colors=(gc.color['GREEN'], gc.color["RED"]),
                                                  size=(gc.playerSize[0], 5), maxL=self.health)

        '''Get player'''
        for i in self.group[0]:
            if i != self:
                self.player = i
                break

    def update(self, *args, ):
        self.image = pygame.transform.flip(self.idleAnimate[self.i // 10], not self.facing, False)
        self.i = (self.i + 1) % (10 * (len(self.idleAnimate)))

        self.rect = self.rect.move(self.velocity)
        '''Randomly Shoot towards player'''
        if not self.stunBar.currentLevel(0):
            if random.randint(0, 5000) < 3:
                self.shootPlayer()
            if random.randint(0, 10) == 3:
                self.walking = not self.walking
            if self.rect.x > gc.screenSize[0] - 100 or self.rect.x < 100:
                if random.randint(0, 1):
                    self.walking = False
                else:
                    self.moveInDirection(not self.facing)

            '''Orient Self facing towards player'''
            if self.player.rect.x > self.rect.x:
                self.facing = True
            else:
                self.facing = False

            '''Check player too close - then attack'''
            if self.invisibleRect.colliderect(self.player.rect) and random.randint(0, 10) == 1:
                x = random.randint(0, 100)
                if x < 10:
                    self.attackPlayerHeavyDash()
                elif 25 < x < 50:
                    self.attackPlayerLight()

            '''Slow itself'''
            if not self.walking:
                self.slowDown()
            else:
                self.moveInDirection(not self.facing)

            self.invisibleRect.x, self.invisibleRect.y = self.rect.x - self.rect.width, self.rect.y
            if self.tangible and self.player.tangible:
                if self.rect.colliderect(self.player.rect):
                    if self.rect.x > self.player.rect.x:
                        self.rect.x = self.player.rect.x + self.rect.width
                    else:
                        self.rect.x = self.player.rect.x - self.rect.width
                    self.velocity[0] = 0
                    if random.randint(0, 10) == 3:
                        projectiles.forceField(self.group[1], creator=self, direction=self.facing, pushvel=25, damage=5)
                    if random.randint(0, 10) == 2:
                        if not self.jumping:
                            self.velocity[1] = -15
                            self.jumping = True
                        self.moveInDirection(self.facing)
        else:
            self.velocity[0] = 0
        super(EnemyAI, self).update()

    def shootPlayer(self):
        if self.player is None:
            return
        projectiles.bullets(self.group[1], creator=self,
                            vel=self.transform((self.player.rect.x, self.player.rect.y), 30.0))

    def moveInDirection(self, direction, vel=0):
        if direction is None:
            return
        if self.velocity[0] != 0:
            return
        if vel == 0:
            if direction:
                self.velocity[0] = -10
            else:
                self.velocity[0] = +10
        else:
            if direction:
                self.velocity[0] = -vel
            else:
                self.velocity[0] = +vel

    def attackPlayerHeavyDash(self):
        x = random.randint(0, 10)
        if x != 1:
            return
        elif not self.player.blocking:  # TODO: Add player stun
            self.tangible = False
            self.moveInDirection(not self.facing, 30)
            self.player.damage(30, 10)
            print('[Enemy]: Heavy Attack')

    def attackPlayerLight(self):
        x = random.randint(0, 10)
        if x != 1:
            return
        elif not self.player.blocking:
            self.moveInDirection(not self.facing)
            self.player.damage(30, 5)
            print('[Enemy]: Light Attack')

    def slowDown(self):
        if self.velocity[0] > 0:
            self.velocity[0] -= 1
        elif self.velocity[0] < 0:
            self.velocity[0] += 1
        else:
            self.tangible = True

    def distanceFromPlayer(self, outFormat=''):
        x_ = self.player.rect.x - self.rect.x
        y_ = self.player.rect.y - self.rect.y
        if outFormat == 'x':
            return x_
        elif outFormat == 'y':
            return y_
        else:
            return x_, y_

    def damage(self, hit, stun=0):
        super(EnemyAI, self).damage(hit, stun)
        if random.randint(0, 120) == 1:
            collectibles.healthBoost(self.group, floor=self.platform, pos=(self.rect.x, self.rect.y),
                                     dire=not self.facing,
                                     player=self.player)

    def kill(self):
        self.healthBar.kill()
        super(EnemyAI, self).kill()


class smallFlyingEnemySpawner(EnemyAI):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        self.rect.y = 200
        self.finalPos = 0
        self.image = pygame.transform.scale(pygame.image.load('assets/bird.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.group = groups
        self.player = None
        for i in self.group[0]:
            if i != self:
                self.player = i
                break
        self.replicate = deltaTime()
        self.health = 150
        self.healthBar.maxlevel = self.health
        self.flip = False

    def update(self, *args):
        if self.replicate.delta(5000) and smallFlyingEnemySpawned.count < 20:
            smallFlyingEnemySpawned(*self.group, ssmanager=self.sSManager,
                                    platform=self.platform, time=self.clock, x=self.rect.x)
        self.rect.y = 100 + 5 * math.sin((pygame.time.get_ticks() % 43200) // 120)
        if self.rect.x != self.finalPos:
            if self.rect.x < self.finalPos:
                self.rect.x += 2
                if self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = False

            else:
                self.rect.x -= 2
                if not self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = True
        else:
            self.finalPos = random.randint(5, 370) * 2
        if self.health <= 0:
            self.kill()


class smallFlyingEnemySpawned(EnemyAI):
    count = 0

    def __init__(self, *groups, ssmanager, platform, time, x):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        smallFlyingEnemySpawned.count += 1
        self.finalPos = 0
        self.image = pygame.transform.scale(pygame.image.load('assets/bird.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.y = 200
        self.rect.x = x
        self.group = groups
        self.player = None
        for i in self.group[0]:
            if i != self:
                self.player = i
                break
        self.health = 40
        self.healthBar.maxlevel = self.health
        self.flip = False

    def update(self, *args):
        self.rect.y = 100 + 5 * math.sin((pygame.time.get_ticks() % 43200) // 120)
        if self.rect.x != self.finalPos:
            if self.rect.x < self.finalPos:
                self.rect.x += 2
                if self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = False

            else:
                self.rect.x -= 2
                if not self.flip:
                    self.image = pygame.transform.flip(self.image, True, False)
                    self.flip = True
        else:
            self.finalPos = random.randint(5, 370) * 2
        if not random.randint(0, 50):
            projectiles.bullets(self.group[1], creator=self,
                                vel=self.transform((self.player.rect.x, self.player.rect.y), 30.0))
        if self.health <= 0 or self.player is None:
            smallFlyingEnemySpawned.count -= 1
            self.kill()
