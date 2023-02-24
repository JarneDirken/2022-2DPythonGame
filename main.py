import pygame, sys, random

# To start using pygame
pygame.init()
pygame.font.init()

# Constant variables
FPS = 60
WIDTH, HEIGHT = 800, 600
VEL_PLAYER = 8
VEL_ENEMY = 5
LIGHT_BLUE = (8, 97, 87)
OBSTACLE_INTERVAL = 900
BULLET_VEL = 7
ENEMY_HIT = pygame.USEREVENT + 2
PURPLE = (193, 0, 250)
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

# Variables
game_started = False
death = True
start_time = 0
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, OBSTACLE_INTERVAL)
enemy_rect_list = []
score = 0

#backgrounds
background1 = pygame.image.load(r'Graphics/Background/Hills_Layer_01.png').convert_alpha()
background1 = pygame.transform.scale(background1, (800, 575))
background2 = pygame.image.load(r'Graphics/Background/Hills_Layer_03.png').convert_alpha()
background2 = pygame.transform.scale(background2, (800,177))
background3 = pygame.image.load(r'Graphics/Background/Hills_Layer_05.png').convert_alpha()
background3 = pygame.transform.scale(background3, (800,36))
background4 = pygame.image.load(r'Graphics/Background/Hills_Layer_06.png').convert_alpha()
background5 = pygame.image.load(r'Graphics/Background/Hills_Layer_04.png').convert_alpha()
#start/end screen
screen_start = pygame.image.load(r'Graphics/Start_End/start_screen.png').convert_alpha()
screen_end = pygame.image.load(r'Graphics/Start_End/end_screen.png').convert_alpha()
#person
Person_Static = pygame.image.load(r'Graphics/Player/IdleStatic.png').convert_alpha()
Person_Static = pygame.transform.rotozoom(Person_Static,0,1.4)
Person_Static_rect = Person_Static.get_rect(midbottom = (WIDTH/2, 600))
direction = True
#enemy
enemy_static_1 = pygame.image.load(r'Graphics/Enemy/enemy_move_1.png').convert_alpha()
enemy_rect = enemy_static_1.get_rect(midbottom = (100, 0))

#font
font = pygame.font.Font(r'Graphics/Fonts/Khronopix.ttf', 50)

# Definitions
def draw_window(bullets):
  screen.blit(background1, (0,0))
  screen.blit(background5, (WIDTH/6,310))
  screen.blit(background2, (0, HEIGHT-176.56))
  screen.blit(background4, (0,HEIGHT-35.94-10))
  screen.blit(background3, (0,HEIGHT-31.25))
  screen.blit(time_surf, time_rect)
  screen.blit(score_surf, score_rect)

  for bullet in bullets:
        pygame.draw.rect(screen, PURPLE, bullet)

def show_fps():
  fps = int(clock.get_fps())
  fps_surf = font.render(f"{fps}", False, (LIGHT_BLUE))
  fps_rect = fps_surf.get_rect(center = (750,50))
  screen.blit(fps_surf, fps_rect)

def draw_person():
  if direction == True:
    screen.blit(Person_Static, Person_Static_rect)
  if direction == False:
    screen.blit(pygame.transform.flip(Person_Static, True, False), Person_Static_rect)

def draw_enemy(enemy_list):
  if enemy_list:
    for enemy_rect in enemy_list:
      enemy_rect.y += VEL_ENEMY
      screen.blit(enemy_static_1, enemy_rect)
      if enemy_rect.y > 800:
        enemy_rect_list.remove(enemy_rect)

def collision_check(player, enemys):
  global death
  if enemys:
    for enemy_rect in enemys:
      if player.colliderect(enemy_rect):
        death = True

def player_input():
  global direction # flip player
  keys = pygame.key.get_pressed()
  if keys[pygame.K_d] and Person_Static_rect.x < WIDTH-83:
    Person_Static_rect.x += VEL_PLAYER
    direction = True
  if keys[pygame.K_a] and Person_Static_rect.x > 0:
    Person_Static_rect.x -= VEL_PLAYER
    direction = False

def display_time():
  global time_rect, time_surf
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  time_surf = font.render(f"Time: {current_time}", False, (LIGHT_BLUE))
  time_rect = time_surf.get_rect(center = (100, 50))

def display_score():
  global score_rect, score_surf, score
  score_surf = font.render(f"Score: {score}", False, (LIGHT_BLUE))
  score_rect = score_surf.get_rect(center = (WIDTH/2,50))

def start_screen():
  start_text = font.render("Press RETURN to start!", False, (LIGHT_BLUE))
  start_text = pygame.transform.rotozoom(start_text,0,0.5)
  start_rect = start_text.get_rect(center = (WIDTH/2, 400))

  screen.blit(screen_start, (0,0))
  screen.blit(start_text, start_rect)

def death_screen():
  death_text = font.render("Press ESC to try again!", False, (LIGHT_BLUE))
  death_text = pygame.transform.rotozoom(death_text,0,0.5)
  death_rect = death_text.get_rect(center = (WIDTH/2, 400))

  screen.blit(screen_end, (0,0))
  screen.blit(death_text, death_rect)

def bullets_handle(bullets, enemys):
  for bullet in bullets:
    bullet.y -= BULLET_VEL
    if enemys:
       for enemy_rect in enemys:
          if bullet.colliderect(enemy_rect):
            pygame.event.post(pygame.event.Event(ENEMY_HIT))
            bullets.remove(bullet)
            enemys.remove(enemy_rect)

    elif bullet.y < 0:
      bullets.remove(bullet)

def main():
  global game_started, death, start_time, enemy_rect_list, Person_Static_rect, enemy_static_1, score

  bullets = []

  while True:
    for event in pygame.event.get():
      #quit event
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      #keys events
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
          game_started = True
          death = False
        if death == True:
          if event.key == pygame.K_ESCAPE:
            death = False
            enemy_rect.y = 0
        if event.key == pygame.K_SPACE:
          bullet = pygame.Rect(Person_Static_rect.x + Person_Static_rect.width, Person_Static_rect.y + Person_Static_rect.height/2 -2,5,10)
          bullets.append(bullet)
      #enemy hit
      if event.type == ENEMY_HIT:
        score += 1
      #timer event
      if event.type == enemy_timer and game_started and not death:
        enemy_rect_list.append(enemy_static_1.get_rect(midbottom = (random.randint(50,750), -50)))
    
    # Game logic
    if game_started == True:
      if death == False:
        display_time()
        display_score()
        draw_window(bullets)
        draw_person()
        bullets_handle(bullets, enemy_rect_list)
        draw_enemy(enemy_rect_list)
        player_input()
        collision_check(Person_Static_rect, enemy_rect_list)
        show_fps()
      else:
        death_screen()
        start_time = int(pygame.time.get_ticks() / 1000) # after respawn timer = 0
        enemy_rect_list.clear() # after death remove all enemys
        bullets.clear()
        Person_Static_rect = Person_Static.get_rect(midbottom = (WIDTH/2, 600))
        score = 0
    else:
      start_screen()
      start_time = int(pygame.time.get_ticks() / 1000) # after start screen timer = 0
      score = 0

    pygame.display.flip() 
    clock.tick(FPS)

if __name__ == '__main__':
  main()