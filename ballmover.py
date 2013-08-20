#!/usr/bin/python

import Leap
import pygame
from pygame.locals import QUIT

HEIGHT=800
WIDTH=600

#swiped from http://www.pygame.org/docs/tut/tom/games6.html
def load_png(filename):
    """ Load image and return image object"""
    try:
        image = pygame.image.load(filename)
        if image.get_alpha is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error, message:
        print 'Cannot load image:', filename
        raise SystemExit, message
    return image, image.get_rect()


class Ball(pygame.sprite.Sprite):
    def __init__(self, (xy)):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('ball.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

    def move(self, x, y):
        self.rect.x=x
        self.rect.y=y

class TouchPointListener(Leap.Listener):
    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        frame = controller.frame()
        interactionBox = frame.interaction_box
        for pointable in frame.pointables:
            #Convert the coordinates to something we can use
            normalizedPosition = interactionBox.normalize_point(
                pointable.tip_position)
            #Move the ball
            self.ball.move(normalizedPosition.x * HEIGHT,
                WIDTH - normalizedPosition.y * WIDTH)

    def set_ball(self, ball):
        self.ball = ball


def main():
    pygame.init()
    screen = pygame.display.set_mode((HEIGHT, WIDTH))
    pygame.display.set_caption('Move the ball')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    ball = Ball((0,0))
    ballsprite = pygame.sprite.RenderPlain(ball)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    #Leap stuff
    leap = Leap.Controller()
    listener = TouchPointListener()
    listener.set_ball(ball)
    leap.add_listener(listener)

    clock = pygame.time.Clock()
    while 1:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.blit(background, (0,0))
        ballsprite.update()
        ballsprite.draw(screen)
        pygame.display.flip()


if __name__ == '__main__': main()
