import pygame
import random

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()

def create_building():
    random_building_pos = random.choice(building_height)
    bottom_building = building_surface.get_rect(midtop=(500, random_building_pos))
    top_building = building_surface.get_rect(midtop=(500, random_building_pos - 650))
    return bottom_building, top_building

def create_coin():
    random_building_pos = random.choice(building_height)
    coin_rect = coin_surface.get_rect(midtop=(700, random_building_pos - 100))
    return coin_rect

def move_building(buildings):
    for building in buildings:
        building.centerx -= 4
    return buildings

def move_coins(coins):
    for coin in coins:
        coin.centerx -= 4
    return coins

def draw_building(buildings):
    for building in buildings:
        if building.bottom >= 600:
            screen.blit(building_surface, building)
        else:
            flip_building = pygame.transform.flip(building_surface, False, True)
            screen.blit(flip_building, building)

def draw_coins(coins):
    for coin in coins:
        screen.blit(coin_surface, coin)

def check_collision(buildings, coins):
    global score
    for building in buildings:
        if drone_hcn.colliderect(building):
            hit_sound.play()
            return False

    for coin in coins:
        if drone_hcn.colliderect(coin):
            coins.remove(coin)
            score += 1
            score_sound.play()

    if drone_hcn.top <= -75 or drone_hcn.bottom >= 600:
        return False
    return True

def rotate_drone(drone1):
    new_drone = pygame.transform.rotozoom(drone1, -drone_y * 10, 1)
    return new_drone

def score_view(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(f'Score: ${int(score)}', True, (255, 0, 0))
        score_rect = score_surface.get_rect(center=(100, 20))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: ${int(score)}', True, (255, 0, 0))
        score_rect = score_surface.get_rect(center=(100, 20))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: ${int(high_score)}', True, (255, 0, 0))
        high_score_rect = score_surface.get_rect(center=(200, 750))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
#Khai báo các biến
score = 0
high_score = 0
p = 0.05
drone_y = 0
game_active = False  # đưa giá trị đầu của hoạt động game là false
splash_screen = True
running=True
fl_x=0
coin_list = []
building_list = []
building_height = [200, 300, 400] 
game_font = pygame.font.Font(r'C:\python game\game1\04B_19.TTF', 40)
pygame.display.set_caption('Flappy Drone')
clock = pygame.time.Clock()
#Tạo background và floor
bg = pygame.image.load(r'C:\python game\game1\Blue and Yellow Neon Retro Pixel Art Game Night Game Presentation (2).png')
fl = pygame.image.load(r'C:\python game\game1\assets\81.png')
fl = pygame.transform.scale2x(fl)
bg = pygame.transform.scale2x(bg)
lockscreen=pygame.image.load(r'C:\python game\game1\Blue and Yellow Neon Retro Pixel Art Game Night Game Presentation (3).png')
#biểu tượng của game
icon = pygame.image.load(r'C:\python game\game1\assets\15.png')
pygame.display.set_icon(icon)
#tạo drone
drone = pygame.image.load(r'C:\python game\game1\assets\15.png')
drone = pygame.transform.scale2x(drone)
drone_hcn = drone.get_rect(center=(100, 384))
#tạo hình tòa nhà
building_surface = pygame.image.load(r'C:\python game\game1\assets\4.png')
building_surface = pygame.transform.scale2x(building_surface)
#tạo timer 
spawnbuilding = pygame.USEREVENT 
pygame.time.set_timer(spawnbuilding, 1200) # sau 1.2 s sẽ xuất hiện tòa nhà
screen = pygame.display.set_mode((432, 768))
#tạo hình đồng xu
coin_surface = pygame.image.load(r'C:\python game\game1\coin.png')
#màn hình game over
game_over_surface = pygame.image.load(r'C:\python game\game1\assets\FL (580 x 840 px) (290 x 420 px) (3).png')
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center=(216, 384))
#âm thanh
flap_sound = pygame.mixer.Sound(r'C:\python game\game1\sound\sfx_wing.wav')
hit_sound = pygame.mixer.Sound(r'C:\python game\game1\sound\sfx_hit.wav')
score_sound = pygame.mixer.Sound(r'C:\python game\game1\sound\sfx_point.wav')
score_sound_countdown = 100
# Splash screen loop
while splash_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            splash_screen = False
            running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            splash_screen = False
            game_active = True  # Start the game

    # Display splash screen graphics
    screen.blit(lockscreen, (0, 0))
    pygame.display.update()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                drone_y -= 5
                flap_sound.play()

            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                building_list.clear()
                coin_list.clear()
                drone_hcn.center = (100, 384)
                drone_y = 0
                score = 0

        if event.type == spawnbuilding:
            building_list.extend(create_building())
            coin_list.append(create_coin())

    screen.blit(bg, (0, 0))
    screen.blit(fl, (fl_x, 600))
    screen.blit(fl, (fl_x + 432, 600))
    if game_active:
        game_active = check_collision(building_list, coin_list)

        building_list = move_building(building_list)
        draw_building(building_list)

        coin_list = move_coins(coin_list)
        draw_coins(coin_list)

        score += 0.01
        score_view('main game')
        score_sound_countdown -= 1

        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_view('game_over')
    fl_x -= 1
    if fl_x == -432:
        fl_x = 0

    rotated_drone = rotate_drone(drone)
    screen.blit(rotated_drone, drone_hcn)

    drone_y += p
    drone_hcn.centery += drone_y

    pygame.display.update()
    clock.tick(100)


