import pygame
import sys

import constants
from game.plane import OurPlane, SmallEnemyPlane
from store.result import PlayRest


class PlaneWar(object):
    """飞机大战"""

    READY = 0  # 游戏准备中
    PLAYING = 1  # 游戏中
    OVER = 2  # 游戏结束
    status = READY

    our_plane = None

    frame = 0  # 播放帧数

    # 为了方便之后的碰撞检测
    # 一架飞机可以属于多个精灵组
    small_enemies = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # 游戏结果
    rest = PlayRest()

    def __init__(self):
        # 初始化游戏
        pygame.init()
        self.width, self.height = 480, 852

        # 加载游戏屏幕
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 设置标题
        pygame.display.set_caption('PlaneWar')
        # 背景图片
        self.bg = pygame.image.load(constants.BG_IMG)
        # 结束背景
        self.bg_over = pygame.image.load(constants.BG_IMG_OVER)
        # 开始标题的位置设置
        self.img_game_title = pygame.image.load(constants.IMG_GAME_TITLE)
        self.img_game_title_rect = self.img_game_title.get_rect()
        t_width, t_height = self.img_game_title.get_size()
        self.img_game_title_rect.topleft = (int((self.width - t_width) / 2),
                                            int(self.height / 2 - t_height))
        # 开始按钮的位置设置
        self.btn_start = pygame.image.load(constants.IMG_GAME_START_BTN)
        self.btn_start_rect = self.btn_start.get_rect()
        b_width, b_height = self.btn_start.get_size()
        self.btn_start_rect.topleft = (int((self.width - b_width) / 2),
                                       int(self.height / 2 + b_height))

        # 游戏文字对象
        self.score_font = pygame.font.SysFont('华文隶书', 32)

        # background music
        pygame.mixer.music.load(constants.BG_MUSIC)
        pygame.mixer.music.play(-1)  # 无限循环播放
        pygame.mixer.music.set_volume(0.2)  # 设置音量

        # 我方飞机对象
        self.our_plane = OurPlane(self.screen, speed=8)

        # 设置帧数
        self.clock = pygame.time.Clock()

        self.key_down = None

    def bind_event(self):
        """绑定事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 游戏正在等待中，点击鼠标进入游戏
                if self.status == self.READY:
                    self.status = self.PLAYING
                elif self.status == self.OVER:
                    self.status = self.READY
                    self.add_small_enemies(6)
            elif event.type == pygame.KEYDOWN:

                self.key_down = event.key
                # 先判断在游戏中，在判断上下左右控制方向
                if self.status == self.PLAYING:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.our_plane.move_up()
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.our_plane.move_down()
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.our_plane.move_left()
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.our_plane.move_right()
        # 让飞机一直发射炮
        if self.status == self.PLAYING and self.frame % 10 == 0:
            self.our_plane.shoot()

    def add_small_enemies(self, num):
        for i in range(num):
            plane = SmallEnemyPlane(self.screen, 4)
            plane.add(self.small_enemies, self.enemies)

    def run_game(self):
        """游戏的主循环"""
        while True:
            # 1. 设置帧数
            self.clock.tick(60)
            # 计数
            self.frame += 1
            if self.frame >= 60:
                self.frame = 0

            # 2. 绑定事件
            self.bind_event()

            # 3. 更新游戏状态  硬编码
            if self.status == self.READY:
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 绘制开始背景
                self.screen.blit(self.img_game_title, self.img_game_title_rect)
                # 开始按钮
                self.screen.blit(self.btn_start, self.btn_start_rect)
                # 重置按键
                self.key_down = None
                self.rest.score = 0
            elif self.status == self.PLAYING:
                # 游戏进行中
                # 绘制背景
                self.screen.blit(self.bg, self.bg.get_rect())
                # 绘制我方飞机
                self.our_plane.update(self)
                # 绘制子弹
                self.our_plane.bullets.update(self)
                # 绘制敌方飞机
                self.small_enemies.update()
                # 游戏分数
                score_text = self.score_font.render('得分：{}'.format(self.rest.score), False, constants.TEXT_SCORE_COLOR)
                # 绘制分数
                self.screen.blit(score_text, score_text.get_rect())

            elif self.status == self.OVER:
                # 游戏结束背景
                self.screen.blit(self.bg_over, self.bg_over.get_rect())
                # 分数统计
                # 1.本次总分
                score_text = self.score_font.render(
                    '{}'.format(self.rest.score),
                    False,
                    constants.TEXT_SCORE_COLOR)
                score_text_rect = score_text.get_rect()
                text_w, text_h = score_text.get_size()
                score_text_rect.topleft = (
                    int((self.width - text_w) / 2),
                    int(self.height / 2)
                )

                # 绘制分数
                self.screen.blit(score_text, score_text_rect)
                # 2.历史最高分
                score_his = self.score_font.render('{}'.format(self.rest.get_max_core()), False,
                                                   constants.TEXT_SCORE_COLOR)

                self.screen.blit(score_his, (150, 40))

            pygame.display.flip()
