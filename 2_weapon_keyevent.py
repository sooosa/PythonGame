from email.mime import image
import os
import pygame

pygame.init()  #초기화 (반드시 필요)

 #화면 크기 설정 
screen_width = 640  #가로 크기
screen_height = 480 #세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("Pang") # 게임 이름

#FPS
clock = pygame.time.Clock()
###############################################

#1.사용자 게임 초기화 (배경화면, 게임 이미지, 좌표, 속도, 폰트등)

#배경 이미지 불러오기
current_path = os.path.dirname(__file__)#현재 파일의 위치 변환 
image_path = os.path.join(current_path,"images") #image 폴더 위차 반환

#배경만들기 
background = pygame.image.load(os.path.join(image_path,"background.png"))
#스테이지 만들기 
stage = pygame.image.load(os.path.join(image_path,"stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

#배경 이미지 불러오기
character = pygame.image.load(os.path.join(image,"character.png"))
character_size = character.get_rect().size #이미지의 크기를 구해옴
character_width = character_size[0] #캐릭터의 가로 크기
character_height = character_size[1] #캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2)    #화면 가로의 절반 크기에 해당하는 곳에 위치(가로)
character_y_pos = screen_height  - character_height  #화면 세로 크기 가장 아래 에 해당하는 곳에 위치
#캐릭터 이동 방향
character_to_x = 0
#이동 속도
character_speed = 5
# 무기
weapon = pygame.image.load(os.path.join(image_path,"weapon.png")) 
weapon_size =weapon.get_rect().size
weapon_width = weapon_size[0] 

#무기는 한번에 여러 발 발사 가능 
weapons = []

#무기 이동 속도 
weapons_speed = 10

#이벤트 루프
running = True #게임이 진행중인가?
while running:
    dt = clock.tick(30) #게임화면의 초당 프레임 수를 설정

    #캐릭터가 1초동안에 100 만큼 이동을 해야함
    #10 fps :1초 동안에 10번동작   -> 1번에 몇 만큼 이동? 10만큼! 10*10 = 100
    #20 fps :1초 동안에 20번동작   -> 1번에 몇 만큼 이동? 5만큼! 20*5 = 100

    print("fps : " + str(clock.get_fps()))
    # 2.이벤트 처리 (키보드, 마우스등)
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False #게임이 진행중이 아님
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽 으로 이동 
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT: 
                character_speed += character_speed
            elif event.key == pygame.K_SPACE: #무기 발사
               weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
               weapon_y_pos = character_y_pos
               weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
       
    #3.게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos  = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
  
    #무기 위치 조정 
    #100,200 -> 180,160,140....
    #500,200 -> 180,160,140....
    weapons = [ [w[0], w[1] - weapons_speed] for w in weapons] #무기 위치를 위로

    #천장에 닿은 무기 없애기
    weapons = [[w[0],w[1]]for w in weapons if w[1] > 0]

    #4.충돌 처리 
    

    
    #5.화면에 그리기
    screen.blit(background, (0,0)) #배경 그리기

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon,(weapon_x_pos, weapon_y_pos))

    screen.blit(stage,(0,screen_height-screen_height)) #스테이지 그리기
    screen.blit(character,(character_x_pos, character_y_pos))

    
    
    pygame.display.update() #게임화면 다시그리기

#잠시 대기 
pygame.time.delay(2000) #2초 정도 대기 (ms)  

# pygame 종료
pygame.quit()