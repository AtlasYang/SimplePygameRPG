#coding: utf-8
#==========================================================#
# RPG Project by GAY Gil Mo - From August 1st.            #
# All Rights reserved                                      #
#==========================================================#

# Basic Declaring zone
import numpy as np
import pygame, sys, time, random, math, threading
import pickle as pkl
from pygame.locals import *
pygame.init()
FPS = 20
fpsClock = pygame.time.Clock()

ATEAM = 'a team'
BTEAM = 'b team'

BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
AQUA = (0,125,255)
GREEN = (0,128,0)

LEFTP = 1
RIGHTP = 3

RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

K_W = ord('w')
K_A = ord('a')
K_S = ord('s')
K_D = ord('d')
K_Q = ord('q')
K_E = ord('e')
K_F = ord('f')

LEFTP = 1
RIGHTP = 3

K_W = ord('w')
K_A = ord('a')
K_S = ord('s')
K_D = ord('d')

BASICATTACK = 'basicattack'
MOVINGSKILL = 'movingskill'
ATTACKSKILL = 'attackskill'
FREESKILL = 'freeskill'
DEFENSESKILL = 'defenseskill'

get_tick = pygame.time.get_ticks

WIDTH = 1240
HEIGHT = 840
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('RPG')

Charlist = []  #움직이는 모든 캐릭터의 리스트
Imagelist = []  #기타 그래픽 (direction이 없음. timeout과 step이 있음) 리스트

active = {                   #메인 루프에서 사용할 리스트
        BASICATTACK : False,
        MOVINGSKILL : False,
        DEFENSESKILL : False,
        ATTACKSKILL : False,
        FREESKILL : False
    }
# Basic Declaring zone end

#basic function area
def distanceof(crd1, crd2):
    distance = math.sqrt(((crd1[0]-crd2[0])**2)+((crd1[1]-crd2[1])**2))
    return distance

def rectof(obj):
    rect = pygame.image.fromstring(obj.image[obj.direction][obj.imgcnt], obj.size, obj.image_encoding).get_rect()
    x, y = obj.pos[0], obj.pos[1]
    res = pygame.Rect(x, y, rect.width, rect.height)
    return res

def iscollided(obj1, obj2):
    obj1rect = pygame.image.fromstring(obj1.image[obj1.direction][obj1.imgcnt], obj1.size, obj1.image_encoding).get_rect()
    obj2rect = pygame.image.fromstring(obj2.image[obj2.direction][obj2.imgcnt], obj2.size, obj2.image_encoding).get_rect()
    rect1 = pygame.Rect(obj1.pos[0], obj1.pos[1], obj1rect.width, obj1rect.height)
    rect2 = pygame.Rect(obj2.pos[0], obj2.pos[1], obj2rect.width, obj2rect.height)
    return rect1.colliderect(rect2)

def get_text(text, size=20, color=BLACK):
    font = pygame.font.SysFont("comicsansms", size)
    t = font.render(text, True, color)
    return t

def draw_grass():
    grassimg = pygame.image.load('images\grass.jpg')
    for i in range(0, WIDTH + 1, 45):
        for j in range(0, HEIGHT + 1, 45):
            DISPLAYSURF.blit(grassimg, (i, j))


#basic function area end


#monster class
#몹들은 인공지능 구현 필요
class Monster():
    def __init__(self):
        self.inventory = []
        self.radiation = False
        self.team = BTEAM
        self.HP = 50
        self.AP = 100
        self.DP = 0
        self.SP = 5
        self.RIGHT = False
        self.LEFT = False
        self.UP = False
        self.DOWN = False
        self.direction = DOWN
        self.pos = [500, 500]
        self.time = get_tick()
        self.cooltime = 2
        self.image_encoding = 'RGBA'

    def attack(self):
        while True:
            for character in Charlist:
                if not character == self:
                    if iscollided(self, character):
                        now = get_tick()
                        if now - self.time >= self.cooltime*1000:
                            if character.team == ATEAM:
                                if not self.AP - character.DP < 0:
                                    character.HP -= self.AP - character.DP
                                    self.time = now

class Skeleton(Monster):
    def __init__(self):
        super().__init__()
        self.name = 'Skeleton'
        self.HP = 1500000
        self.imgcnt= 0
        self.image = {
            RIGHT : [],
            LEFT : [],
            UP : [],
            DOWN : []
        }
        for i in range(1, 17):
            if i<10:
                filename = 'images\Skeleton_00' + str(i) + '.png'
            else:
                filename = 'images\Skeleton_0' + str(i) + '.png'
            if i<5:
                self.image[DOWN].append(pygame.image.load(filename))
            elif i>4 and i<9:
                self.image[LEFT].append(pygame.image.load(filename))
            elif i>8 and i<13:
                self.image[RIGHT].append(pygame.image.load(filename))
            else:
                self.image[UP].append(pygame.image.load(filename))

        self.size = (self.image[self.direction][self.imgcnt].get_rect().width, self.image[self.direction][self.imgcnt].get_rect().height)

        for i in range(len(self.image[RIGHT])):
            a = pygame.image.tostring(self.image[RIGHT][i], self.image_encoding)
            self.image[RIGHT][i] = a
        for i in range(len(self.image[LEFT])):
            a = pygame.image.tostring(self.image[LEFT][i], self.image_encoding)
            self.image[LEFT][i] = a
        for i in range(len(self.image[UP])):
            a = pygame.image.tostring(self.image[UP][i], self.image_encoding)
            self.image[UP][i] = a
        for i in range(len(self.image[DOWN])):
            a = pygame.image.tostring(self.image[DOWN][i], self.image_encoding)
            self.image[DOWN][i] = a







#monster class end


#character class
class Character():
    def __init__(self):
        self.team = ATEAM
        self.inventory = []   #inventory 에는 Item/Weapon클래스의 인스턴스가 들어간다
        self.HP = 50
        self.AP = 10
        self.DP = 0
        self.SP = 5
        self.RIGHT = False
        self.LEFT = False
        self.UP = False
        self.DOWN = False
        self.direction = DOWN
        self.pos = [0, 0]
        self.image_encoding = 'RGBA'
        self.time = {
            BASICATTACK : get_tick(),
            MOVINGSKILL : get_tick(),
            DEFENSESKILL : get_tick(),
            ATTACKSKILL : get_tick(),
            FREESKILL : get_tick()
        }
        self.cooltime = {
            BASICATTACK : 1,
            MOVINGSKILL : 7,
            DEFENSESKILL : 10,
            ATTACKSKILL : 12,
            FREESKILL : 25
        }
        self.skillActive = {
            BASICATTACK : False,
            MOVINGSKILL : False,
            DEFENSESKILL : False,
            ATTACKSKILL : False,
            FREESKILL : False
        }

    def AdaptInventoryItems(self):   #인벤토리에 있는 아이템들을 플레이어의 능력치에 적용
        for item in self.inventory:
            self.AP += item.AP
            self.DP += item.DP
            self.HP += item.HP

    def move(self, dir):
        if dir == RIGHT:
            self.pos[0] += self.SP
        elif dir == LEFT:
            self.pos[0] -= self.SP
        elif dir == UP:
            self.pos[1] -= self.SP
        elif dir == DOWN:
            self.pos[1] += self.SP

    def BasicAttack(self):
        pass

    def MovingSkill(self, distance):
        pass

    def DefenseSkill(self):
        pass

    def AttackSkill(self):
        pass

    def FreeSkill(self):
        pass

    def PassiveSkill(self):
        pass


class Heal():
    def __init__(self, obj):
        self.obj = obj
        self.timeout = 7
        self.time = get_tick()
        self.imgcnt = 0
        self.image = []
        for i in range(1, 13):
            if i<10:
                filename = 'images/Heal_00{0}.png'.format(str(i))
            else:
                filename = 'images/Heal_0{0}.png'.format(str(i))
            t = pygame.image.load(filename)
            self.image.append(t)
        self.pos = [-999, -999]

    def step(self):
        self.imgcnt = (self.imgcnt + 1)%12

    def update_pos(self, obj):
        t = rectof(obj).center
        rect = self.image[self.imgcnt].get_rect()
        rect.center = t
        pos = rect.x, rect.y
        self.pos = pos

    def alert(self):
        self.obj.SP -= 5
        self.obj.DP /= 3
        self.obj.time[DEFENSESKILL] = get_tick()


class Knight(Character):  #기사는 체력과 방어력이 가장 높으며, 공격력도 준수하고, 속도도 빠른 편이다. 공격속도는 느린 편이다.
    def __init__(self):
        super().__init__()
        self.name = 'Knight'
        self.AP = 120
        self.DP = 50
        self.HP = 1000
        self.SP = 10
        self.HPrate = 10
        self.APrate = 3
        self.DPrate = 5
        self.imgcnt= 0
        self.image = {
            RIGHT : [],
            LEFT : [],
            UP : [],
            DOWN : []
        }
        for i in range(1, 17):
            if i<10:
                filename = 'images\Knight_00' + str(i) + '.png'
            else:
                filename = 'images\Knight_0' + str(i) + '.png'
            if i<5:
                self.image[DOWN].append(pygame.image.load(filename))
            elif i>4 and i<9:
                self.image[LEFT].append(pygame.image.load(filename))
            elif i>8 and i<13:
                self.image[RIGHT].append(pygame.image.load(filename))
            else:
                self.image[UP].append(pygame.image.load(filename))

        self.size = (self.image[self.direction][self.imgcnt].get_rect().width, self.image[self.direction][self.imgcnt].get_rect().height)


        for i in range(len(self.image[RIGHT])):
            a = pygame.image.tostring(self.image[RIGHT][i], self.image_encoding)
            self.image[RIGHT][i] = a
        for i in range(len(self.image[LEFT])):
            a = pygame.image.tostring(self.image[LEFT][i], self.image_encoding)
            self.image[LEFT][i] = a
        for i in range(len(self.image[UP])):
            a = pygame.image.tostring(self.image[UP][i], self.image_encoding)
            self.image[UP][i] = a
        for i in range(len(self.image[DOWN])):
            a = pygame.image.tostring(self.image[DOWN][i], self.image_encoding)
            self.image[DOWN][i] = a


        self.cooltime = {
            BASICATTACK : 1,
            MOVINGSKILL : 7,
            DEFENSESKILL : 10,
            ATTACKSKILL : 12,
            FREESKILL : 60
        }

    def BasicAttack(self):   #기사는 적에 충돌하면 공격한다(근거리)
        for character in Charlist:
            if not character == self:
                if iscollided(self, character):
                    now = get_tick()
                    if now - self.time[BASICATTACK] >= self.cooltime[BASICATTACK]*1000:
                        character.HP -= self.AP - character.DP
                        self.time[BASICATTACK] = now

    def MovingSkill(self):     #주변의 적이 모두 멈추고 5번 이동한다.
        now = get_tick()
        if now - self.time[MOVINGSKILL] >= self.cooltime[MOVINGSKILL]*1000:
            for i in range(25):
                self.move(self.direction)
            self.time[MOVINGSKILL] = now

    def DefenseSkill(self):
        now = get_tick()
        if now - self.time[DEFENSESKILL] >= self.cooltime[DEFENSESKILL]*1000:
            self.DP *= 3
            self.SP += 5
            heal = Heal(self)
            Imagelist.append(heal)

    def AttackSkill():
        pass
        #발키리 평타

    def FreeSkill():
        pass
        #주변 8개의 공간에 장벽 설치 (시간 제한)


class Poison():
    def __init__(self, obj):
        self.obj = obj
        self.timeout = 15
        self.time = get_tick()
        self.damagecnt = 0
        self.imgcnt = 0
        self.image = []
        for i in range(1, 26):
            if i<10:
                filename = 'images/poison2_00{0}.png'.format(str(i))
            else:
                filename = 'images/poison2_0{0}.png'.format(str(i))
            t = pygame.image.load(filename)
            self.image.append(t)
        self.pos = [-999, -999]

    def step(self):
        self.imgcnt = (self.imgcnt + 1)%25

    def update_pos(self, obj):
        self.damagecnt = (self.damagecnt + 1)%15
        t = rectof(self.obj).center
        rect = self.image[self.imgcnt].get_rect()
        rect.center = t
        pos = rect.x, rect.y
        self.pos = pos
        if self.damagecnt == 1:
            self.obj.HP -= obj.AP * 0.5

    def alert(self):
        self.obj.radiation = False


class Sheild():
    def __init__(self, obj):
        self.obj = obj
        self.timeout = 10
        self.time = get_tick()
        self.imgcnt = 0
        self.image = []
        for i in range(1, 21):
            if i<10:
                filename = 'images/magic_00{0}.png'.format(str(i))
            else:
                filename = 'images/magic_0{0}.png'.format(str(i))
            t = pygame.image.load(filename)
            self.image.append(t)

        self.pos = [-999, -999]

    def step(self):
        self.imgcnt = (self.imgcnt + 1)%20

    def update_pos(self, obj):
        t = rectof(obj).center
        rect = self.image[self.imgcnt].get_rect()
        rect.center = t
        pos = rect.x, rect.y
        self.pos = pos

    def alert(self):
        self.obj.time[DEFENSESKILL] = get_tick()
        self.obj.DP -= 99999


class Radiation():
    def __init__(self, obj):
        self.obj = obj
        self.width = 300
        self.height = self.width
        self.num = 0
        self.num2 = 50
        self.num2dir = UP
        self.timeout = 15
        self.time = get_tick()
        self.imgcnt = 0
        self.image = [pygame.Surface((self.width, self.height), pygame.SRCALPHA), ]
        self.image[0].fill((0, 234, 0, self.num2))
        self.pos = [-999, -999]

    def step(self):
        self.num = (self.num + 1) % 12
        rect = self.image[0].get_rect()
        rect.move_ip(self.pos[0], self.pos[1])
        for char in Charlist:
            if not char == self.obj:
                if rectof(char).colliderect(rect):
                    if self.num == 1:
                        char.HP -= self.obj.AP
                        if char.radiation == False:
                            char.radiation = True
                            t = Poison(char)
                            Imagelist.append(t)

    def update_pos(self, obj):
        self.pos = [self.obj.pos[0] - self.width/2 + self.obj.size[0]/2, self.obj.pos[1] - self.height/2 + self.obj.size[1]/2]
        if self.num2dir == UP:
            self.num2 += 10
        else:
            self.num2 -= 10
        if self.num2 >= 130:
            self.num2dir = DOWN
        if self.num2 <= 50:
            self.num2dir = UP
        self.image[0].fill((0, 234, 0, self.num2))

    def alert(self):
        self.obj.time[FREESKILL] = get_tick()
        self.obj.skillActive[FREESKILL] = False
        self.obj.AP /= 4


class Plasma():
    def __init__(self, obj):
        self.obj = obj
        self.timeout = 5
        self.time = get_tick()
        self.imgcnt = 0
        self.image = []
        for i in range(1, 17):
            if i<10:
                filename = 'images/plasma_00{0}.png'.format(str(i))
            else:
                filename = 'images/plasma_0{0}.png'.format(str(i))
            t = pygame.image.load(filename)
            self.image.append(t)

        self.pos = [-999, -999]

    def step(self):
        self.imgcnt = (self.imgcnt + 1)%16

    def update_pos(self, obj):
        t = rectof(obj).center
        rect = self.image[self.imgcnt].get_rect()
        rect.center = t
        pos = rect.x, rect.y
        self.pos = pos

    def alert(self):
        self.obj.time[ATTACKSKILL] = get_tick()
        self.obj.AP /= 6




class Scientist(Character):  #과학자는 체력과 방어력이 매우 낮지만 강력한 플라즈마 공격과 과충전을 통한 유연한 스킬 사용이 가능하다.
    def __init__(self):
        super().__init__()
        self.name = 'Scientist'
        self.HP = 450
        self.DP = 35
        self.range = 200
        self.AP = 2
        self.HPcnt = 0
        self.SP = 9
        self.HPrate = 4
        self.APrate = 2.5
        self.DPrate = 1
        self.imgcnt= 0
        self.image = {
            RIGHT : [],
            LEFT : [],
            UP : [],
            DOWN : []
        }
        for i in range(1, 17):
            if i<10:
                filename = 'images\Scientist_00' + str(i) + '.png'     
            else:
                filename = 'images\Scientist_0' + str(i) + '.png'
            if i<5:
                self.image[DOWN].append(pygame.image.load(filename))
            elif i>4 and i<9:
                self.image[LEFT].append(pygame.image.load(filename))
            elif i>8 and i<13:
                self.image[RIGHT].append(pygame.image.load(filename))
            else:
                self.image[UP].append(pygame.image.load(filename))

        self.size = (self.image[self.direction][self.imgcnt].get_rect().width, self.image[self.direction][self.imgcnt].get_rect().height)


        for i in range(len(self.image[RIGHT])):
            a = pygame.image.tostring(self.image[RIGHT][i], self.image_encoding)
            self.image[RIGHT][i] = a
        for i in range(len(self.image[LEFT])):
            a = pygame.image.tostring(self.image[LEFT][i], self.image_encoding)
            self.image[LEFT][i] = a
        for i in range(len(self.image[UP])):
            a = pygame.image.tostring(self.image[UP][i], self.image_encoding)
            self.image[UP][i] = a
        for i in range(len(self.image[DOWN])):
            a = pygame.image.tostring(self.image[DOWN][i], self.image_encoding)
            self.image[DOWN][i] = a

        self.cooltime = {
            BASICATTACK : 0,
            MOVINGSKILL : 0,
            DEFENSESKILL : 20,
            ATTACKSKILL : 25,
            FREESKILL : 65
        }

    def BasicAttack(self):
        now = get_tick()
        if now - self.time[BASICATTACK] >= self.cooltime[BASICATTACK]*1000:
            if not len(Charlist)==1:
                distance = 99999999999
                target = None
                for i in range(len(Charlist)):
                    if not len(Charlist) == 1:
                        if not Charlist[i]==self:
                            if not Charlist[i].team == ATEAM:
                                if distanceof(self.pos, Charlist[i].pos)<distance and distanceof(self.pos, Charlist[i].pos) <= self.range:
                                    distance = distanceof(self.pos, Charlist[i].pos)
                                    target = Charlist[i]
                                    target_rect = rectof(target)
                                    self_rect = rectof(self)
                                    color = AQUA
                                    if self.skillActive[FREESKILL]:
                                        color = GREEN
                                    pygame.draw.circle(DISPLAYSURF, color, self_rect.center, random.randint(7, 9))
                                    pygame.draw.line(DISPLAYSURF, color, target_rect.center, self_rect.center, random.randint(10, 15))
                                    target.HP -= self.AP  #과학자의 공격은 방어력을 무시하며, 무작위적인 공격력을 가진다
                                    self.time[BASICATTACK] = now

    def MovingSkill(self):
        now = get_tick()
        if now - self.time[MOVINGSKILL] >= self.cooltime[MOVINGSKILL]*1000:
            self.time[MOVINGSKILL] = get_tick()
            self.time[DEFENSESKILL] -= self.cooltime[DEFENSESKILL]*1000
            self.time[ATTACKSKILL] -= self.cooltime[ATTACKSKILL]*1000
            self.time[FREESKILL] -= self.cooltime[FREESKILL]*1000   #궁극기는 나중에 뺌

    def DefenseSkill(self):
        now = get_tick()
        if now - self.time[DEFENSESKILL] >= self.cooltime[DEFENSESKILL]*1000:
            sheild = Sheild(self)
            self.DP += 99999
            Imagelist.append(sheild)

    def AttackSkill(self):
        now = get_tick()
        if now - self.time[ATTACKSKILL] >= self.cooltime[ATTACKSKILL]*1000:
            plasma = Plasma(self)
            self.AP *= 6
            Imagelist.append(plasma)

    def FreeSkill(self):
        now = get_tick()
        if now - self.time[FREESKILL] >= self.cooltime[FREESKILL]*1000:
            self.skillActive[FREESKILL] = True
            self.AP *= 4
            radiation = Radiation(self)
            Imagelist.append(radiation)

    def PassiveSkill(self):
        self.HPcnt = (self.HPcnt+1)%15
        if self.HPcnt == 1:
            self.HP += 1


class Fireball():
    def __init__(self, obj, pos):
        self.obj = obj
        self.objpos = obj.pos
        self.target = pos
        self.timeout = 1.92
        self.time = get_tick()
        self.num = 0
        self.cnt = 0
        self.imgcnt = 0
        self.image = []
        for i in range(1, 8):
            if i<10:
                filename = 'images/fireball_00{0}.png'.format(str(i))
            else:
                filename = 'images/fireball_0{0}.png'.format(str(i))
            t = pygame.image.load(filename)
            self.image.append(t)

        self.pos = [-999, -999]

    def f(self, x):
        a, b, c, d = self.objpos[0], self.objpos[1], self.target[0], self.target[1]
        grad = (b - d) / (a - c)
        y_inter = (a*d - b*c) / (a - c)
        return grad*x + y_inter

    def step(self):
        if self.num == 11:
            self.imgcnt = (self.imgcnt + 1)%8
            self.num = 0
        else:
            self.num += 1
        self.cnt += 1

    def update_pos(self, dummy):
        if self.objpos[0] < self.target[0]:
            x = self.cnt*10 + self.objpos[0]
        else:
            x = self.objpos[0] - self.cnt*10
        y = self.f(x)
        self.pos = [x, y]

    def alert(self):
        self.obj.time[ATTACKSKILL] = get_tick()



class Mage(Character):  #마법사는 강력한 광역공격을 사용하며, 불사조를 소환하여 공격한다. 체력과 방어력이 떨어지는 편이다.
    def __init__(self):
        super().__init__()
        self.HP = 500
        self.SP = 9
        self.DP = 30
        self.AP = 10
        self.name = 'Mage'
        self.HPrate = 3.5
        self.APrate = 7
        self.DPrate = 1
        self.imgcnt= 0
        self.image = {
            RIGHT : [],
            LEFT : [],
            UP : [],
            DOWN : []
        }
        for i in range(1, 17):
            if i<10:
                filename = 'images\Mage_00' + str(i) + '.png'
            else:
                filename = 'images\mage_0' + str(i) + '.png'
            if i<5:
                self.image[DOWN].append(pygame.image.load(filename))
            elif i>4 and i<9:
                self.image[LEFT].append(pygame.image.load(filename))
            elif i>8 and i<13:
                self.image[RIGHT].append(pygame.image.load(filename))
            else:
                self.image[UP].append(pygame.image.load(filename))

        self.size = (self.image[self.direction][self.imgcnt].get_rect().width, self.image[self.direction][self.imgcnt].get_rect().height)


        for i in range(len(self.image[RIGHT])):
            a = pygame.image.tostring(self.image[RIGHT][i], self.image_encoding)
            self.image[RIGHT][i] = a
        for i in range(len(self.image[LEFT])):
            a = pygame.image.tostring(self.image[LEFT][i], self.image_encoding)
            self.image[LEFT][i] = a
        for i in range(len(self.image[UP])):
            a = pygame.image.tostring(self.image[UP][i], self.image_encoding)
            self.image[UP][i] = a
        for i in range(len(self.image[DOWN])):
            a = pygame.image.tostring(self.image[DOWN][i], self.image_encoding)
            self.image[DOWN][i] = a

        self.cooltime = {
            BASICATTACK : 1.2,
            MOVINGSKILL : 15,
            DEFENSESKILL : 20,
            ATTACKSKILL : 0,
            FREESKILL : 50
        }

    def BasicAttack(self):
        pass

    def MovingSkill():
        pass
        #공격속도가 매우 빨라짐

    def DefenseSkill():
        pass

    def AttackSkill(self, target):
        now = get_tick()
        if now - self.time[ATTACKSKILL] >= self.cooltime[ATTACKSKILL]*1000:
            fireball = Fireball(self, target)
            Imagelist.append(fireball)

    def FreeSkill():
        pass
        #피닉스 소환


class Assasin(Character): #암살자는 광역공격이 불가능하지만 속도가 빠르고 공격력과 공격 속도가 높으며, 순간이동을 사용한다.
    def __init__(self):
        super().__init__()
        self.name = 'Assasin'
        self.HPrate = 4.7
        self.APrate = 7.5
        self.DPrate = 1.2
        self.AP = 150
        self.DP = 25
        self.HP = 750
        self.SP = 11
        self.imgcnt= 0
        self.image = {
            RIGHT : [],
            LEFT : [],
            UP : [],
            DOWN : []
        }
        for i in range(1, 17):
            if i<10:
                filename = 'images\Assasinator_00' + str(i) + '.png'
            else:
                filename = 'images\Assasinator_0' + str(i) + '.png'
            if i<5:
                self.image[DOWN].append(pygame.image.load(filename))
            elif i>4 and i<9:
                self.image[LEFT].append(pygame.image.load(filename))
            elif i>8 and i<13:
                self.image[RIGHT].append(pygame.image.load(filename))
            else:
                self.image[UP].append(pygame.image.load(filename))

        self.size = (self.image[self.direction][self.imgcnt].get_rect().width, self.image[self.direction][self.imgcnt].get_rect().height)


        for i in range(len(self.image[RIGHT])):
            a = pygame.image.tostring(self.image[RIGHT][i], self.image_encoding)
            self.image[RIGHT][i] = a
        for i in range(len(self.image[LEFT])):
            a = pygame.image.tostring(self.image[LEFT][i], self.image_encoding)
            self.image[LEFT][i] = a
        for i in range(len(self.image[UP])):
            a = pygame.image.tostring(self.image[UP][i], self.image_encoding)
            self.image[UP][i] = a
        for i in range(len(self.image[DOWN])):
            a = pygame.image.tostring(self.image[DOWN][i], self.image_encoding)
            self.image[DOWN][i] = a

        self.cooltime = {
            BASICATTACK : 0.7,
            MOVINGSKILL : 3,
            DEFENSESKILL : 20,
            ATTACKSKILL : 10,
            FREESKILL : 20
        }

    def BasicAttack(self):
        self.team = ATEAM
        for character in Charlist:
            if not character == self:
                if iscollided(self, character):
                    now = get_tick()
                    if now - self.time[BASICATTACK] >= self.cooltime[BASICATTACK]*1000:
                        character.HP -= self.AP - character.DP
                        self.time[BASICATTACK] = now

    def MovingSkill(self):
        self.team = ATEAM
        now = get_tick()
        if now - self.time[MOVINGSKILL] >= self.cooltime[MOVINGSKILL]*1000:
            if self.direction == RIGHT:
                self.pos[0] += 120
            elif self.direction == LEFT:
                self.pos[0] -= 120
            elif self.direction == UP:
                self.pos[1] -= 120
            else:
                self.pos[1] += 120

            self.time[MOVINGSKILL] = now

    def DefenseSkill(self):
        now = get_tick()
        if now - self.time[DEFENSESKILL] >= self.cooltime[DEFENSESKILL]*1000:
            self.team = BTEAM
            self.time[DEFENSESKILL] = now


    def AttackSkill(self):
        self.team = ATEAM
        #질풍참

    def FreeSkill(self):
        self.team = ATEAM
        #가까운 적으로 이동

#character class end



#weapon class
#weapon class end

#main loop


mainChar = Scientist()
Mob = Skeleton()
Charlist.append(mainChar)
Charlist.append(Mob)

t = threading.Thread(target = Mob.attack, args = ())
t.start()

def main():
    num = 0
    while True:
        for char in Charlist:
            if char.HP <=0:
                Charlist.remove(char)
        for item in Imagelist:
            now = get_tick()
            if now - item.time >= item.timeout*1000:
                item.alert()
                Imagelist.remove(item)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key in (K_UP, K_W):
                    mainChar.UP = True
                elif event.key in (K_LEFT, K_A):
                    mainChar.LEFT = True
                elif event.key in (K_DOWN, K_S):
                    mainChar.DOWN = True
                elif event.key in (K_RIGHT, K_D):
                    mainChar.RIGHT = True
                elif event.key == K_Q:
                    active[FREESKILL] = True
                elif event.key == K_F:
                    active[ATTACKSKILL] = True
                elif event.key == K_E:
                    active[DEFENSESKILL] = True
                elif event.key == K_LSHIFT:
                    active[MOVINGSKILL] = True

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if mainChar.name == 'Mage':
                        if active[ATTACKSKILL]:
                            mainChar.AttackSkill(event.pos)
                    else:
                        active[BASICATTACK] = True
                if event.button == 3:
                    active[DEFENSESKILL] = True

            if event.type == MOUSEBUTTONUP:
                if event.button==1:
                    active[BASICATTACK] = False
                if event.button == 3:
                    active[DEFENSESKILL] = False

            if event.type == KEYUP:
                if event.key in (K_UP, K_W):
                    mainChar.UP = False
                elif event.key in (K_LEFT, K_A):
                    mainChar.LEFT = False
                elif event.key in (K_DOWN, K_S):
                    mainChar.DOWN = False
                elif event.key in (K_RIGHT, K_D):
                    mainChar.RIGHT = False
                elif event.key == K_E:
                    active[DEFENSESKILL] = False
                elif event.key == K_F:
                    active[ATTACKSKILL] = False
                elif event.key == K_Q:
                    active[FREESKILL] = False
                elif event.key == K_LSHIFT:
                    active[MOVINGSKILL] = False

        if mainChar.UP == True:
            mainChar.pos[1] -= mainChar.SP
            mainChar.direction = UP
            mainChar.imgcnt = (mainChar.imgcnt+1)%4
        elif mainChar.LEFT == True:
            mainChar.pos[0] -= mainChar.SP
            mainChar.direction = LEFT
            mainChar.imgcnt = (mainChar.imgcnt+1)%4
        elif mainChar.DOWN == True:
            mainChar.pos[1] += mainChar.SP
            mainChar.direction = DOWN
            mainChar.imgcnt = (mainChar.imgcnt+1)%4
        elif mainChar.RIGHT == True:
            mainChar.pos[0] += mainChar.SP
            mainChar.direction = RIGHT
            mainChar.imgcnt = (mainChar.imgcnt+1)%4

        draw_grass()
        mainChar.PassiveSkill()

        for char in Charlist:
            img = pygame.image.fromstring(char.image[char.direction][char.imgcnt], char.size, char.image_encoding)
            DISPLAYSURF.blit(img, char.pos)

        for item in Imagelist:
            DISPLAYSURF.blit(item.image[item.imgcnt], item.pos)
            item.update_pos(mainChar)
            item.step()


        #서버 데이터 전송을 위해 Charlist 의 객체에서 필요한 요소만을 따로 저장한다. 데이터 전송 존
        #Sendlist = []
        #for char in Charlist:
            #t = {}
            #t['name'] = char.name
            #t['pos'] = char.pos
            #t['direction'] = char.direction
            #t['imgcnt'] = char.imgcnt
            #t['HP'] = char.HP
            #t['AP'] = char.AP
            #t['SP'] = char.SP
            #t['DP'] = char.DP
            #t['inventory'] = char.inventory
            #Sendlist.append(t)


        #데이터 전송 코드 끝

        #텍스트 테스트 존(슨)
        gg = mainChar.team
        now = get_tick()
        t1 = {}
        t1[BASICATTACK] = int((now - mainChar.time[BASICATTACK]) / 1000)
        t1[MOVINGSKILL] = int((now - mainChar.time[MOVINGSKILL]) / 1000)
        t1[DEFENSESKILL] = int((now - mainChar.time[DEFENSESKILL]) / 1000)
        t1[ATTACKSKILL] = int((now - mainChar.time[ATTACKSKILL]) / 1000)
        t1[FREESKILL] = int((now - mainChar.time[FREESKILL]) / 1000)
        ggg = t1
        b = get_text(str(ggg))

        DISPLAYSURF.blit(get_text(str(mainChar.HP) + '   '+str(Mob.HP)), (0, 0))
        DISPLAYSURF.blit(b, (200, 0))
        #텍스트 테스트 코드 끝

        if active[BASICATTACK]:
            mainChar.BasicAttack()
        if active[FREESKILL]:
            mainChar.FreeSkill()
        if active[ATTACKSKILL]:
            if not mainChar.name == 'Mage':
                mainChar.AttackSkill()
        if active[DEFENSESKILL]:
            mainChar.DefenseSkill()
        if active[MOVINGSKILL]:
            mainChar.MovingSkill()

        pygame.display.update()
        fpsClock.tick(FPS)
        print(num)
        num += 1

if __name__ == '__main__':
    main()
