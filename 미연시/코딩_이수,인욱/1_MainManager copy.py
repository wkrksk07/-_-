import string
from tkinter.messagebox import NO
import pygame

########################################################################
#기본 초기화(반드시 해야하는 것들)

pygame.init() #초기화

#화면 크기
screen_width = 1366
screen_height = 768
screen = pygame.display.set_mode((screen_width,screen_height))

#화면 타이틀
pygame.display.set_caption("코딩의 노예들")

#FPS
clock = pygame.time.Clock()

#
########################################################################

# 1. 사용자 게임 초기화( 배경화면, 게임 이미지, 좌표, 속도, 폰트 등 )

# 배경 이미지 불러오기
background = pygame.image.load("C:/Users/VVIP/Documents/GitHub/MyComputerLanguageStudy/Python\Make the Game/PyGame_NadoCoding_2/Img/BackGround.png")

#Player 스프라이트 불러오기
Player = pygame.image.load("C:/Users/VVIP/Documents/GitHub/MyComputerLanguageStudy/Python\Make the Game/PyGame_NadoCoding_2/Img/Player.png")
Player_size = Player.get_rect().size #이미지 크기
Player_width = Player_size[0] #캐릭터 가로
Player_height = Player_size[1] #케릭터 세로
Player_x_pos = (screen_width / 2) - (Player_width/2) #화면 가로의 절반 크기에 해당하는 곳에 위치
Player_y_pos = screen_height - Player_height

#이동 좌표
to_x = 0
to_y = 0

#이동속도
Player_Speed = 0.75

#적 캐릭터
Enemy = pygame.image.load("C:/Users/VVIP/Documents/GitHub/MyComputerLanguageStudy/Python\Make the Game/PyGame_NadoCoding_2/Img/Player.png")
Enemy_size = Player.get_rect().size #이미지 크기
Enemy_width = Player_size[0] #캐릭터 가로
Enemy_height = Player_size[1] #케릭터 세로
Enemy_x_pos = (screen_width / 2) - (Enemy_width/2) #화면 가로의 절반 크기에 해당하는 곳에 위치
Enemy_y_pos = (screen_height / 2) - (Enemy_height/2)

# 폰트 정의
game_font = pygame.font.Font(None, 40)#폰트 객체생성(폰트, 크기)

#총 시간
total_time = 10

#시간 계산
start_ticks = pygame.time.get_ticks()#시작 tick을 받아옴

#이벤트 루프
running = True #게임이 진행중인가
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임


    for event in pygame.event.get(): #어떤 이벤트가 발생했는가
        if event.type == pygame.QUIT: #창위 X = 닫기 눌렀을때
            running = False #게임 진행중 아님

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                to_x -= Player_Speed
            elif event.key == pygame.K_RIGHT:
                to_x += Player_Speed
            elif event.key == pygame.K_UP:
                to_y -= Player_Speed
            elif event.key == pygame.K_DOWN:
                to_y += Player_Speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                to_x = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                to_y = 0

    Player_x_pos += to_x * dt
    Player_y_pos += to_y * dt

    #가로 경계값
    if Player_x_pos <0:
        Player_x_pos = 0
    elif Player_x_pos > screen_width - Player_width:
        Player_x_pos = screen_width - Player_width

    #세로 경계값
    if Player_y_pos <0:
        Player_y_pos = 0
    elif Player_y_pos > screen_height - Player_height:
        Player_y_pos = screen_height - Player_height

    #충돌 처리를 위한 rect 업데이트 함수
    Player_rect = Player.get_rect()
    Player_rect.left = Player_x_pos
    Player_rect.top = Player_y_pos

    Enemy_rect = Enemy.get_rect()
    Enemy_rect.left = Enemy_x_pos
    Enemy_rect.top = Enemy_y_pos

    screen.blit(background,(0, 0)) #배경 그리기
    screen.blit(Player, (Player_x_pos,Player_y_pos))#캐릭터 그리기
    
    screen.blit(Enemy, (Enemy_x_pos, Enemy_y_pos))#적 그리기

    #타이머 계산

    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 #경과 시간(ms)을 1000으로 나누어서 초 단위로 표시

    timer = game_font.render(str(int(total_time - elapsed_time)), True, (0,0,0)) #출력할 글자, True, 글자색상
    screen.blit(timer,(10,10))

    #충돌 체크
    if Player_rect.colliderect(Enemy_rect) or total_time <= 0:
        print('충돌')
        running = False
    
    pygame.display.update()#게임화면호출

#잠시 대기
pygame.time.delay(2000) #2초 정도 대기(ms)

# 게임 종료
pygame.quit()