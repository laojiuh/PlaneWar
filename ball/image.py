# 1.引入相关的包
import sys, pygame

# 2. pygame进行初始化
pygame.init()

size = width, height = 500, 500
speed1 = [10, 10]
speed2 = [10, 10]
# 3. 得到屏幕对象Surface
screen = pygame.display.set_mode(size)

ball = pygame.image.load("intro_ball.gif")

ballrect = ball.get_rect()
ballrect2 = ball.get_rect()
ballrect2.left += 200
ballrect2.top += 200

clock = pygame.time.Clock()

# 4. 游戏主循环
while 1:
    # 处理游戏的事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # 更新游戏的状态
    ballrect = ballrect.move(speed1)
    ballrect2 = ballrect2.move(speed2)
    if ballrect.left < 0 or ballrect.right > width:
        speed1[0] = -speed1[0]
    elif ballrect.top < 0 or ballrect.bottom > height:
        speed1[1] = -speed1[1]

    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]
    elif ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]

    clock.tick(30)

    # 在屏幕上进行绘制
    screen.fill(pygame.Color(150, 150, 250))
    screen.blit(ball, ballrect)
    screen.blit(ball, ballrect2)
    pygame.display.flip()
