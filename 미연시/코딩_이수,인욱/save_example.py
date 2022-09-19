import pygame, sys
import json

pygame.init()
screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 32)

#도형
red_surf = pygame.Surface([200,200])
red_surf.fill((240,80,54))
red_rect = red_surf.get_rect(center = (150,180))

blue_surf = pygame.Surface([200,200])
blue_surf.fill((0,123,194))
blue_rect = blue_surf.get_rect(center = (450,180))

#데이터
data = {
    'red' : 0,
    'blue' : 0
}

#아님말고 코드(이 코드가 없으면 clicker_score.txt 세이브 파일이 없을 경우 게임이 실행되지 않음)

try: #세이브파일이 있을 경우
    with open('clicker_score.txt') as score_file:
        data = json.load(score_file)
except: #세이브파일이 없을 경우
    print('No file created yet')

# 점수 표시
red_score_surf = game_font.render(f'Clicks: {data["red"]}', True, 'Black')
red_score_rect = red_score_surf.get_rect(center = (150, 320))

blue_score_surf = game_font.render(f'Clicks: {data["blue"]}', True, 'Black')
blue_score_rect = blue_score_surf.get_rect(center = (450, 320))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open('clicker_score.txt', 'w') as score_file: # 점수 세이브 파일을 생성
                json.dump(data,score_file) # data를 score_file에 써서 내보냄

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if red_rect.collidepoint(event.pos): # 빨간색 버튼을 누르면 빨강 점수가 올라감
                data['red'] += 1
                red_score_surf = game_font.render(f'Clicks: {data["red"]}', True, 'Black')
                red_score_rect = red_score_surf.get_rect(center = (150, 320))

            elif data['red'] >= 30: # 빨강 점수가 30점이 돼야 파란색 점수를 올릴 수 있음
                if blue_rect.collidepoint(event.pos):
                    data['blue'] += 1
                    blue_score_surf = game_font.render(f'Clicks: {data["blue"]}', True, 'Black')
                    blue_score_rect = blue_score_surf.get_rect(center = (450, 320))



        screen.fill((245,255,252))
        screen.blit(red_surf,red_rect)
        screen.blit(blue_surf,blue_rect)

        screen.blit(red_score_surf,red_score_rect)
        screen.blit(blue_score_surf,blue_score_rect)

        pygame.display.update()
        clock.tick(60)