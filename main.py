import os

import pygame
import random
import sys


# 객체 그리기
def paintEntity(entity, x, y):
    monitor.blit(entity, (int(x), int(y)))


# 점수 표시
def WriteScore(score):
    myfont = pygame.font.Font(os.path.join('venv', 'NanumGothic.ttf'), 18)
    txt = myfont.render('파괴한 우주선 수 : '+str(score), True, (255-r, 255-g, 255-b))
    monitor.blit(txt, (18, sHeight - 30))


def playGame():
    global monitor, ship, missile, monster
    global r, g, b

    # 배경 색
    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)

    shipX = sWidth / 2 + shipSize[0] / 2
    shipY = sHeight * 0.8
    dx, dy = 0, 0

    # 적 생김
    randImage = random.choice(monsterImage)
    monster = pygame.image.load(randImage)
    monsterSize = monster.get_rect().size  # 우주괴물 크기
    monsterX = 0
    monsterY = random.randrange(0, int(sWidth * 0.3))  # 상위 30% 위치까지만
    monsterSpeed = random.randrange(2, 5)

    # 미사일 위치 초기화
    missileX, missileY = None, None

    # 맞힌 미사일 수
    fireCount = 0

    while True:
        (pygame.time.Clock()).tick(60)
        monitor.fill((r, g, b))

        for e in pygame.event.get():
            if e.type in [pygame.QUIT]:
                pygame.quit()
                sys.exit()

            # 키 다운 이벤트, 우주선 이동 시작, 미사일 시작
            if e.type in [pygame.KEYDOWN]:
                if e.key == pygame.K_DOWN:
                    dy += 5
                elif e.key == pygame.K_UP:
                    dy += -5
                elif e.key == pygame.K_LEFT:
                    dx += -5
                elif e.key == pygame.K_RIGHT:
                    dx += 5
                elif e.key == pygame.K_SPACE:
                    if missileY is None:
                        missileX = shipX + shipSize[0] / 2
                        missileY = shipY

            # 키 업 이벤트, 우주선 이동 중지
            if e.type in [pygame.KEYUP]:
                if e.key == pygame.K_DOWN:
                    dy -= 5
                elif e.key == pygame.K_UP:
                    dy -= -5
                elif e.key == pygame.K_LEFT:
                    dx -= -5
                elif e.key == pygame.K_RIGHT:
                    dx -= 5

        # 우주선 이동 제한
        if 0 < shipX + dx <= sWidth - shipSize[0]:
            shipX += dx
        if sHeight / 2 < shipY + dy <= sHeight - shipSize[1]:
            shipY += dy

        paintEntity(ship, shipX, shipY)

        # 미사일 이동
        if missileY is not None:
            missileY -= 20
            if missileY < 0:
                missileY = None

        # 미사일 그리기
        if missileY is not None:
            paintEntity(missile, missileX, missileY)

            # 미사일 맞췄는지 확인
            if (monsterX < missileX < monsterX + monsterSize[0]) and \
                    (monsterY < missileY < monsterY + monsterSize[1]):
                fireCount += 1

                # 적 초기화
                monsterX = 0
                monsterY = random.randrange(0, int(sWidth * 0.3))
                # 우주괴물 이미지를 랜덤하게 선택한다.
                monster = pygame.image.load(random.choice(monsterImage))
                monsterSize = monster.get_rect().size
                monsterSpeed = random.randrange(2, 5)

                #미사일 초기화
                missileX, missileY = [None]*2

        # 적 움직임
        monsterX += monsterSpeed
        if monsterX > sWidth:
            monsterX = 0
            monsterY = random.randrange(0, int(sWidth * 0.3))
            # 우주괴물 이미지를 랜덤하게 선택한다.
            monster = pygame.image.load(random.choice(monsterImage))
            monsterSize = monster.get_rect().size
            monsterSpeed = random.randrange(2, 5)

        paintEntity(monster, monsterX, monsterY)

        WriteScore(fireCount)

        pygame.display.update()
        # print('~', end=' ')


# 전역변수
r, g, b = [0] * 3
sWidth, sHeight = 500, 700
monitor = None

shipSize = list()
ship = None

monsterImage = list()
monster = None

missile = None

# 메인 코드
pygame.init()
monitor = pygame.display.set_mode((sWidth, sHeight))
pygame.display.set_caption('우주괴물 무찌르기')

# 우주선
ship = pygame.image.load(os.path.join('venv\\image', 'ship02.png'))
shipSize = ship.get_rect().size

# 적
for i in range(1, 11):
    imageName = 'monster' + str(format('%02d' % i)) + '.png'
    monsterImage.append(os.path.join('venv\\image', imageName))
monster = pygame.image.load(monsterImage[0])

# 미사일
missile = pygame.image.load(os.path.join('venv\\image', 'missile.png'))

playGame()
