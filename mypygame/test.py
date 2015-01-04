#coding=utf-8
'''
Created on 2014��10��23��

@author: ����_2
'''
import pygame
import random
pygame.init()

screen = pygame.display.set_mode((640,480))
badguys = []

badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg2 = pygame.image.load("resources/images/badguy2.png")
badguyimg3 = pygame.image.load("resources/images/badguy3.png")
badguyimg4 = pygame.image.load("resources/images/badguy4.png")
allbadguyimg=[badguyimg1,badguyimg2,badguyimg3,badguyimg4]
badguyimg = allbadguyimg[0]
timer = 100
timer1 = 0
while 1:
    screen.fill(0)
    i = 0
    y = random.randint(50,430)
#     if timer <= 0:
#         timer = 100 - (timer1 * 2)
#         if timer1 >= 35:
#             timer1 = 35
#         else:
#             timer1 += 5
    timer -= 3
    index = 1
    if timer < 0:
        for b in badguys:
                b[0] -= 7
                if b[0] < 50:
                    badguyimg
        timer = 100
    

    for b in badguys:
        screen.blit(badguyimg,b)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            badguys.append(list(position))
    pygame.display.flip()