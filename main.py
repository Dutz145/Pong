import pygame, sys
from pong import Player, Ball, AIOponent
from random import choice

pygame.init()

width, height = 700, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")

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