import pygame
from pygame.locals import *
from config import *
from human_controls import HumanInput
from hardcoded_ai import HardcodedAi
import random
import math


class App:
    def __init__(self):
        self._running = True
        self.display_surf = None
        self._image_surf = None
        self.left_paddle = pygame.Rect((LEFT_GUY_X, STARTING_POSITION_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.right_paddle = pygame.Rect((RIGHT_GUY_X, STARTING_POSITION_Y), (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.ball = pygame.Rect((GAME_HEIGHT/2, GAME_WIDTH/2), BALL_SIZE)
        self.player_one = HumanInput()
        self.player_two = HardcodedAi()
        self.system_clock = pygame.time.Clock()
        self.ball_velocity = [0, 0]

    def randomise_ball_vel(self):
        ball_direction = (random.random() * (math.pi/2)) - math.pi/4
        if random.randint(0, 1) == 1:
            ball_direction = ball_direction + math.pi
        self.ball_velocity = [math.cos(ball_direction) * BALL_SPEED, math.sin(ball_direction) * BALL_SPEED]

    def ball_paddle_redirect(self, paddle: pygame.Rect):
        collision_vet = [self.ball.center[0] - paddle.center[0], self.ball.center[0] - paddle.center[0]]
        collision_angle = math.atan2(collision_vet[1], collision_vet[0])
        self.ball_velocity = [math.cos(collision_angle) * BALL_SPEED, math.sin(collision_angle) * BALL_SPEED]

    def on_init(self):
        pygame.init()
        self.display_surf = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        self.randomise_ball_vel()
        return True

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    # ballx = 0, bally = 1, lastballx = 2, lastbally = 3, mey = 4, enemyy = 5

    def on_loop(self):
        control = self.player_one.run()
        self.left_paddle = self.move_paddle(self.left_paddle, control)

        control = self.player_two.run([self.ball.centery, 0, 0, 0, self.right_paddle.centery, 0])
        self.right_paddle = self.move_paddle(self.right_paddle, control)

        self.left_paddle = self.limit_paddles(self.left_paddle)
        self.right_paddle = self.limit_paddles(self.right_paddle)
        self.ball = self.ball.move(self.ball_velocity)
        self.bounce_ball()

    def move_paddle(self, paddle: pygame.Rect, control):
        if control[0] == 1:
            paddle = paddle.move(0, -PADDLE_SPEED)
        elif control[1] == 1:
            paddle = paddle.move(0, PADDLE_SPEED)
        return paddle

    def limit_paddles(self, paddle: pygame.Rect):
        if paddle.top < 0:
            paddle.top = 0
        elif paddle.bottom > GAME_HEIGHT:
            paddle.bottom = GAME_HEIGHT
        return paddle

    def bounce_ball(self):
        if self.ball.top < 0:
            self.ball_velocity[1] = abs(self.ball_velocity[1])
        elif self.ball.bottom > GAME_HEIGHT:
            self.ball_velocity[1] = -abs(self.ball_velocity[1])

        if self.ball.colliderect(self.left_paddle):
            self.ball_paddle_redirect(self.left_paddle)
        elif self.ball.colliderect(self.right_paddle):
            self.ball_paddle_redirect(self.right_paddle)

        if self.ball.left < 0 or self.ball.right > GAME_WIDTH:
            self.restat_ball()

    def restat_ball(self):
        self.ball.centerx = GAME_WIDTH/2
        self.ball.centery = GAME_HEIGHT/2
        self.randomise_ball_vel()

    def on_render(self):
        self.display_surf.fill(BACKGROUND_COLOUR)
        pygame.draw.rect(self.display_surf, LEFT_GUY_COLOUR, self.left_paddle)
        pygame.draw.rect(self.display_surf, RIGHT_GUY_COLOUR, self.right_paddle)
        pygame.draw.rect(self.display_surf, BALL_COLOUR, self.ball)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self._running = self.on_init()

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.system_clock.tick(FRAME_RATE)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
