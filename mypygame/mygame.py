#coding=gbk
'''
Created on 2014年10月21日
@author: 洪振_2
'''
#1.导入pygame
import pygame
import math
import random
#2.初始化游戏
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
keys = [False,False,False,False] #移动的方向
playerpos = [132,123]
drawplayerpos = [playerpos[0]-32,playerpos[1]-23]
#增加弓箭
acc=[0,0]#命中数和射击数
arrows=[]
#增加坏蛋
badtimer = 100
badtimer1 = 0
badguys = [[640,100]]
healthvalue = 194
pygame.mixer.init()
#3.导入图片
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg2 = pygame.image.load("resources/images/badguy2.png")
badguyimg3 = pygame.image.load("resources/images/badguy3.png")
badguyimg4 = pygame.image.load("resources/images/badguy4.png")
badguyimg = badguyimg1
allbadguyimg=[badguyimg1,badguyimg2,badguyimg3,badguyimg4]
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")
# 3.1 - Load audio
hit = pygame.mixer.Sound("resources/audio/explode.wav")
enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)
pygame.mixer.music.load('resources/audio/moonlight.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
#4.while循环游戏
running = 1
exitcode = 0
while running:
    badtimer -= 3
    #5.绘图前填充
    screen.fill(0)
    #6.画图
    
    #6.2画出草
    '''for x in range(0,width,100):
        #print('x',x)
        for y in range(0,height,100):
            #print('y',y)
            screen.blit(grass,(x,y))'''
    for x in range(width//grass.get_width()+1):
        for y in range(height//grass.get_height()+1):
            screen.blit(grass,(x*100,y*100))
    #6.3画出城堡
    for y in range(10,height,120):
        screen.blit(castle,(0,y+7.5))
    #6.1画个player
    #screen.blit(player,playerpos)
    #6.1.1 根据鼠标位置画player
    moucepos = pygame.mouse.get_pos()
    #print(moucepos)
    angle = math.atan2((moucepos[1] - (playerpos[1] + 23)),(moucepos[0] - (playerpos[0]+32))) / math.pi * 180
    playerrot = pygame.transform.rotate(player, 360-angle)
#     print(playerpos)
    
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
#     print(playerpos1)
    screen.blit(playerrot,playerpos1)
#     screen.blit(playerrot,drawplayerpos)
#     print(angle)
    
    #6.1.2 画箭头
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0]) * 10
        vely = math.sin(bullet[0]) * 10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow,360-projectile[0]/math.pi*180)
            screen.blit(arrow1,(projectile[1],projectile[2]))
            
    #6.1.3画坏蛋
    if badtimer <= 0:
        badguys.append([640,random.randint(50,430)])
        badtimer = 100 - (badtimer1 * 2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    index = 0 
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index)
       
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            hit.play()
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
        index1 = 0
#         i = 0
        for bullet in arrows:
            bullrect = pygame.Rect(arrow.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                enemy.play()
                acc[0] += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
       
        badguy[0] -= 7
#         badguyimg = allbadguyimg[i%4]
        index += 1
#         i += 1
    for badguy in badguys:
        #print(badguy)
        screen.blit(badguyimg,badguy)    
    #6.1.4画上时钟
    font = pygame.font.Font(None,24)
#     print(pygame.time.get_ticks())
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"
                               +str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright = [600,5]
    screen.blit(survivedtext,textRect.topright)
    #6.5画生命线
    screen.blit(healthbar,(5,5))
    for health1 in range(healthvalue):
        screen.blit(health,(health1+8,8))
    #7.刷新屏幕
    pygame.display.flip()
    #8.监听事件
    for event in pygame.event.get():
        #8.1关闭事件
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        #8.2键盘的上下左右或WSAD事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys[0] = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys[1] = True
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                keys[2] = True
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys[3] = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys[0] = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys[1] = False
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                keys[2] = False
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                keys[3] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1 #射击数加1
#             arrowspos = [playerrot.get_rect().width/2,playerrot.get_rect().height/2]
            arrows.append([math.atan2((position[1] - (playerpos1[1] + 23)),(position[0] - (playerpos1[0]+32))),
                                   playerpos1[0]+playerrot.get_rect().width/2,playerpos1[1]+playerrot.get_rect().height/2])
#             print(acc[1])
            
    if keys[0]:
        if playerpos[1] > 23:
            playerpos[1] -= 5
    if keys[1]:
        if playerpos[1] < height - player.get_height()+23:
            playerpos[1] += 5
    if keys[2]:
        if playerpos[0] > 32:
            playerpos[0] -= 5
    if keys[3]:
        if playerpos[0] < width - player.get_width()+32:
            playerpos[0] += 5
            
    #10判断胜负
    if pygame.time.get_ticks() >= 90000:
        running = 0
        exitcode = 1
    if healthvalue <= 0:
        running = 0
        exitcode = 0
    if acc[1] != 0:
        accuracy = acc[0] * 1.0 / acc[1] * 100
    else:
        accuracy = 0
#11-胜负显示
if exitcode == 0:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy:"+str(accuracy)+"%",True,(255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
#     print('textRect',textRect.centerx,textRect.centery)
    screen.blit(gameover,(0,0))
    screen.blit(text,textRect)
#     print('textRect',textRect)

else:
    pygame.font.init()
    font = pygame.font.Font(None, 24)
    text = font.render("Accuracy:"+str(accuracy)+"%",True,(0,255,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery + 24
    screen.blit(youwin,(0,0))
    screen.blit(text,textRect)
#     print('youwin',textRect)
    
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
    
    
    