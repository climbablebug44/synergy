import pygame
import random
from CombatSystem import projectiles, collectibles, gameConstants as gc


class attackCooldown:
    def __init__(self, cooldown, prevTime, currLevel, maxLevel):
        self.cooldown = cooldown
        self.prevTime = prevTime
        self.currLevel = currLevel
        self.d = maxLevel

    def checkCooldown(self, cldwn=-1):
        if cldwn != -1:
            check = cldwn
        else:
            check = self.cooldown
        time = pygame.time.get_ticks()
        if time - self.prevTime > check:
            self.prevTime = time
            return True
        else:
            return False

    def gradualIncrease(self, k):
        self.currLevel += k
        if self.currLevel > self.d:
            self.currLevel = self.d

    def fill(self):
        self.currLevel = self.d


class combatEntity(pygame.sprite.Sprite):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups)
        self.clock = time
        self.gravity = 1
        self.sSManager = ssmanager
        self.velocity = [0, 0]
        self.health = 375
        self.jumping = True
        self.blocking = False
        self.facing = True
        self.tangible = True
        self.rect = pygame.Rect(0, 0, gc.playerSize[0], gc.playerSize[1])
        self.platform = platform
        self.group = groups
        self.stun = attackCooldown(100, pygame.time.get_ticks(), 100, 100)

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
        if self.stun.currLevel == 0 and self.stun.checkCooldown(cldwn=3000):
            self.stun.fill()
        ''' Gravity Code'''
        if self.rect.colliderect(self.platform) and self.rect.y >= self.platform.y - gc.playerSize[1]:
            self.jumping = False
            self.rect.y = self.platform.y - gc.playerSize[1]
            self.velocity[1] = 0
        elif self.jumping:
            self.velocity[1] += self.gravity
        '''/Gravity code'''

        '''L-R bounds'''
        if self.rect.x < 0:
            self.rect.x = 0
            if self.velocity[0] != 0:
                if self.stun.currLevel > 5:
                    self.stun.currLevel -= 5
        if self.rect.x > gc.screenSize[0] - gc.playerSize[0]:
            self.rect.x = gc.screenSize[0] - gc.playerSize[0]
            if self.stun.currLevel > 5:
                self.stun.currLevel -= 5
        '''/bounds'''

        if self.health <= 0:
            self.kill()

    def damage(self, hit):
        if not self.blocking or self.stun.currLevel == 0:
            self.health -= hit
            if self.health > 375:
                self.health = 375
            elif self.health < 0:
                self.health = 0

    def eventHandle(self, event=None):
        pass
        ''' 
            Used in player class
            to update only when an event occurs
            Has no use here
        '''


class player(combatEntity):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        self.image = pygame.transform.scale(pygame.image.load('assets/player.png'), gc.playerSize)
        self.moveX = 6
        self.moveY = 20
        self.magicBar = attackCooldown(100, pygame.time.get_ticks(), 100, 100)
        self.healthRect = pygame.Rect(self.rect.x, self.rect.y, 100, 5)
        self.enemy = None
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pressed()
        self.attacks = [self.chargedAttack, self.rushAttack, self.whirlWindStrike, self.magicWeapon]
        self.slot = 0
        # Call an attack: self.attacks[i]()

    def updateHealthBar(self):
        del self.healthRect
        self.healthRect = pygame.Rect(self.rect.x, self.rect.y - 10, self.health // 5, 5)

    def update(self):
        self.rect = self.rect.move(self.velocity)
        # remove this later
        self.health = 100
        if self.enemy is None:
            for i in self.group[0]:
                if i != self and isinstance(i, EnemyAI):
                    self.enemy = i
                    break
        self.updateHealthBar()

        '''Magic Bar fills'''
        if self.magicBar.checkCooldown():
            self.magicBar.gradualIncrease(1)

        if self.velocity[0] == 0:
            self.movement()
        else:
            if self.velocity[0] > 0:
                self.velocity[0] -= 1
            else:
                self.velocity[0] += 1

        '''Super Call'''
        super(player, self).update()

    def movement(self):
        moveFr, moveBa = True, True
        if self.tangible:
            if self.enemy.rect.colliderect(self.rect):
                if self.rect.x > self.enemy.rect.x:
                    moveBa = False
                elif self.rect.x < self.enemy.rect.x:
                    moveFr = False

        if self.keys[pygame.K_d] and moveFr:
            self.rect.x += self.moveX
            self.facing = True
        if self.keys[pygame.K_a] and moveBa:
            self.rect.x -= self.moveX
            self.facing = False
        if self.keys[pygame.K_b]:
            self.blocking = True
        else:
            self.blocking = False
            if self.keys[pygame.K_SPACE] and not self.jumping:
                self.velocity[1] -= self.moveY
                self.jumping = True

    def eventHandle(self, event=None):
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and self.magicBar.currLevel > 20:
                # Force Field
                projectiles.forceField(self.group[1], creator=self, direction=self.facing)
                projectiles.forceField(self.group[1], creator=self, direction=not self.facing)
                self.magicBar.currLevel -= 20
            if event.key == pygame.K_w:
                self.slot = (self.slot + 1) % 4
            elif event.key == pygame.K_s:
                self.slot = (self.slot - 1) % 4
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Bullet
            if self.mouse[2]:
                projectiles.bullets(self.group[1], creator=self,
                                    vel=(self.transform(pygame.mouse.get_pos(), 30.0)))
            elif self.mouse[0]:
                self.meleeAttack(True)

    def meleeAttack(self, aType: bool):
        # aType true means heavy attack false means light attack
        if self.facing and 0 < self.enemy.rect.x - self.rect.x < 100:
            if aType:
                self.enemy.damage(20)
                print('player: heavy')
            else:
                self.enemy.damage(10)
                print('player light')
        elif not self.facing and 0 > self.enemy.rect.x - self.rect.x > -100:
            if aType:
                self.enemy.damage(20)
                print('player: heavy')
            else:
                self.enemy.damage(10)
                print('player light')

    def chargedAttack(self):
        pass

    def rushAttack(self):
        pass

    def whirlWindStrike(self):
        pass

    def magicWeapon(self):
        pass


class EnemyAI(combatEntity):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        self.image = pygame.transform.scale(pygame.image.load('assets/enemy.png'), (75, 150))
        self.rect.x = 500
        self.walking = False
        self.invisibleRect = pygame.rect.Rect(self.rect.x - 50, self.rect.y, 225, gc.playerSize[1])
        self.player = None
        self.healthRect = pygame.rect.Rect(20, 20, (self.health / 375) * 700, 10)
        self.stunRect = pygame.rect.Rect(20, 50, (self.health / 100) * 600, 10)
        '''Get player'''
        for i in self.group[0]:
            if i != self:
                self.player = i
                break

    def update(self, *args, ):
        self.rect = self.rect.move(self.velocity)
        self.healthRect = pygame.rect.Rect(20, 20, (self.health / 375) * 750, 10)
        self.stunRect = pygame.rect.Rect(70, 40, (self.stun.currLevel / 100) * 600, 5)
        '''Randomly Shoot towards player'''
        if self.stun.currLevel > 0:
            if random.randint(0, 200) < 3:
                self.shootPlayer()
            if random.randint(0, 100) == 3:
                self.walking = not self.walking

            if self.rect.x > 700 or self.rect.x < 100:
                if random.randint(0, 1):
                    self.walking = False
                else:
                    self.moveInDirection(not self.facing)

            '''Orient Self facing towards player'''
            if self.player.rect.x > self.rect.x:
                self.facing = True
            else:
                self.facing = False

            '''Check player too close'''
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

            self.invisibleRect.x, self.invisibleRect.y = self.rect.x - 75, self.rect.y
            if self.tangible:
                if self.rect.colliderect(self.player.rect):
                    if self.rect.x > self.player.rect.x:
                        self.rect.x = self.player.rect.x + 75
                    else:
                        self.rect.x = self.player.rect.x - 75
                    self.velocity[0] = 0
                    if random.randint(0, 10) == 3:
                        projectiles.forceField(self.group[1], creator=self, direction=self.facing, pushvel=25, damage=5)
                    if random.randint(0, 10) == 2:
                        if not self.jumping:
                            self.velocity[1] = -15
                            self.jumping = True
                        self.moveInDirection(self.facing)

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
        elif not self.player.blocking or self.player.stun.currLevel < 20:
            self.player.stun.currLevel = 0
            self.tangible = False
            self.moveInDirection(not self.facing, 30)
            self.player.damage(30)
            print('[Enemy]: Heavy Attack')

    def attackPlayerLight(self):
        x = random.randint(0, 10)
        if x != 1:
            return
        elif not self.player.blocking:
            self.moveInDirection(not self.facing)
            self.player.damage(30)
            print('[Enemy]: Light Attack')

    def slowDown(self):
        if self.velocity[0] > 0:
            self.velocity[0] -= 1
        elif self.velocity[0] < 0:
            self.velocity[0] += 1
        else:
            self.tangible = True

    def distanceFromPlayer(self, Outformat=''):
        x_ = self.player.rect.x - self.rect.x
        y_ = self.player.rect.y - self.rect.y
        if Outformat == 'x':
            return x_
        elif Outformat == 'y':
            return y_
        else:
            return x_, y_

    def damage(self, hit):
        super(EnemyAI, self).damage(hit)
        self.stun.currLevel -= 10
        if self.stun.currLevel <= 0:
            self.stun.currLevel = 0
            self.stun.prevTime = pygame.time.get_ticks()
            # Refresh ticks
        if random.randint(0, 120) == 1:
            collectibles.healthBoost(self.group, floor=self.platform, pos=(self.rect.x, self.rect.y),
                                     dire=not self.facing,
                                     player=self.player)


class smallEnemy(EnemyAI):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        pass


class smallFlyingEnemy(EnemyAI):
    def __init__(self, *groups, ssmanager, platform, time):
        super().__init__(*groups, ssmanager=ssmanager, platform=platform, time=time)
        pass
