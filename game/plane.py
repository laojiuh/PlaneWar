import random
import time

import pygame

import constants
from game.bullet import Bullet


class Plane(pygame.sprite.Sprite):
    """飞机的基础类型"""
    # 飞机的图片
    plane_images = []
    # 飞机碰撞的图片
    destroy_images = []
    # 飞机碰撞的声音
    down_sounds_src = None
    # 飞机的状态: True表示活着
    active = True
    # 子弹
    bullets = pygame.sprite.Group()

    def __init__(self, screen, speed=None):
        super().__init__()
        self.screen = screen
        # pygame中的存储的图片和音乐
        self.img_list = []
        self._destroy_images_list = []
        self.down_sounds = None
        # 把文件中的图片或者音乐载入到pygame中
        self.load_src()
        # 飞机的速度
        self.speed = speed or 10
        # 获取飞机的长宽
        self.plane_w, self.plane_h = self.img_list[0].get_size()

        # 飞机的位置
        self.rect = self.img_list[0].get_rect()

        # 屏幕的宽度和高度
        self.width, self.height = self.screen.get_size()

        # 改变飞机的初始化位置，放在屏幕的下方
        self.rect.left = int((self.width - self.plane_w) / 2)
        self.rect.top = int(self.height / 2)

    def load_src(self):
        """加载静态资源"""
        # 飞机的图像载入
        for img in self.plane_images:
            self.img_list.append(pygame.image.load(img))

        # 飞机坠毁的图像
        for img in self.destroy_images:
            self._destroy_images_list.append(pygame.image.load(img))

        # 飞机坠毁的声音
        if self.down_sounds_src:
            self.down_sounds = pygame.mixer.Sound(self.down_sounds_src)

    @property
    def image(self):
        return self.img_list[0]

    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def move_up(self):
        """飞机向上移动"""
        self.rect.top -= self.speed

    def move_down(self):
        """飞机向下移动"""
        self.rect.top += self.speed

    def move_left(self):
        """飞机向左移动"""
        self.rect.left -= self.speed

    def move_right(self):
        """飞机向右移动"""
        self.rect.left += self.speed

    def broke_down(self):
        """飞机坠毁"""
        # 播放音乐
        if self.down_sounds:
            self.down_sounds.play()

        # 播放坠毁的动画
        for img in self._destroy_images_list:
            self.screen.blit(img, self.rect)

        # 坠毁时的状态
        self.active = False

    def shoot(self):
        bullet = Bullet(self.screen, self, 15)
        self.bullets.add(bullet)


# 我方的飞机
class OurPlane(Plane):
    # 飞机的图片
    plane_images = constants.OUR_PLANE_IMG_LIST
    # 飞机碰撞的图片
    destroy_images = constants.OUR_DESTROY_IMG_LIST
    # 飞机碰撞的声音
    down_sounds_src = None

    def update(self, war):
        """更新飞机的动画"""
        self.move(war.key_down)
        # 1. 切换飞机的动画效果,喷气式效果
        if war.frame % 5 == 0:
            self.screen.blit(self.img_list[0], self.rect)
        else:
            self.screen.blit(self.img_list[1], self.rect)
        # 飞机撞击检测
        rest = pygame.sprite.spritecollide(self, war.enemies, False)
        if rest:
            # 1.游戏结束
            war.status = war.OVER
            # 2.销毁敌方飞机
            # 播放销毁动画
            # for i in war.enemies:
            #     i.broken_down()
            war.enemies.empty()
            war.small_enemies.empty()

            # 3.我方飞机坠毁效果
            self.broke_down()
            # 4.记录游戏的成绩

    def move(self, key):
        """飞机移动自动控制"""
        if key == pygame.K_w or key == pygame.K_UP:
            self.move_up()
        elif key == pygame.K_s or key == pygame.K_DOWN:
            self.move_down()
        elif key == pygame.K_a or key == pygame.K_LEFT:
            self.move_left()
        elif key == pygame.K_d or key == pygame.K_RIGHT:
            self.move_right()


    def move_up(self):
        super().move_up()
        if self.rect.top <= 0:
            self.rect.top = 0

    def move_down(self):
        super().move_down()
        if self.rect.bottom >= self.height:
            self.rect.bottom = self.height

    def move_left(self):
        super().move_left()
        if self.rect.left <= 0:
            self.rect.left = 0

    def move_right(self):
        super().move_right()
        if self.rect.right >= self.width:
            self.rect.right = self.width


class SmallEnemyPlane(Plane):
    # 敌方飞机的图片
    plane_images = constants.SMALL_ENEMY_PLANE_IMG_LIST
    # 敌方飞机碰撞的图片
    destroy_images = constants.SMALL_ENEMY_PLANE_DESTROY_IMG_LIST
    # 敌方飞机的坠毁声音
    down_sounds_src = constants.SMALL_ENEMY_PLANE_DOWN_SOUND

    def __init__(self, screen, speed):
        super().__init__(screen, speed)
        # 改变飞机的初始位置
        self.init_pos()

    def init_pos(self):
        """改变飞机的位置"""
        # 每次生成一架新飞机的时候，随机的位置出现在屏幕中
        self.rect.left = random.randint(0, self.width - self.plane_w)
        # 屏幕之外的随即高度产生飞机
        self.rect.top = random.randint(-5 * self.plane_h, - self.plane_h)

    def update(self, *args):
        """更新飞机的移动"""
        super().move_down()
        self.blit_me()
        # 超出范围后如何处理
        # 重用
        if self.rect.top >= self.height:
            self.active = True
            self.reset()

    def reset(self):
        self.active = True
        self.init_pos()

    def broken_down(self):
        """飞机爆炸效果"""
        super().broke_down()
        self.reset()
