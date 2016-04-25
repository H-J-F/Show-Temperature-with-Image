import pygame
from pygame.locals import *
import sys, threading, random
from math import pi

pygame.init()
screen = pygame.display.set_mode((600, 560), 0, 32)
screen.fill((255,225,200))
FK_surface = pygame.Surface((400,104))
FK = pygame.image.load('/home/pi/Programing/TEM/LED2/FK.gif').convert()

T = 0
temp = 0

def get_TEM():
    global temp
    global T
    T_file = open("/sys/bus/w1/devices/28-000006c9bcb1/w1_slave",'r')
    T_file.seek(69,0)
    T = int(T_file.read(5))/1000
    T_file.close()

def thermometer():
    pygame.time.delay(890)
    global temp
    global T
    y1 = 448
    y2 = 452
    i = 0
    j = 1
    k = 0
    my_font = list(range(11))
    text = list(range(11))
    text_rect = list(range(11))
    for k in range(11):
        my_font[k] = pygame.font.SysFont('droidsans', 13)
        text[k] = my_font[k].render("%s" % (k*5), True, (0,0,0))
        text_rect[k] = text[k].get_rect()
        text_rect[k].center = (40,448-k*35)

    pygame.draw.circle(screen, (170,170,170), (90,472), 60)
    pygame.draw.circle(screen, (170,170,170), (90,80), 60)
    pygame.draw.rect(screen, (170,170,170), ((30,80), (120,393)))
    pygame.draw.circle(screen, (210,210,210), (90,472), 31)
    pygame.draw.line(screen, (210,210,210), (74,80), (74,453), 6)
    pygame.draw.line(screen, (210,210,210), (105,80), (105,453), 6)
    pygame.draw.arc(screen, (210,210,210), ((72,66), (36,38)), 0, pi, 6)
    pygame.draw.arc(screen, (210,210,210), ((73,66), (35,36)), 0, pi, 5)
    
    for k in range(11):
        screen.blit(text[k], text_rect[k])
    while y1 >= 96:
        if i%5 == 0:
            pygame.draw.line(screen, (0,0,0), (50,y1), (70,y1))
        else:
            pygame.draw.line(screen, (0,0,0), (55,y1), (70,y1))
        y1 -= 7
        i += 1

    pygame.draw.circle(screen, (255,50,50), (90,472), 25)
    pygame.display.update()

    while j <= 7*T:
        pygame.draw.rect(screen, (255,50,50), ((79,y2-j-4), (23,j+4)))
        pygame.display.update()
        j += 2
    while True:
        get_TEM()
        if T - temp >= 0:
            pygame.draw.rect(screen, (255,50,50), ((79,y2-7*T-3), (23,7*T+3)))
            pygame.display.update()
            temp = T
        else:
            pygame.draw.rect(screen, (170,170,170), ((79,90), (23,359-7*T)))
            pygame.display.update()
            temp = T

def display_T():
    global FK_surface
    tem_font = pygame.font.SysFont('dejavusansmono',20)
    while True:
        get_TEM()
        text_tem = tem_font.render('Temperature = %r\'C' % T, True, (random.randint(1,255),random.randint(1,255),random.randint(1,255)))
        rect_tem = text_tem.get_rect()
        rect_tem.center = (200,50)
        FK_surface.fill((255,225,200))
        FK_surface.blit(FK, (0,0))
        FK_surface.blit(text_tem, rect_tem)
        screen.blit(FK_surface, (180,20))

def kill_PRO():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

th_TMT = threading.Thread(target = thermometer)
th_DT = threading.Thread(target = display_T)
th_kill = threading.Thread(target = kill_PRO)

get_TEM()

try:
    th_kill.start()
    th_DT.start()
    th_TMT.start()
    while True:
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()
