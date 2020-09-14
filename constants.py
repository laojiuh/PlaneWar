import os, os.path
import pygame

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 静态文件目录
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
# 游戏开始背景
BG_IMG = os.path.join(ASSETS_DIR, 'images/background.png')
# 游戏结束背景
BG_IMG_OVER = os.path.join(ASSETS_DIR, 'images/game_over.png')
# 开始标题
IMG_GAME_TITLE = os.path.join(ASSETS_DIR, 'images/game_title.png')
# 开始按钮
IMG_GAME_START_BTN = os.path.join(ASSETS_DIR, 'images/game_start.png')
# background music path
BG_MUSIC = os.path.join(ASSETS_DIR, 'sounds/game_bg_music.mp3')
# 文字分数颜色
TEXT_SCORE_COLOR = pygame.Color(255, 255, 0)
# 飞机击中得分
SCORE_SHOOT_SMALL = 10

# 我方飞机的静态资源
OUR_PLANE_IMG_LIST = [os.path.join(ASSETS_DIR, 'images/hero1.png'), os.path.join(ASSETS_DIR, 'images/hero2.png')]
OUR_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/hero_broken_n1.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n2.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n3.png'),
    os.path.join(ASSETS_DIR, 'images/hero_broken_n4.png')
]

# 子弹的图片
BULLET_IMG = os.path.join(ASSETS_DIR, 'images/bullet1.png')
# 子弹的声音
BULLET_SHOOT_SOUND = os.path.join(ASSETS_DIR, 'sounds/bullet.wav')

# 地方飞机的静态资源
SMALL_ENEMY_PLANE_IMG_LIST = [os.path.join(ASSETS_DIR, 'images/enemy1.png')]
SMALL_ENEMY_PLANE_DESTROY_IMG_LIST = [
    os.path.join(ASSETS_DIR, 'images/enemy1_down1.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down2.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down3.png'),
    os.path.join(ASSETS_DIR, 'images/enemy1_down4.png')
]
SMALL_ENEMY_PLANE_DOWN_SOUND = os.path.join(ASSETS_DIR, 'sounds/enemy1_down.wav')

# 游戏结果存储文件
PLAY_RESULT_STORE_FILE = os.path.join(BASE_DIR, 'store/rest.txt')

