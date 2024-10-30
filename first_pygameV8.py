import pygame
from random import randint

def spawn_enemy(enemy_list, level):
    if enemy_list:
        if level == 1:
            for enemy_rect in enemy_list:
                enemy_rect.x -= 5          
                game_screen.blit(snail_surf, enemy_rect)      
                if enemy_rect.x < -100:
                    enemy_list.remove(enemy_rect)    
            return enemy_list
        elif level == 2:
            for enemy_rect in enemy_list:
                enemy_rect.x -= 5
                if enemy_rect.bottom == 300:
                    game_screen.blit(snail_surf, enemy_rect)     
                else:
                    game_screen.blit(fly_surf, enemy_rect)     
                if enemy_rect.x < -100:
                    enemy_list.remove(enemy_rect)
            return enemy_list
    return []

def player_animation():
    global player_surf1, player_surf2, p_animation 
    p_animation += 0.1
    if p_animation > 2:
        p_animation = 0
    if player_rect.bottom < 300:
        return player_jump
    elif p_animation < 1:
        return player_surf1
    else:
        return player_surf2

def enemy_animation():
    global snail_surf1, snail_surf2, e_animation
    global fly_surf1, fly_surf2
    e_animation += 0.05
    if e_animation > 2:
        e_animation = 0
    if e_animation < 1:
        return snail_surf1, fly_surf2
    else:
        return snail_surf2, fly_surf1
    
def collision_check(enemy_list):
    for enemy in enemy_list:
        if player_rect.colliderect(enemy):
            return True
    return False

#score fonksiyonu
def score():
    global cur_score, highest_score
    global my_font
    if player_rect.x > 0:
        cur_score += 0.01 * hardness
    if cur_score > highest_score:
        highest_score = cur_score
        #dosyaya yazma
        with open("Oyun dosyaları/score/highest_score.txt", "w") as file:
            file.write(str(int(highest_score)))
    score_surf = my_font.render(f"Score: {int(cur_score)}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 30))
    game_screen.blit(score_surf, score_rect)

pygame.init()

game_screen = pygame.display.set_mode((800, 400))
game_clock= pygame.time.Clock()

pygame.display.set_caption("First Pygame")

platform_surf=pygame.image.load("Oyun dosyaları/graphics/ground.png").convert_alpha()

sky_surf=pygame.image.load("Oyun dosyaları/graphics/Sky.png").convert_alpha()

player_surf1 = pygame.image.load("Oyun dosyaları/graphics/Player/player_walk_1.png").convert_alpha()
player_surf2 = pygame.image.load("Oyun dosyaları/graphics/Player/player_walk_2.png").convert_alpha()
player_jump = pygame.image.load("Oyun dosyaları/graphics/Player/jump.png").convert_alpha()
player_rect = player_surf1.get_rect(midbottom=(80, 300))
p_animation=0

char_surf=pygame.image.load("Oyun dosyaları/graphics/Player/player_stand.png").convert_alpha()
char_surf=pygame.transform.rotozoom(char_surf,0,2)
char_rect=char_surf.get_rect(center=(400,200))

skull_surf=pygame.image.load("Oyun dosyaları/graphics/skull.png").convert_alpha()
skull_rect=skull_surf.get_rect(center=(100,30))

fly_surf1=pygame.image.load("Oyun dosyaları/graphics/Fly/Fly1.png").convert_alpha()#yeni düşman resimleri
fly_surf2=pygame.image.load("Oyun dosyaları/graphics/Fly/Fly2.png").convert_alpha()
fly_rect=fly_surf1.get_rect(midbottom=(randint(900,1100),250))


snail_surf1 = pygame.image.load("Oyun dosyaları/graphics/snail/snail1.png").convert_alpha()
snail_surf2 = pygame.image.load("Oyun dosyaları/graphics/snail/snail2.png").convert_alpha()
snail_rect = snail_surf1.get_rect(midbottom=(750, 300))
e_animation=0

enemy_list = []

my_font = pygame.font.Font("Oyun dosyaları/font/Pixeltype.ttf", 50)
score_surf = my_font.render("Score : 0", False, "White")
score_rect = score_surf.get_rect(center=(400, 30))
pygame.draw.rect(game_screen, "#c0e8ec", score_rect, 100)

start_text=my_font.render("Press SPACE to start",False,"White")
start_rect=start_text.get_rect(center=(400,350))

speed_surf = pygame.image.load("Oyun dosyaları/graphics/speed.png").convert_alpha()
speed_transform = pygame.transform.scale2x(speed_surf)
speed_rect = speed_transform.get_rect(center=(700, 30))
pygame.draw.rect(game_screen, "#c0e8ec", speed_rect, 100)

gameover_sound=pygame.mixer.Sound("Oyun dosyaları/audio/game_over.wav")
jump_sound = pygame.mixer.Sound("Oyun dosyaları/audio/jump.mp3")
music = pygame.mixer.Sound("Oyun dosyaları/audio/music.wav")

gravity = 0
game_continiue = False
platform_speed=0
level = 1
hardness = 1
game_speed=1
cur_score=0 # gerekli değişkenler
try:#dosyadan okuma
    with open("Oyun dosyaları/score/highest_score.txt", "r") as file:
        highest_score = int(file.read())
except FileNotFoundError:
    highest_score = 0

spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, int(1500/hardness)) 

level_text=my_font.render(f"Level {level}",False,"Black")
level_rect=level_text.get_rect(center=(400,60))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_continiue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    jump_sound.play()
                    gravity = -12
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if speed_rect.collidepoint(event.pos):
                    if game_speed == 1:
                        game_speed = 2
                    else:
                        game_speed = 1
                if skull_rect.collidepoint(event.pos):
                    if hardness == 1:
                        hardness = 2
                    else:
                        hardness = 1
                    pygame.time.set_timer(spawn_timer, int(1500/hardness)) 
                    
            
            if event.type == spawn_timer:
                if level == 1:
                    enemy_list.append(snail_surf1.get_rect(midbottom=(randint(900, 1100), 300)))
                elif level == 2:
                    if randint(0, 1):
                        enemy_list.append(snail_surf1.get_rect(midbottom=(randint(900, 1100), 300)))
                    else:
                        enemy_list.append(fly_surf1.get_rect(midbottom=(randint(900, 1100), randint(100, 200))))
        
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    music.play(-1)
                    game_continiue = True
                    enemy_list.clear()

    if game_continiue:
        game_screen.blit(platform_surf, (platform_speed, 300))
        game_screen.blit(platform_surf, (platform_speed+600, 300))
        game_screen.blit(sky_surf, (platform_speed, 0))
        game_screen.blit(sky_surf, (platform_speed+600, 0))
        platform_speed-=3
        if platform_speed <= -600:
            platform_speed=0

        score()

        if cur_score>10:#level atlamak için
            level=2
        #level ekranda gösteriliyor
        level_text=my_font.render(f"Level: {level}",False,(64, 64, 64))
        game_screen.blit(level_text, level_rect)

        game_screen.blit(speed_transform, speed_rect)
        if(game_speed == 2):
            speed_rect2=speed_transform.get_rect(center=(750,30))
            game_screen.blit(speed_transform, speed_rect2)

        game_screen.blit(skull_surf, skull_rect)
        if(hardness == 2):
            skull_rect2=skull_surf.get_rect(center=(150,30))
            game_screen.blit(skull_surf, skull_rect2)
            
        player_surf = player_animation()
        game_screen.blit(player_surf, player_rect)

        gravity += 0.5
        player_rect.y += gravity

        if player_rect.bottom > 300:
            player_rect.bottom = 300

       
        enemy_list=spawn_enemy(enemy_list, level)
        snail_surf=enemy_animation()[0]
        fly_surf=enemy_animation()[1]

       
        if collision_check(enemy_list):
            gameover_sound.play()
            cur_score=0
            game_continiue = False
        
    else:
        music.fadeout(250)
        game_screen.fill((94,129,162))
        game_screen.blit(char_surf, char_rect)
        game_screen.blit(start_text, start_rect)
        #en yüksek scoru ekranda göster
        highest_score_text=my_font.render(f"Highest Score : {int(highest_score)}",False,"White")
        highest_score_rect=highest_score_text.get_rect(center=(400,50))
        game_screen.blit(highest_score_text, highest_score_rect)
        level=1

    pygame.display.update()
    game_clock.tick(60 * game_speed)
