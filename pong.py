import pygame, sys
from random import choice

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")

class Ball:
    def __init__(self, y_direction, facing, go_left=False, go_right=True):
        self.width = 10
        self.height = 10

        self.go_right = go_right
        self.go_left = go_left

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(center = (width//2, height//2))

        self.y_direction = y_direction
        self.facing = facing

    def choose_direction(self, y_direction, facing):
        if facing == 1: 
            self.go_right = True
            self.go_left = False
            self.facing = 1
        else:
            self.go_right = False
            self.go_left = True
            self.facing = -1

        self.y_direction = y_direction

    def move(self):
        if self.go_right:
            self.rect.x += 5 * self.facing
            self.rect.y += 3 * self.y_direction

        else:
            self.rect.x += 5 * self.facing
            self.rect.y += 3 * self.y_direction

        if self.rect.bottom >= height:
            self.choose_direction(-1,self.facing)

        if self.rect.top <= 0:
            self.choose_direction(1, self.facing)

        if self.rect.left <= 0:
            self.choose_direction(self.y_direction, 1)

        if self.rect.right >= width:
            self.choose_direction(self.y_direction, -1)

    def draw(self, screen):
        pygame.draw.circle(screen, "White", self.rect.center, 15)

    def update(self, screen):
        self.draw(screen)
        self.move()

class Player:
    def __init__(self):
        self.width = 10
        self.height = 100
        self.vel = 0

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(midright = (width, height//2))

        self.score = 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.vel = -7
            self.rect.y += self.vel

        if keys[pygame.K_DOWN] and self.rect.bottom < height:
            self.vel = 7
            self.rect.y += self.vel

    def collide_ball(self, ball_obj):
        if pygame.Rect.colliderect(self.rect, ball_obj.rect):
            ball_obj.go_left = True
            ball_obj.go_right = False

            if self.vel > 0:
                ball_obj.choose_direction(1, -1)
            else:
                ball_obj.choose_direction(-1, -1)

    def draw(self, screen):
        pygame.draw.rect(screen, "White", (self.rect.x, self.rect.y, self.width, self.height))

    def update(self, screen, ball_obj):
        self.get_input()
        self.draw(screen)
        self.collide_ball(ball_obj)

class AIOponent:
    def __init__(self):
        self.vel = 0
        self.width = 10
        self.height = 100

        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect(midleft = (0, height//2))

        self.score = 0

    def collide_ball(self, ball_obj):
        if pygame.Rect.colliderect(self.rect, ball_obj.rect):
            if self.vel > 0:
                ball_obj.choose_direction(1, 1)
            else:
                ball_obj.choose_direction(-1, 1)

    def beatable_move(self, ball_obj):
        if ball_obj.y_direction < 0 and ball_obj.facing == -1:
            self.vel = -3
            self.rect.y += self.vel
        elif ball_obj.y_direction > 0 and ball_obj.facing == -1:
            self.vel = 3
            self.rect.y += self.vel
        else:
            self.vel = 0
            self.rect.y += self.vel

        if self.rect.bottom >= height:
            self.rect.bottom = height

        if self.rect.top <= 0:
            self.rect.top = 0

    def unbeatable_move(self, ball_obj):
        self.rect.y = ball_obj.rect.y

    def draw(self, screen):
        pygame.draw.rect(screen, "White", (self.rect.x, self.rect.y, self.width, self.height))

    def update(self, screen, ball_obj, move):
        move(ball_obj)
        self.collide_ball(ball_obj)
        self.draw(screen)

font = pygame.font.SysFont("comicsans", 50)

def main():
    clock = pygame.time.Clock()

    player = Player()
    ball = Ball(choice([1, -1]), choice([1, -1]), False, True)
    oponent = AIOponent()

    player_score = 0

    game_active = True

    choose_ai_move = pygame.USEREVENT
    pygame.time.set_timer(choose_ai_move, 15000)

    move_choice = oponent.beatable_move

    def score(ball, oponent, player):
        if ball.rect.right >= width:
            oponent.score += 1
        
        if ball.rect.left <= 0:
            player.score += 1

    while game_active:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (oponent.score == 10 or player.score == 10):
                game_active = False

            if event.type == choose_ai_move:
                move_choice = choice([oponent.unbeatable_move, oponent.beatable_move])

        screen.fill("Black")
        player.update(screen, ball)
        ball.update(screen)
        oponent.update(screen, ball, move_choice)
        score(ball, oponent, player)

        oponent_score = font.render(f"Oponent: {oponent.score}", 0, "Red")
        oponent_score_rect = oponent_score.get_rect(midtop = (width//4, 10))
        screen.blit(oponent_score, oponent_score_rect)

        player_score = font.render(f"Player: {player.score}", 0, "Gold")
        player_score_rect = player_score.get_rect(midtop = (width - width//4, 10))
        screen.blit(player_score, player_score_rect)

        pygame.display.update()

def main_menu():
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                main()


        screen.fill("Black")

        text_1 = font.render(f"Welcome to Pong!", 0, "White")
        text_1_rect = text_1.get_rect(center = (width//2, height//4))
        screen.blit(text_1, text_1_rect)

        text_2 = font.render(f"Press any button to start", 0, "Gold")
        text_2_rect = text_2.get_rect(center = (width//2 + 10, text_1_rect.bottom + 10))
        screen.blit(text_2, text_2_rect)

        pygame.display.update()

if __name__ == "__main__":
    main_menu()