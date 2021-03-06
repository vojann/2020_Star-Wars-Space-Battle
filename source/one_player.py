import time as TIME
import pygameMenu
from source import cls
from source import gui
from source import glob
from pygame import mixer
import pygame
import math
import random

player = None
destroyer = None
game_timer = 0
burst_fire = 0
timer_destroyer = 0

timer_hidden = 0
hidden_enemy = None

def check_menu_events():
    
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                exit()

        # Ukoliko smo kliknuli na pauzu, otvaramo pause_meni i zaustavljamo muziku
        if e.type == pygame.MOUSEBUTTONDOWN and gui.pause_menu.is_disabled():
            if glob.pause_img_1.get_rect(topleft=glob.PAUSE_ONE_PLAYER_POS).collidepoint(pygame.mouse.get_pos()):
                gui.pause_menu.enable()

    # ako su ukljuceni meniji, prikupljamo dogadjaje u njima
    if gui.main_menu.is_enabled():
        gui.main_menu.mainloop(events)
    elif gui.pause_menu.is_enabled():
        gui.pause_menu.mainloop(events)


def check_player_events():
    global game_timer, burst_fire
    cont = cls.Controler()
    movement = 5
    left_margin = 0 + 10
    right_margin = glob.WINDOW_SIZE[0] - 70
    pressed = pygame.key.get_pressed()

    if pressed[cont.Left] and player.position_x > left_margin:
        player.position_x -= movement

    if pressed[cont.Right] and player.position_x < right_margin:
        player.position_x += movement

    # IZMENJENO burst fire je najmanje vreme izmedju dve rakete
    burst_fire += 1

    if pressed[cont.Fire] and (glob.ENEMIES_IS_READY or destroyer.is_ready):
        # Metak se ispaljuje u svakom 20-tom ciklusu 
        # Promenio na 2 da bi se brze prelazila igrica tokom testiranja
        if burst_fire > 2:
            # Zvuk pri ispaljivanju metaka
            rocket_sound = mixer.Sound('sounds/laser.wav')
            rocket_sound.play()

            rocket = cls.Rocket()
            rocket.rect.x = player.position_x + 26  # razlika u velicina slika
            rocket.rect.y = player.position_y

            glob.all_sprites_list.add(rocket)
            glob.rockets_list.add(rocket)
            burst_fire = 0

def check_rocket_to_enemise_collide():
    global destroyer, timer_hidden, hidden_enemy, enemies

    for r in glob.rockets_list:
        r.show_rocket()

        if glob.ENEMIES_IS_READY:
            # Obrada kolizije player vs enemies
            enemy_hit_list = pygame.sprite.spritecollide(r, glob.enemies_list, True)

            for enm in enemy_hit_list:
                glob.enemies[enm.enmType] -= 1
                glob.rockets_list.remove(r)
                glob.all_sprites_list.remove(r)
                glob.enemies_list.remove(enm)

        # ako je destroyer spreman onda mozemo da pucamo na njega i da mu skidamo health-e
        if destroyer.is_ready:
            # Obrada kolizije player vs destroyer
            if r.rect.x in range(destroyer.rect.x, destroyer.rect.x + 120):
                dist = 120 - r.rect.x + destroyer.rect.x
                dist = dist if dist < 64 else 120 - dist
                if r.rect.y < destroyer.rect.y + 3 * dist + 40:
                    glob.rockets_list.remove(r)
                    glob.all_sprites_list.remove(r)
                    #Zvuk eksplozije kada metak pogodi protivnika
                    explosion_sound = mixer.Sound('sounds/explosion.wav')
                    explosion_sound.play()
                    destroyer.health -= 7

        if r.rect.y < -20:
            glob.rockets_list.remove(r)
            glob.all_sprites_list.remove(r)

def draw_player():

    if player.health > 0:
        player.show()
        player.show_health()
    else:
        if player.lives_number >= 0:
            player.lives_number -= 1
            player.health = 100
            player.show_health()
            pygame.display.update()
            TIME.sleep(0.5)



def draw_destroyer():
    global destroyer, timer_destroyer
    timer_destroyer += 3
    destroyer.rect.x = glob.WINDOW_SIZE[0] / 2 - 64
    destroyer.rect.y = (int(timer_destroyer / 5) - 240 if timer_destroyer < 1400 else 40)
    
    color = (255,120,0)
    font = pygameMenu.font.get_font(pygameMenu.font.FONT_PT_SERIF, 30)
    name = font.render(glob.boss_name[glob.LEVEL], 1, color)
    health = font.render('Health:', 1, color)

    if destroyer.health > 0:
        destroyer.show()
        if timer_destroyer > 1000:
            pygame.draw.rect(gui.screen, (40, 40, 40), (0,10,glob.WINDOW_SIZE[0], 30))
            gui.screen.blit(glob.bosses[glob.LEVEL], (10,0))
            gui.screen.blit(name, (glob.WINDOW_SIZE[0]-280,5))
            gui.screen.blit(health, (75,5))
            pygame.draw.rect(gui.screen, color, (300, 15, destroyer.health * 6, 20))
        if timer_destroyer > 1200:

            #iscrtavanje pred-bossovskog storija i cekanje na ENTER
            pressed_enter = False
      
            while not pressed_enter and not destroyer.is_ready:
                gui.screen.blit(glob.boss_stories[glob.LEVEL-1], (0, -40))
                pygame.display.update()
                events = pygame.event.get()
                for e in events:
                        if e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_RETURN:
                                pressed_enter = True
                                break

            destroyer.is_ready = True
            destroyer_fire_to_player()



def go_to_next_level():

    glob.LEVEL += 1
    start_game_one_player()

def destroyer_battle():

    if destroyer.health <= 0:
        destroyer.is_ready = False
        go_to_next_level()
    else:
        draw_destroyer()

def set_hidden_enemys():
    global timer_hidden, hidden_enemy

    if glob.LEVEL == 1:
        if hidden_enemy is True:
            if timer_hidden == 0:
                for enm in glob.enemies_list:
                    enm.hidden = True
                    timer_hidden += 1
            elif timer_hidden < 150:  # odokativna duzina koliko je nevidljiv
                timer_hidden += 1
            else:
                timer_hidden = -150
                for enm in glob.enemies_list:
                    enm.hidden = False
    elif glob.LEVEL == 3:
        if hidden_enemy is True:
            if timer_hidden == 0:
                for enm in glob.enemies_list:
                    enm.hidden = True
                    timer_hidden += 1
            elif timer_hidden < 150:  # odokativna duzina koliko je nevidljiv
                timer_hidden += 1
            else:
                timer_hidden = -220
                for enm in glob.enemies_list:
                    enm.hidden = False


def enemies_fire_to_player():
    
    #Ako nema neprijatelja ne pucamo
    if glob.ENEMIES_IS_READY is False or player.health <= 0:
        glob.bullets_enm_list.draw(gui.screen)
        return

    rand_enm = random.choice(glob.enemies_list.sprites())
    num_enemies = len(glob.enemies_list.sprites())

    #Da ne gadjaju svi metkovi direktno u playera
    frequency = int(300 / num_enemies)

    #Ogranicnje frekvencije paljbe
    if frequency < 48:
        frequency = 48

    frequency -= glob.LEVEL * 9
    
    fire_mode = game_timer % (3*frequency)
    

    if fire_mode == 0:  # Napad neprijatelja: 400 ucestalost paljbe
        bul = cls.BulletEnemy()
        bul.rect.x = rand_enm.rect.x + 20
        bul.rect.y = rand_enm.rect.y + 20
        intensity = math.sqrt((bul.rect.x - player.position_x) ** 2 + (bul.rect.y - player.position_y) ** 2)
        bul.set_direction(player.position_x, player.position_y, intensity)
        glob.bullets_enm_list.add(bul)
        glob.all_sprites_list.add(bul)

    # Svaki drugi ispaljuje metak u pravcu (0,1)
    if fire_mode * 2 == frequency:
        bul = cls.BulletEnemy()
        bul.rect.x = rand_enm.rect.x + 32
        bul.rect.y = rand_enm.rect.y + 32
        glob.bullets_enm_list.add(bul)
        glob.all_sprites_list.add(bul)

    glob.bullets_enm_list.draw(gui.screen)

    set_hidden_enemys()


def destroyer_fire_to_player():

    global timer_destroyer
    if player.health <= 0:
        glob.bullets_enm_list.draw(gui.screen)
        return

        # Ucestalost pucnja zavisi od levela
    if timer_destroyer % (180 - glob.LEVEL * 30) == 0:
        for i in range(3):
            bul = cls.BulletDestroyer()
            bul.rect.x = destroyer.rect.x + 32*(i+1)
            bul.rect.y = destroyer.rect.y + 115
            intensity = math.sqrt((bul.rect.x - player.position_x) ** 2 + (bul.rect.y - player.position_y) ** 2)
            bul.direction[0] = (player.position_x - bul.rect.x) / intensity + i/10
            bul.direction[1] = (player.position_y - bul.rect.y) / intensity + i/10
            glob.bullets_enm_list.add(bul)
            glob.all_sprites_list.add(bul)

    glob.bullets_enm_list.draw(gui.screen)


def check_bullets_player_collide():
    for bullet in glob.bullets_enm_list:
        if bullet.rect.x in range(player.position_x, player.position_x + 64):
            if bullet.rect.y in range(player.position_y + 20, player.position_y + 64):
                glob.bullets_enm_list.remove(bullet)
                if destroyer.is_ready:
                    player.health -= 25
                else:
                    player.health -= 20

        if bullet.rect.y > glob.WINDOW_SIZE[1] - 55:
            glob.bullets_enm_list.remove(bullet)

def make_new_enemies():

    if glob.LEVEL == 1:
        make_enemies1(glob.num_enemies[glob.LEVEL][glob.FIGHT])
    elif glob.LEVEL == 2:
        make_enemies2(glob.num_enemies[glob.LEVEL][glob.FIGHT])
    elif glob.LEVEL == 3:
        make_enemies3(glob.num_enemies[glob.LEVEL][glob.FIGHT])

    glob.FIGHT += 1


def make_enemies1(number):

    num = glob.num_enemies[1][glob.FIGHT]

    for i in range(1, 5):
        for n in range(1, num):
            enm = cls.Enemy(i-1)
            glob.enemies[enm.enmType] += 1
            enm.rect.y = -(30 * i + 40 * (i-1))-100
            distance = int((glob.WINDOW_SIZE[0] - num*40) / num)
            enm.rect.x = float(n * distance + n*40)
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)

def make_enemies2(number):
   
    num = int(glob.num_enemies[2][glob.FIGHT] / 4)
    for i in range(1, 5):
        for n in range(num):
            enm = cls.Enemy(i-1)
            glob.enemies[enm.enmType] += 1
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)

def make_enemies3(number):

    if glob.FIGHT == 0:
        glob.make_star()
    elif glob.FIGHT == 1:
        glob.make_wars()
    elif glob.FIGHT == 2:
        glob.make_end()

def fight_1():
    if game_timer < 500:
        
        for enm in glob.enemies_list:
            if enm.enmType >= 2 :
                enm.rect.y += 2
    else:
        glob.ENEMIES_IS_READY = True
        
    if game_timer > 2500 and game_timer < 3000:
        
        for enm in glob.enemies_list:
            if enm.enmType < 2 :
                enm.rect.y += 2

def fight_2():

    if game_timer < 500:
        for enm in glob.enemies_list:
            enm.rect.y += 2
    else:
        glob.ENEMIES_IS_READY = True
        for enm in glob.enemies_list:
            if enm.enmType % 2 == 0:
                enm.rect.x = (enm.rect.x-4) % glob.WINDOW_SIZE[0]
            else:
                enm.rect.x = (enm.rect.x+4) % glob.WINDOW_SIZE[0]

def fight_3():
    global hidden_enemy
    if game_timer < 500:
        for enm in glob.enemies_list:
            enm.rect.y += 2
    else:
        glob.ENEMIES_IS_READY = True
        hidden_enemy = True
        for enm in glob.enemies_list:
            if enm.enmType % 2 == 0:
                enm.rect.x = (enm.rect.x - 4) % glob.WINDOW_SIZE[0]
            else:
                enm.rect.x = (enm.rect.x + 4) % glob.WINDOW_SIZE[0]


def fight_4():
    
    if game_timer < 500:
        glob.ENEMIES_IS_READY = False
    else:
        glob.ENEMIES_IS_READY = True

    global enemies
    enms = [0, 0, 0, 0]
    r = 100
    for enm in glob.enemies_list:
        if glob.enemies[enm.enmType] % 2 == 0:
            step = glob.enemies[enm.enmType]
        else:
            step = glob.enemies[enm.enmType] + 1
        angle_param = enms[enm.enmType] * (360 / step) + game_timer / 100.0
        enms[enm.enmType] += 1
        enm.rect.y = r * math.sin(angle_param) - 100 * math.cos(game_timer/100)
        enm.rect.x = 200 + 300 * enm.enmType + r * math.cos(angle_param)


def fight_5():
    
    if game_timer < 500:
        glob.ENEMIES_IS_READY = False
    else:
        glob.ENEMIES_IS_READY = True

    n = len(glob.enemies_list.sprites())
    i = 0
    for enm in glob.enemies_list:
        i += 1
        angle_param = i * (360 / n) + game_timer / 100.0
        enm.rect.y = 50*(enm.enmType+1) * math.sin(angle_param) + 180
        enm.rect.x = 50*(enm.enmType+1) * math.cos(angle_param) + math.cos(game_timer / 100) * 400 + 600.0


def fight_6():

    if game_timer < 500:
        glob.ENEMIES_IS_READY = False
    else:
        glob.ENEMIES_IS_READY = True

    global enemies
    enms = [0, 0, 0, 0]
    r = 50
    param = game_timer / 100
    for enm in glob.enemies_list:
        if glob.enemies[enm.enmType] % 2 == 0:
            step = glob.enemies[enm.enmType]
        else:
            step = glob.enemies[enm.enmType] + 1
        angle_param = enms[enm.enmType] * (360 / step) + param
        enms[enm.enmType] += 1
        if enm.enmType % 2 == 0:
            enm.rect.y = 140 - 80 * math.sin(param) + r * math.sin(angle_param) - 60 * math.cos(param)
            enm.rect.x = (200 + 300 * enm.enmType + r * math.cos(angle_param) + game_timer * 2) % glob.WINDOW_SIZE[0]
        else:
            enm.rect.y = 140 + 80*math.sin(param) + r * math.sin(angle_param) - 60 * math.cos(param)
            enm.rect.x = (200 + 300 * enm.enmType + r * math.cos(angle_param) - game_timer*2) % glob.WINDOW_SIZE[0]


direction = ['left', 'right', 'circle']
iter = 0
dir = ''
circle_step = 1
def fight_7():

    global game_timer, direction, dir, iter, circle_step, hidden_enemy
    if game_timer % 300 == 0:
        circle_step *= (-1)
    if game_timer % 1200 == 0:
        dir = direction[iter]
        iter = (iter + 1) % len(direction)

    for enm in glob.enemies_list:
        if game_timer < 500:
            enm.rect.y += 2
        else:
            glob.ENEMIES_IS_READY = True

        if dir == 'left':
            enm.rect.x = (enm.rect.x - 10) % glob.WINDOW_SIZE[0]
        elif dir == 'right':
            enm.rect.x = (enm.rect.x + 10) % glob.WINDOW_SIZE[0]
        elif dir == 'circle':
            enm.rect.y -= (7 * circle_step)

def fight_8():

    global game_timer, direction, dir, iter, circle_step, hidden_enemy
    if game_timer % 300 == 0:
        circle_step *= (-1)
    if game_timer % 1200 == 0:
        dir = direction[iter]
        iter = (iter + 1) % len(direction)

    for enm in glob.enemies_list:
        if game_timer < 500:
            enm.rect.y += 2
        else:
            glob.ENEMIES_IS_READY = True

        if dir == 'left':
            enm.rect.x = (enm.rect.x - 10) % glob.WINDOW_SIZE[0]
        elif dir == 'right':
            enm.rect.x = (enm.rect.x + 10) % glob.WINDOW_SIZE[0]
        elif dir == 'circle':
            enm.rect.y -= (7 * circle_step)


def fight_9():

    global game_timer, direction, dir, iter, circle_step, hidden_enemy, timer_hidden
    if game_timer % 300 == 0:
        circle_step *= (-1)
    if game_timer % 1200 == 0:
        dir = direction[iter]
        iter = (iter + 1) % len(direction)

    if (game_timer % 200) < 180 :
        hidden_enemy = True
    else:
        hidden_enemy = False

    for enm in glob.enemies_list:
        if game_timer < 500:
            enm.rect.y += 2
        else:
            glob.ENEMIES_IS_READY = True

        if dir == 'left':
            #timer_hidden = -10
            enm.rect.x = (enm.rect.x - 10) % glob.WINDOW_SIZE[0]
        elif dir == 'right':
            enm.rect.x = (enm.rect.x + 10) % glob.WINDOW_SIZE[0]
        elif dir == 'circle':
            enm.rect.y -= (7 * circle_step)


def move_enemies1():
    if glob.FIGHT == 1:
        fight_1()

    if glob.FIGHT == 2:
        fight_2()

    if glob.FIGHT == 3:
        fight_3()

def move_enemies2():
    if glob.FIGHT == 1:
        fight_4()

    if glob.FIGHT == 2:
        fight_5()

    if glob.FIGHT == 3:
        fight_6()

def move_enemies3():
    if glob.FIGHT == 1:
        fight_7()

    if glob.FIGHT == 2:
        fight_8()

    if glob.FIGHT == 3:
        fight_9()


def move_enemies():

    #Samo ako postoje neprijatelji
    if len(glob.enemies_list) > 0:
        if glob.LEVEL == 1:
            move_enemies1()
        elif glob.LEVEL == 2:
            move_enemies2()
        elif glob.LEVEL == 3:
            move_enemies3()

def set_background():
    gui.screen.blit(glob.game_background, (0, 0))

    pygame.draw.rect(gui.screen, (40, 40, 40), (0, glob.WINDOW_SIZE[1]-40, glob.WINDOW_SIZE[0],30))
    gui.screen.blit(pygame.image.load('images/yellow1.png'), (10, 650))
    gui.screen.blit(glob.pause_img_1, glob.PAUSE_ONE_PLAYER_POS)
    font = pygameMenu.font.get_font(pygameMenu.font.FONT_PT_SERIF, 30)
    lives = font.render('Lives:', 1, (180, 150, 0))
    gui.screen.blit(lives, (75, 655))


def set_background_num_enemies():

    font = pygameMenu.font.get_font(pygameMenu.font.FONT_PT_SERIF, 30)
    for i in range(1, 5):
        f = font.render(f':{glob.enemies[i-1]}', 1, (180, 150, 0))
        gui.screen.blit(f, (970+80*(i-1), 655))
        gui.screen.blit(pygame.transform.scale(glob.fighters[i-1], (25,25)), (935+80*(i-1), 660))
        
def add_life():
    global player, game_timer

    font = pygame.font.Font('freesansbold.ttf',75)
    TextSurf = font.render("Extra LIFE", True,(180,150,0))
    TextRect = TextSurf.get_rect()
    TextRect.center = ((glob.WINDOW_SIZE[0]/2),160)
    
    
    if game_timer in range(50, 360):
        gui.screen.blit(TextSurf, TextRect)
        gui.screen.blit(pygame.transform.scale(glob.x_wing,(200-int(0.5*game_timer),200-int(0.5*game_timer))),
        (360 - 1*game_timer + 150, glob.WINDOW_SIZE[1] - 580 + 1.5*game_timer ))
        #pygame.display.update()

    if game_timer == 360:
        player.lives_number += 1
        
        
def init_game():
    
    global player, destroyer, game_timer, timer_destroyer, burst_fire

    player = cls.Player()
    destroyer = cls.Destroyer()

    game_timer = 0
    timer_destroyer = 0
    burst_fire = 0

    glob.FIGHT = 0
    glob.all_sprites_list.empty()
    glob.enemies_list.empty()
    glob.rockets_list.empty()
    glob.bullets_enm_list.empty()
    

def start_game_one_player():

    global player, destroyer, game_timer, timer_destroyer, burst_fire, hidden_enemy

    init_game()
    next_level = True  # da znamo da li igramo igricu ili isrctavamo prelazak nivoa
  
    while True:
        # Funkcija za proveru dogadjaja u meniju
        check_menu_events()
        # U narednih nekoliko linija se prebacuje mod igre u menu mode
        if gui.pause_menu.is_enabled(): 
            pygame.display.update()
            continue
        # Ako ukljucimo glavni meni, pocinjemo novu partiju
        if gui.main_menu.is_enabled(): 
            glob.LEVEL = 1
            pygame.display.update()
            return

        game_timer += 3
        set_background()
        
        if next_level:
            
            if glob.LEVEL == 4:
                glob.victory()
                return
            pressed_enter = False

            events = pygame.event.get()
            for e in events:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        pressed_enter = True
            gui.screen.blit(glob.stories[glob.LEVEL], (0, -40))
            pygame.display.update() 
            
            if not pressed_enter:
                game_timer = 0
                continue
            
            next_level = False


        if player.lives_number < 0:
            glob.defeat()
            return

        # Ako ima neprijatelja, neka ispaljuju metkove i neka se krecu:
        num_enemies = len(glob.enemies_list.sprites())
        if num_enemies > 0:
            enemies_fire_to_player()
            move_enemies()
        else:
            glob.ENEMIES_IS_READY = False
            hidden_enemy = False
            game_timer = 0
            if glob.FIGHT < 3:
                make_new_enemies()
            else:
                #Zavrsili smo fight 3, vreme je za destroyera
                destroyer_battle()

        # Iscrtaj neprijatelje
        for enm in glob.enemies_list:
            enm.show()

        #ispisuje broj preostalih enemyja u health-baru
        set_background_num_enemies()

        # Funkcija koja proverava da li je pogodjen player
        check_bullets_player_collide()

        # Funkcija za proveru dogadjaja nad player-om
        check_player_events()

        # Funkcija za proveru pogotka u (sve) neprijatelje
        check_rocket_to_enemise_collide()

        # Funkcija za iscrtavanje player-a  ( X-Wing )
        draw_player()
 
            # Funkcija dodaje dodatni zivot na pocetku svakog fajta
        add_life()

        glob.all_sprites_list.update()
        pygame.display.update()

