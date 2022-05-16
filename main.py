import math
import random
import pymunk
import pygame as pg
import pymunk.pygame_util

pymunk.pygame_util.positive_y_is_up = False


clock = pg.time.Clock()

body = pymunk.Body()
ball_mass, ball_radius = 1, 10
class Game:
    pg.init()
    def __init__(self):
        self.name_game = pg.image.load('Interface_pictures/name.png')
        self.name_game_pos = pymunk.Vec2d(0, 0)
        self.start_button = pg.image.load('Interface_pictures/start.png')
        self.start_button_pos = pymunk.Vec2d(0, 100)

        self.WIDTH = 1280
        self.HEIGHT = 720
        self.FPS = 100
        self.surface = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.draw_options = pymunk.pygame_util.DrawOptions(self.surface)
        self.space = pymunk.Space()
        self.gravityStrength = 10.0e6
        self.gravity_pos = pymunk.Vec2d(0, 0)

        self.body = pymunk.Body()
        self.ball_mass = 1
        self.ball_radius = 10
        self.active_window = 'menu'

    def planetGravity(self, body, gravity, damping, dt):
        sq_dist = body.position.get_dist_sqrd(self.gravity_pos)
        g = (
                (body.position - self.gravity_pos)
                * - self.gravityStrength
                / (sq_dist * math.sqrt(sq_dist))
        )
        pymunk.Body.update_velocity(body, g, damping, dt)

    def create_platform(self, space):
        segment_shape_1 = pymunk.Segment(space.static_body, (2, self.HEIGHT), (self.WIDTH, self.HEIGHT), 26)
        space.add(segment_shape_1)
        segment_shape_1.elasticity = 0.0
        segment_shape_1.friction = 1.0
        segment_shape_2 = pymunk.Segment(space.static_body, (2, 2), (self.WIDTH, 2), 26)
        space.add(segment_shape_2)
        segment_shape_2.elasticity = 0.0
        segment_shape_2.friction = 1.0
        segment_shape_3 = pymunk.Segment(space.static_body, (self.WIDTH, 2), (self.WIDTH, self.HEIGHT), 26)
        space.add(segment_shape_3)
        segment_shape_3.elasticity = 0.0
        segment_shape_3.friction = 1.0
        segment_shape_4 = pymunk.Segment(space.static_body, (2, 2), (2, self.HEIGHT), 26)
        space.add(segment_shape_4)
        segment_shape_4.elasticity = 0.0
        segment_shape_4.friction = 1.0

    def create_ball(self, space, pos):
        ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
        ball_body = pymunk.Body(ball_mass, ball_moment)
        ball_body.position = pos
        ball_shape = pymunk.Circle(ball_body, ball_radius)
        ball_shape.elasticity = 0.0
        ball_shape.friction = 0.6
        space.add(ball_body, ball_shape)
        ball_body.velocity_func = self.planetGravity
        return ball_body

    def try_to_click(self, pos):
        if self.active_window == 'menu':
            if 0 < pos[0] < 1280 and 100 < pos[1] < 720:
                self.active_window = 'game'
        if self.active_window == 'game':
            if 0 < pos[0] < 640 and 0 < pos[1] < 720:
                if self.gravity_pos == (0,0) or self.gravity_pos == (0, 144
                                ) or self.gravity_pos == (0, 288) or self.gravity_pos == (0, 432) or self.gravity_pos == (0, 576):
                    self.gravity_pos += pymunk.Vec2d(0, 144)
                elif self.gravity_pos == (0,720) or self.gravity_pos == (256, 720
                                ) or self.gravity_pos == (512, 720) or self.gravity_pos == (768, 720) or self.gravity_pos == (1024, 720):
                    self.gravity_pos += pymunk.Vec2d(256, 0)
                elif self.gravity_pos == (1280,720) or self.gravity_pos == (1280, 144
                                ) or self.gravity_pos == (1280, 288) or self.gravity_pos == (1280, 432) or self.gravity_pos == (1280, 576):
                    self.gravity_pos += pymunk.Vec2d(0, -144)
                elif self.gravity_pos == (1280, 0) or self.gravity_pos == (256, 0
                                ) or self.gravity_pos == (512, 0) or self.gravity_pos == (768, 0) or self.gravity_pos == (1024, 0):
                    self.gravity_pos += pymunk.Vec2d(-256, 0)
            elif 641 < pos[0] < 1280 and 0 < pos[1] < 720:
                if self.gravity_pos == (0, 144) or self.gravity_pos == (0, 288) or self.gravity_pos == (0, 432) or self.gravity_pos == (0, 576) or self.gravity_pos == (0, 720):
                    self.gravity_pos += pymunk.Vec2d(0, -144)
                elif self.gravity_pos == (256, 720) or self.gravity_pos == (512, 720) or self.gravity_pos == (768, 720) or self.gravity_pos == (1024, 720) or self.gravity_pos == (1280, 720):
                    self.gravity_pos += pymunk.Vec2d(-256, 0)
                elif self.gravity_pos == (1280,720) or self.gravity_pos == (1280, 144
                                ) or self.gravity_pos == (1280, 288) or self.gravity_pos == (1280, 432) or self.gravity_pos == (1280, 576) or self.gravity_pos == (1280, 0):
                    self.gravity_pos += pymunk.Vec2d(0, 144)
                elif self.gravity_pos == (256, 0) or self.gravity_pos == (512, 0) or self.gravity_pos == (768, 0) or self.gravity_pos == (1024, 0) or self.gravity_pos == (0, 0):
                    self.gravity_pos += pymunk.Vec2d(256, 0)
    def menu_draw(self):
        self.surface.fill((0, 0, 0))
        self.surface.blit(self.name_game, self.name_game_pos)
        self.surface.blit(self.start_button, self.start_button_pos)



    def draw(self):
        if self.active_window == 'game':
            self.surface.fill((0, 0, 0))
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    exit()

            self.space.step(1 / self.FPS)
            self.space.debug_draw(self.draw_options)

            pg.draw.circle(self.surface, pg.Color("red"), self.gravity_pos, 50)
        elif self.active_window == 'menu':
            self.menu_draw()


    def start(self):
        self.create_ball(self.space, (26, 26))
        self.create_platform(self.space)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return 0
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.try_to_click(event.pos)
            self.draw()
            pg.display.flip()



game = Game()
game.start()

