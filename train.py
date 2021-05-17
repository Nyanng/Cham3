import numpy as np
import cv2
import pygame as pyg
import search
import time
import threading
import random

playing = True
is_ingame = False
result = 'NONE'
set_profile = 'easy'
difficult_profile = {
    'easy': [
        60, 80, 100
    ],
    'hard': [
        30, 90, 100
    ],
    'extreme': [
        5, 55, 100
    ]
}

# Image Object
# left = pyg.image.load("./img/left.png")
# left_rect = left.get_rect()
# right = pyg.image.load("./img/right.webp")
# right_rect = right.get_rect()

# init
screen = pyg.display.set_mode((1280, 720))
screen.fill((255, 255, 255))

pyg.init()

# Text
font = pyg.font.SysFont('applesdgothicneo', 30)
font_lg = pyg.font.SysFont('applesdgothicneo', 50)
title_text = font_lg.render("AI와 한판하는 참참참", True, (10, 120, 150))
press_x_key = font.render(
    "Extreme 난이도를 시작하려면 X를 눌러주세요.", True, (155, 15, 15))
press_h_key = font.render("Hard 난이도를 시작하려면 H를 눌러주세요.", True, (230, 60, 35))
press_e_key = font.render("Easy 난이도를 시작하려면 E를 눌러주세요.", True, (35, 170, 15))
game_start_text = {
    'easy': font.render("Easy 참참참을 시작합니다!", True, (0, 0, 0)),
    'hard': font.render("Hard 참참참을 시작합니다!", True, (0, 0, 0)),
    'extreme': font.render("Extreme 참참참을 시작합니다!", True, (0, 0, 0)),
}
ready_text = font.render("준비하세요!", True, (0, 0, 0))
ccc_text = font.render("참 참 참!", True, (0, 0, 0))
you_win_text = font.render("내가 이겼다!", True, (10, 215, 145))
ai_win_text = font.render("AI가 이겼다...", True, (90, 40, 170))
error_text = font.render("참참참 막대를 인식할 수 없어요 !!", True, (255, 0, 0))

# Sound Object
start_sound = pyg.mixer.Sound('./sound/start.mp3')
ready_sound = pyg.mixer.Sound('./sound/ready.mp3')
ccc_sound = pyg.mixer.Sound('./sound/ccc.mp3')
aiwin_sound = pyg.mixer.Sound('./sound/aiwin.mp3')
youwin_sound = pyg.mixer.Sound('./sound/youwin.mp3')
error_sound = pyg.mixer.Sound('./sound/error.mp3')


def refresh_result():
    global result
    while playing:
        result, _frame = search.update_result()
        # frame = cv2.cvtColor(_frame, cv2.COLOR_BGR2RGB)
        # frame = frame.swapaxes(0, 1)
        # cv2.imshow("dbg window", frame)


def ready():
    screen.blit(title_text, (20, 20))
    screen.blit(press_x_key, (20, 100))
    screen.blit(press_h_key, (20, 140))
    screen.blit(press_e_key, (20, 180))


def game_init(profile):
    global is_ingame, set_profile
    is_ingame = True
    set_profile = profile


def ingame():
    global is_ingame, result, set_profile

    screen.fill((255, 255, 255))
    pyg.display.update()

    start_sound.play()
    screen.blit(game_start_text[set_profile], (20, 20))
    pyg.display.update()
    time.sleep(3)

    ready_sound.play()
    screen.blit(ready_text, (20, 60))
    pyg.display.update()
    time.sleep(2)

    ccc_sound.play()
    screen.blit(ccc_text, (20, 100))
    pyg.display.update()
    time.sleep(2.1)

    if(result == '찾을 수 없음'):
        error_sound.play()
        screen.blit(error_text, (20, 220))
        pyg.display.update()

        print(f'[{set_profile}] you:{result} ai:- result:cancel')
        is_ingame = False
        time.sleep(2)

        return

    your_result = result
    rand = random.randrange(1, 100)

    if(rand <= difficult_profile[set_profile][0]):
        ai_result = your_result
    elif(rand <= difficult_profile[set_profile][1]):
        if(your_result == '오른쪽'):
            ai_result = '왼쪽'
        elif(your_result == '왼쪽'):
            ai_result = '오른쪽'
        elif(your_result == '중앙'):
            ai_result = '오른쪽'
    elif(rand <= difficult_profile[set_profile][2]):
        if(your_result == '오른쪽'):
            ai_result = '중앙'
        elif(your_result == '왼쪽'):
            ai_result = '중앙'
        elif(your_result == '중앙'):
            ai_result = '왼쪽'

    screen.blit(font.render("나의 방향  :  " + your_result,
                True, (10, 135, 215)), (20, 220))
    screen.blit(font.render("AI의 방향  :  " + ai_result,
                True, (10, 135, 215)), (20, 260))
    pyg.display.update()

    time.sleep(0.7)

    if(your_result == ai_result):
        screen.blit(you_win_text, (20, 310))
        youwin_sound.play()
    else:
        screen.blit(ai_win_text, (20, 310))
        aiwin_sound.play()

    print(f'[{set_profile}] you:{your_result} ai:{ai_result} result:{your_result == ai_result}')

    pyg.display.update()

    is_ingame = False


threading.Thread(target=refresh_result).start()

while playing:
    # debug
    # search.update_result()
    screen.fill((255, 255, 255))

    for event in pyg.event.get():
        if event.type == pyg.KEYDOWN:
            if(event.key == pyg.K_x):
                game_init('extreme')
            elif(event.key == pyg.K_h):
                game_init('hard')
            elif(event.key == pyg.K_e):
                game_init('easy')

    if(not is_ingame):
        ready()
    else:
        ingame()
        time.sleep(3.5)

    pyg.display.update()

pyg.quit()
