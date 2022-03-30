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
character = pygame.image.load("C:/Python/character.png")
character_size = character.get_rect().size #이미지의 크기를 구해옴
character_width = character_size[0] #캐릭터의 가로 크기
character_height = character_size[1] #캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - (character_width / 2)    #화면 가로의 절반 크기에 해당하는 곳에 위치(가로)
character_y_pos = screen_height  - character_height  #화면 세로 크기 가장 아래 에 해당하는 곳에 위치

#이동할 좌표
to_x = 0
to_y = 0

#이동 속도
character_speed = 0.6

#적 enemy 캐릭터
enemy = pygame.image.load("C:/Python/enemy.png")
enemy_size = enemy.get_rect().size #이미지의 크기를 구해옴
enemy_width = enemy_size[0] #캐릭터의 가로 크기
enemy_height = enemy_size[1] #캐릭터의 세로 크기
enemy_x_pos = (screen_width /  2) - (enemy_width / 2)    #화면 가로의 절반 크기에 해당하는 곳에 위치(가로)
enemy_y_pos = (screen_height / 2) - (enemy_height / 2)  #화면 세로 크기 가장 아래 에 해당하는 곳에 위치


#폰트 정의 
game_font = pygame.font.Font(None,40) # 폰트 객체 생성 (폰트,크기)

#총 시간
total_time = 10

#시작 시간
start_ticks = pygame.time.get_ticks() # 시작 tick 을 받아옴


#이벤트 루프
running = True #게임이 진행중인가?
while running:
    dt = clock.tick(60) #게임화면의 초당 프레임 수를 설정

    #캐릭터가 1초동안에 100 만큼 이동을 해야함
    #10 fps :1초 동안에 10번동작   -> 1번에 몇 만큼 이동? 10만큼! 10*10 = 100
    #20 fps :1초 동안에 20번동작   -> 1번에 몇 만큼 이동? 5만큼! 20*5 = 100

    print("fps : " + str(clock.get_fps()))
    # 2.이벤트 처리 (키보드, 마우스등)
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False #게임이 진행중이 아님
        
        if event.type == pygame.KEYDOWN: # 키가 눌러 졌는지 확인 
            if event.key == pygame.K_LEFT: #캐릭터를 왼쪽으로 
               to_x -= character_speed #to_x = to_x - 5
            elif event.key == pygame.K_RIGHT: #캐릭터를 오른쪽으로 
                to_x += character_speed #to_x = to_x + 5 
            elif event.key == pygame.K_UP: #캐릭터를 위로
                to_y -= character_speed #to_y = to_y -5
            elif event.key == pygame.K_DOWN: #캐릭터를 아래로
                  to_y += character_speed #to_y = to_y +5
        
        if event.type == pygame.KEYUP: # 방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0
    #3.게임 캐릭터 위치 정의
    character_x_pos += to_x * dt
    character_y_pos += to_y * dt
    #가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos >  screen_width - character_width:
        character_x_pos =  screen_width - character_width
    #세로 경계값 처리    
    if character_y_pos < 0:
        character_y_pos =0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height
    
    #4.충돌 처리 
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌체크
    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False

    screen.blit(background, (0,0)) #배경 그리기

    screen.blit(stage,(0,screen_height-screen_height)) #스테이지 그리기

    screen.blit(enemy,(enemy_x_pos, enemy_y_pos)) #적 그리기

    #타이머 집어 넣기
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 
    # 경과 시간을 1000으로 나누어서 초 단위 표시
    
    timer = game_font.render(str(int(total_time - elapsed_time)), True,(255,255,255))
    # 출력할 글자, True, 글자색상
    screen.blit(timer,(10,10))

    # 만약시간이 0이하이면 게임 종료
    if total_time - elapsed_time <= 0:
        print("타임아웃")
        running = False 

    pygame.display.update() #게임화면 다시그리기

#잠시 대기 
pygame.time.delay(2000) #2초 정도 대기 (ms)  

# pygame 종료
pygame.quit()