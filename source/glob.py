import pygame
from pygame import mixer
from source import gui
from source import glob
from source import cls

ABOUT = [
        'This Star Wars Galaga-like game',
        'is made by MATF students:',
        'Boris Cvitak',
        'Ognjen Stamenkovic',
        'Predrag Mitic'
        ]

#DODATO promenljive koje pamte kontrole
CONTROL_LEFT_ORD = ord('a')
CONTROL_LEFT = 'a'
CONTROL_RIGHT_ORD = ord('d')
CONTROL_RIGHT = 'd'
CONTROL_FIRE_ORD = ord('w')
CONTROL_FIRE = 'w'


TWO_CONTROL_LEFT_ORD1 = ord('a')
TWO_CONTROL_LEFT1 = 'a'
TWO_CONTROL_RIGHT_ORD1 = ord('d')
TWO_CONTROL_RIGHT1 = 'd'
TWO_CONTROL_FIRE_ORD1 = ord('w')
TWO_CONTROL_FIRE1 = 'w'

TWO_CONTROL_LEFT_ORD2 = pygame.K_RIGHT
TWO_CONTROL_LEFT2 = 'KEY_RIGHT'
TWO_CONTROL_RIGHT_ORD2 = pygame.K_LEFT
TWO_CONTROL_RIGHT2 = 'KEY_LEFT'
TWO_CONTROL_FIRE_ORD2 = pygame.K_UP
TWO_CONTROL_FIRE2 = 'KEY_UP'

CONTROLS_TEXT = [
                'First player:                                                                                            Second player:',
                f'To left : {CONTROL_LEFT}                                                                                                                  To left : <',
                f'To right : {CONTROL_RIGHT}                                                                                                               To left : >',
                f'To shoot : {CONTROL_FIRE}                                                                                                        To shoot : ^'
                ]

VOLUME_VALUES = {
                '0_PERCENT': 0,
                '10_PERCENT': 0.1,
                '30_PERCENT': 0.3,
                '50_PERCENT': 0.5,
                '70_PERCENT': 0.7,
                '100_PERCENT': 1,
                }
fighters = [
                pygame.image.load('images/enemy1.png'),
                pygame.image.load('images/enemy2.png'),
                pygame.image.load('images/enemy3.png'),
                pygame.image.load('images/enemy4.png'),
               ]

num_enemies = [
                'Nema enemy-ja za 0 level',
                [11, 13, 15],
                [32, 40, 48],
                [None, None, None] # Broj enemy-ja na levelu 3 ne zavisi od ovih brojeva
                ]

enemies = [0, 0, 0, 0]

bosses = [
            "",
            pygame.image.load('images/boss1.png'),
            pygame.image.load('images/boss2.png'),
            pygame.image.load('images/boss3.png')
            ]

boss_name = [
            "",
            "Grand MoffTarkin",
            "Darth Vader",
            "Darth Sidious"
            ]

destroyers = [
                pygame.image.load('images/destroyer1.png'),
                pygame.image.load('images/destroyer2.png'),
                pygame.image.load('images/destroyer3.png'),
                pygame.image.load('images/destroyer3.png')
             ]

stories = [
            pygame.image.load('images/story0.png'),
            pygame.image.load('images/story1.png'),
            pygame.image.load('images/story2.png'),
            pygame.image.load('images/story3.png'),
            pygame.image.load('images/story4.png')
          ]

#storiji koji se prikazuju posle poraza u levelu odgovarajuceg bossa
defeat_stories = [
                    pygame.image.load('images/defeat_boss1.png'),
                    pygame.image.load('images/defeat_boss2.png'),
                    pygame.image.load('images/defeat_boss3.png')
                 ]

#storiji koji se prikazuju pre odgovarajuceg boss-a
boss_stories = [
                pygame.image.load('images/story_boss1.png'),
                pygame.image.load('images/story_boss2.png'),
                pygame.image.load('images/story_boss3.png')
                ]

LEVEL = 1
FIGHT = 0

GAME_VOLUME = 0.5
MENU_VOLUME = 0.5

WINDOW_SIZE = (1300, 700)
MENU_SIZE = (500, 450)
START_WARS_LOGO_POS = (1200, 600)
PAUSE_ONE_PLAYER_POS = (1265, 665)
PAUSE_TWO_PLAYERS_POS = (634, 5)
BLACK_COLOR = (0, 0, 0)
WALL_START_POS = (650, 700)
WALL_END_POS = (650, 40)
WALL_WIDTH = 15
NUM_PLAYERS = 'ONE_PLAYER'

ENEMIES_IS_READY = False

bullets_enm_list = pygame.sprite.Group()
rockets_list = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
left_rockets_list = pygame.sprite.Group()
right_rockets_list = pygame.sprite.Group()

game_background = pygame.image.load('images/game_background.jpg')
pause_img_1 = pygame.image.load('images/pause1.png')
pause_img_2 = pygame.image.load('images/pause2.png')

x_wing = pygame.image.load('images/ply6.png')
rocket = pygame.image.load('images/rocket_player.png')

life_image = pygame.transform.scale(x_wing, (25,25))
blue_sw = pygame.image.load('images/blue.jpg')

#prikazivanje pobednickog storija
def victory():

	pressed_enter = False

	gui.screen.blit(glob.stories[glob.LEVEL], (0, -40))
	pygame.display.update()

	
	while not pressed_enter:
		events = pygame.event.get()
		for e in events:
	            if e.type == pygame.KEYDOWN:
	                if e.key == pygame.K_RETURN:
	                    pressed_enter = True
	                    break

	return_to_main_menu()


#iscrtavanje poraza od odgovarajuceg bossa
def defeat():

	pressed_enter = False

	gui.screen.blit(glob.defeat_stories[glob.LEVEL-1], (0, -40))
	pygame.display.update()

	
	while not pressed_enter:
		events = pygame.event.get()
		for e in events:
	            if e.type == pygame.KEYDOWN:
	                if e.key == pygame.K_RETURN:
	                    pressed_enter = True
	                    break

	return_to_main_menu()



def return_to_main_menu():
    mixer.music.stop()
    gui.main_menu.enable()
    mixer.music.load('sounds/menu_music.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(glob.MENU_VOLUME)

def make_star():

    '''
    S
    '''
    for i in [50, 200, 350]:
        for n in range(5):
            enm = cls.Enemy(0)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = 100 + 50*n
            enm.rect.y = -350 + i
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    for i in [100, 150]:
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 100
        enm.rect.y = -350 + i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in [250, 300]:
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 300
        enm.rect.y = -350 + i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    '''
    T
    '''
    for i in range(5):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 383 + i*50
        enm.rect.y = -350 + 50
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(12):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 483
        enm.rect.y = -350 + 75 + i*25
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    '''
    A
    '''
    for i in [666, 866]:
        for n in range(7):
            enm = cls.Enemy(2)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = i
            enm.rect.y = -350 + 50 + n*50
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    for i in [50, 200]:
        for n in range(1, 4):
            enm = cls.Enemy(2)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = 666 + n*50
            enm.rect.y = -350 + i
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)

    '''
    R
    '''
    for i in range(7):
        enm = cls.Enemy(3)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 949
        enm.rect.y = -350 + 50 + 50*i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in [50, 200]:
        for n in range(1, 5):
            enm = cls.Enemy(3)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = 949 + 50*n
            enm.rect.y = -350 + i
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    for i in range(2):
        enm = cls.Enemy(3)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 1149
        enm.rect.y = -350 + 100 + 50*i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(3):
        enm = cls.Enemy(3)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 999 + 50 * i
        enm.rect.y = -350 + 250 + 50 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    enm = cls.Enemy(3)
    glob.enemies[enm.enmType] += 1
    enm.rect.x = 1149
    enm.rect.y = -350 + 350
    glob.enemies_list.add(enm)
    glob.all_sprites_list.add(enm)

def make_wars():
    '''
    W
    '''
    for i in [100, 300]:
        for n in range(7):
            enm = cls.Enemy(3)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = i
            enm.rect.y = -350 + 50 + n*50
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    enm = cls.Enemy(3)
    glob.enemies[enm.enmType] += 1
    enm.rect.x = 200
    enm.rect.y = -350 + 225
    glob.enemies_list.add(enm)
    glob.all_sprites_list.add(enm)

    for i in [150, 250]:
        enm = cls.Enemy(3)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = i
        enm.rect.y = -350 + 325
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    for i in [170, 230]:
        enm = cls.Enemy(3)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = i
        enm.rect.y = -350 + 275
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    '''
    A
    '''
    for i in [383, 583]:
        for n in range(7):
            enm = cls.Enemy(2)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = i
            enm.rect.y = -350 + 50 + n*50
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    for i in [50, 200]:
        for n in range(1, 4):
            enm = cls.Enemy(2)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = 383 + n*50
            enm.rect.y = -350 + i
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)

    '''
    R
    '''
    for i in range(7):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 666
        enm.rect.y = -350 + 50 + 50 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in [50, 200]:
        for n in range(1, 5):
            enm = cls.Enemy(1)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = 666 + 50 * n
            enm.rect.y = -350 + i
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    for i in range(2):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 866
        enm.rect.y = -350 + 100 + 50 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(3):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 716 + 50 * i
        enm.rect.y = -350 + 250 + 50 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    enm = cls.Enemy(1)
    glob.enemies[enm.enmType] += 1
    enm.rect.x = 866
    enm.rect.y = -350 + 350
    glob.enemies_list.add(enm)
    glob.all_sprites_list.add(enm)

    '''
    S
    '''
    for i in [50, 200, 350]:
        for n in range(5):
            enm = cls.Enemy(0)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = 949 + 50*n
            enm.rect.y = -350 + i
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    for i in [100, 150]:
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 949
        enm.rect.y = -350 + i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in [250, 300]:
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 1149
        enm.rect.y = -350 + i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)


def make_end():

    '''
    E
    '''
    for i in range(7):
        enm = cls.Enemy(2)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 100
        enm.rect.y = -350 + 50 + 50 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in [50, 200, 350]:
        for n in range(4):
            enm = cls.Enemy(2)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = 150 + 50*n
            enm.rect.y = -350 + i
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)

    '''
    N
    '''
    for i in [383, 583]:
        for n in range(7):
            enm = cls.Enemy(3)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = i
            enm.rect.y = -350 + 50 + n*50
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)
    for i in range(5):
        enm = cls.Enemy(3)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 433 + 25*i
        enm.rect.y = -350 + 150 + i * 25
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    '''
    D
    '''
    for i in range(7):
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 666
        enm.rect.y = -350 + 50 + 50 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(4):
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 866
        enm.rect.y = -350 + 125 + 50 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(4):
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 716 + 50*i
        enm.rect.y = -350 + 60 + 10 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(4):
        enm = cls.Enemy(0)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 716 + 50 * i
        enm.rect.y = -350 + 340 - 10 * i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)

    '''
    !
    '''
    for i in range(5):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 949 + 50 * i
        enm.rect.y = -350 + 50
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(5):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 949 + 25 * i
        enm.rect.y = -350 + 50 + 50*i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in range(5):
        enm = cls.Enemy(1)
        glob.enemies[enm.enmType] += 1
        enm.rect.x = 949+200 - 25 * i
        enm.rect.y = -350 + 50 + 50*i
        glob.enemies_list.add(enm)
        glob.all_sprites_list.add(enm)
    for i in [949+75, 949+75+50]:
        for n in [325, 350]:
            enm = cls.Enemy(1)
            glob.enemies[enm.enmType] += 1
            enm.rect.x = i
            enm.rect.y = -350 + n
            glob.enemies_list.add(enm)
            glob.all_sprites_list.add(enm)


