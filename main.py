import pygame
import os
import random

pygame.mixer.init()

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lime = (0, 255, 0)
blue = (0, 0, 255)
ran = (0, 128, 128)
# Creating window
screen_width = 1366
screen_height = 738
gameWindow = pygame.display.set_mode((screen_width, screen_height))

bg1 = pygame.image.load("bg.jpg")
bg2 = pygame.image.load("bg2.jpg")
intro = pygame.image.load("intro1.png")
outro = pygame.image.load("outro.png")

# Game Title
pygame.display.set_caption("Snake game by hacker hunt")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont('Harrington', 55)


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(intro, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.fadeout(200)
                    pygame.mixer.music.load('bgm.mp3')
                    pygame.mixer.music.play(100)
                    pygame.mixer.music.set_volume(.6)
                    gameloop()
        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1

    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
    with open("highscore.txt", "r") as f:
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 5
    snake_size = 15
    fps = 80
    while not exit_game:
        if game_over:
            gameWindow.fill(blue)
            gameWindow.blit(outro, (0, 0))
            text_screen("", black, 50, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('wc.mp3')
                        pygame.mixer.music.play()
                        gameloop()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_w:
                        fps = fps + 50

                    if event.key == pygame.K_s:
                        fps = fps - 5

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 12 and abs(snake_y - food_y) < 12:
                score += 1
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 1

            gameWindow.fill(lime)
            gameWindow.blit(bg1, (0, 0))
            text_screen(f"Score:{score}", red, 5, 5)
            pygame.draw.rect(gameWindow, white, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load('snakehiss2.mp3')
                pygame.mixer.music.play()
                game_over = True

            if snake_x > screen_width:
                snake_x = 0

            if snake_y > screen_height:
                snake_y = 0

            plot_snake(gameWindow, blue, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


pygame.mixer.music.load('wc.mp3')
pygame.mixer.music.play()
welcome()
