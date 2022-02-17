import pygame as pg
import math
from touch_controls import Joystick
from touch_controls import Button

class Game:
    def __init__(self):
        pg.init()
        self.swidth=1024
        self.sheight=768
        self.screen=pg.display.set_mode((self.swidth,self.sheight),pg.SCALED|pg.FULLSCREEN)
        self.rng=True
        self.clock=pg.time.Clock()
        self.fps=60
        self.player=Player(self.swidth,self.sheight,self.screen)
        self.joystick1=Joystick(self.swidth,self.sheight,self.screen,(200,550),radius=150,colour='Purple')
        self.joystick2=Joystick(self.swidth,self.sheight,self.screen,(800,550),auto_center=False,radius=150,colour='Purple')

    def main(self):
        while self.rng:
            dt=self.clock.tick(self.fps)/1000
            
            self.screen.fill((255,0,255))

            #Check for events
            for ev in pg.event.get():
                if ev.type==pg.QUIT:
                    self.rng=False
                elif ev.type==pg.KEYDOWN:
                    if ev.key in (pg.K_ESCAPE,pg.K_AC_BACK):
                        self.rng=False
                self.joystick1.events(ev)
                self.joystick2.events(ev)

            #Handle the events
            self.joystick1.physics()
            self.joystick2.physics()
            phasor1=self.joystick1.get_properties()[0]
            phasor2=self.joystick2.get_properties()[0]
            self.player.physics(phasor2,phasor1,dt)

            #Draw the objects on the screen
            self.player.draw()
            self.joystick1.draw()
            self.joystick2.draw()

            if self.rng:
                pg.display.update()
            else:
                pg.quit()


class Player:
    def __init__(self,swidth,sheight,screen):
        self.swidth,self.sheight=swidth,sheight
        self.screen=screen
        self.image=pg.image.load('Hero.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.pos=pg.math.Vector2(swidth/2,sheight/2)
        self.max_vel=50
        self.rotated_image=self.image
        self.rotated_rect=self.rotated_image.get_rect()
        self.rotated_rect.center=self.pos

    def physics(self,phasor1,phasor2,dt):
        self.pos+=pg.math.Vector2(phasor2*self.max_vel*dt)
        print(phasor2,phasor2*self.max_vel*dt)
        try:
            angle=-math.degrees(math.atan(phasor1.y/phasor1.x))
        except ZeroDivisionError:
            angle=0
        if phasor1.x<0:
        	angle+=180
        self.rotated_image=pg.transform.rotate(self.image,angle)
        self.rotated_rect=self.rotated_image.get_rect()
        self.rotated_rect.center=self.pos

    def draw(self):
        self.screen.blit(self.rotated_image,self.rotated_rect)



if __name__=='__main__':
    game=Game()
    game.main()
