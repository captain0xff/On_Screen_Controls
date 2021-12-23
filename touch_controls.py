import pygame as pg

class Game:
    def __init__(self):
        self.swidth=1024
        self.sheight=768
        self.screen=pg.display.set_mode((self.swidth,self.sheight),pg.SCALED|pg.FULLSCREEN)
        self.rng=True
        self.clock=pg.time.Clock()
        self.fps=60
        self.joystick1=Joystick(self.swidth,self.sheight,self.screen,(250,550),activate_after_stick_touched=True,stick_colour_before_bind='Black',stick_colour_after_bind='Yellow')
        self.joystick2=Joystick(self.swidth,self.sheight,self.screen,(800,550),auto_center=False)
        self.button=Button(self.swidth,self.sheight,self.screen,(100,100,100,100))
        self.toggle_button=Button(self.swidth,self.sheight,self.screen,pg.Rect(800,100,100,100),toggle_enabled=True)

    def main(self):
        while self.rng:
            self.screen.fill((255,0,255))

            for ev in pg.event.get():
                if ev.type==pg.QUIT:
                    self.rng=False
                if ev.type==pg.KEYDOWN:
                    if ev.key in (pg.K_ESCAPE,pg.K_AC_BACK):
                        self.rng=False
                self.joystick1.events(ev)
                self.joystick2.events(ev)
                self.button.events(ev)
                self.toggle_button.events(ev)
                

            #Handle the events
            self.joystick1.physics()
            self.joystick2.physics()

            #Draw the objects
            self.joystick1.draw()
            self.joystick2.draw()
            self.button.draw()
            self.toggle_button.draw()

            if self.rng:
                pg.display.update()


class Joystick:
    def __init__(self,swidth,sheight,screen,center_pos,
            radius=200,
            stick_radius=50,
            action_radius=200,
            auto_center=True,
            activate_after_stick_touched=False,
            colour='White',
            stick_colour_before_bind='Blue',
            stick_colour_after_bind='Green'):
        self.swidth,self.sheight=swidth,sheight
        self.screen=screen
        self.radius=radius
        self.stick_radius=stick_radius
        self.action_radius=action_radius
        self.auto_center=auto_center
        self.activate_after_stick_touched=activate_after_stick_touched
        self.center_pos=pg.math.Vector2(center_pos)
        self.stick_pos=pg.math.Vector2(self.center_pos)
        self.colour=colour
        self.stick_colour_before_bind=stick_colour_before_bind
        self.stick_colour_after_bind=stick_colour_after_bind
        self.stick_colour=self.stick_colour_before_bind
        self.finger_pos=None
        self.binding_finger_id=None
        self.phasor=pg.math.Vector2(0,0)
        
    def physics(self):
        if self.binding_finger_id!=None:
            relative_finger_pos=pg.math.Vector2(self.finger_pos-self.center_pos)
            relative_finger_length=relative_finger_pos.magnitude()
            if relative_finger_length<=self.radius:
                self.stick_pos=self.finger_pos
            else:
                self.stick_pos=pg.math.Vector2(relative_finger_pos*(self.radius/relative_finger_length)+self.center_pos)
            threshold=relative_finger_length/self.radius
            if threshold>1:
                threshold=1
            self.phasor=relative_finger_pos*(threshold/relative_finger_length)
        elif self.auto_center is True:
            self.phasor=pg.math.Vector2(0,0)

    def get_properties(self):
        return self.phasor,self.binding_finger_id

    def draw(self):
        pg.draw.circle(self.screen,self.colour,self.center_pos,self.radius)     #Draw the joystick
        pg.draw.circle(self.screen,self.stick_colour,self.stick_pos,self.stick_radius)    #Draw the stick

    def events(self,ev):
        if ev.type==pg.FINGERDOWN:
            finger_pos=pg.math.Vector2(ev.x*self.swidth,ev.y*self.sheight)
            s=(finger_pos.x-self.center_pos.x)**2+(finger_pos.y-self.center_pos.y)**2
            if self.activate_after_stick_touched:
                if s<=self.stick_radius**2:
                    self.binding_finger_id=ev.finger_id
                    self.finger_pos=finger_pos
                    self.stick_colour=self.stick_colour_after_bind
            else:
                if s<=self.radius**2:
                    self.binding_finger_id=ev.finger_id
                    self.finger_pos=finger_pos
                    self.stick_colour=self.stick_colour_after_bind
        elif ev.type==pg.FINGERUP:
            if ev.finger_id==self.binding_finger_id:
                if self.auto_center:
                    self.binding_finger_id=None
                    self.stick_colour=self.stick_colour_before_bind
                    self.stick_pos=self.center_pos
                else:
                    self.binding_finger_id=None
                    self.finger_pos=None
                    self.stick_colour=self.stick_colour_before_bind
        elif ev.type==pg.FINGERMOTION:
            if ev.finger_id==self.binding_finger_id:
                self.finger_pos=pg.math.Vector2(ev.x*self.swidth,ev.y*self.sheight)


class Button:
    def __init__(self,swidth,sheight,screen,rect,
            colour_before_press='Blue',
            colour_after_press='Red',
            width=0,
            toggle_enabled=False
            ):
        self.swidth,self.sheight=swidth,sheight
        self.screen=screen
        self.rect=pg.Rect(rect)
        self.colour_before_press=colour_before_press
        self.colour_after_press=colour_after_press
        self.colour=colour_before_press
        self.width=width
        self.is_pressed=False
        self.toggle_enabled=toggle_enabled
        if self.toggle_enabled:
            self.toggle_state=False
        self.binding_finger_id=None

    def physics(self):
        pass

    def properties(self):
        if self.toggle_enabled:
            return self.binding_finger_id,self.is_pressed,self.toggle_state
        else:
            return self.binding_finger_id,self.is_pressed

    def draw(self):
        pg.draw.rect(self.screen,self.colour,self.rect,self.width)

    def events(self,ev):
        if self.toggle_enabled:
            if ev.type==pg.FINGERDOWN and self.rect.collidepoint((ev.x*self.swidth,ev.y*self.sheight)):
                self.binding_finger_id=ev.finger_id
                self.is_pressed=True
                self.colour=self.colour_after_press
                if self.toggle_state is True:
                    self.toggle_state=False
                    self.colour=self.colour_before_press
                else:
                    self.toggle_state=True
                    self.colour=self.colour_after_press

        else:
            if ev.type==pg.FINGERDOWN and self.rect.collidepoint((ev.x*self.swidth,ev.y*self.sheight)):
                self.binding_finger_id=ev.finger_id
                self.is_pressed=True
                self.colour=self.colour_after_press
            elif ev.type==pg.FINGERUP and ev.finger_id==self.binding_finger_id:
                self.binding_finger_id=None
                self.colour=self.colour_before_press



if __name__=='__main__':
    pg.init()
    game=Game()
    game.main()
    pg.quit()
